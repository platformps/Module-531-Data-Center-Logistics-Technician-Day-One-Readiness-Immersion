"""Check for the goals + scenario pass (v2.4). Fails non-zero.

    python3 test_goals_scenario.py ORIG_HANDOUTS NEW_HANDOUTS ORIG_TOOLS NEW_TOOLS

Handouts: Learning Objectives and Scenario lead the document, in bold on a shaded block, and not one line of
the original text is lost (tracked changes are accepted; the 531 bench goal is reworded for the virtual bench). Tools: a goals + scenario band sits above everything else in the lab, bold white on
navy, wording taken from the handout, and the rest of the file is byte-identical to the original.
Needs python-docx, pandoc and playwright (Chromium).
"""
import glob, os, re, subprocess, sys, zipfile
from collections import Counter
from docx import Document
from docx.oxml.ns import qn
from playwright.sync_api import sync_playwright

OH, NH, OT, NT = sys.argv[1:5]
fails = []
def check(ok, where, what):
    if not ok: fails.append(f"{where}: {what}")

def norm(s): return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()
def plain(path):
    out = subprocess.run(["pandoc", path, "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout
    return [norm(l) for l in out.split("\n") if norm(l)]
def dedupe(line):                          # a sentence repeated back to back (left by an accepted tracked edit) counts once
    out = []
    for x in re.split(r"(?<=[.!?])\s+", line):
        if not (out and out[-1] == x and len(x) > 12): out.append(x)
    return " ".join(out)
def lab_of(name): return re.match(r"(\d{3}-\d-\d)", name).group(1)

# ------------------------------------------------------------------ handouts
handouts = sorted(f for f in glob.glob(os.path.join(OH, "*.docx")) if "_GLAB_" in f)
new_text = {}
for f in handouts:
    name = os.path.basename(f); new = os.path.join(NH, name); lab = lab_of(name)
    o = [dedupe(l) for l in plain(f)]
    if not os.path.exists(new): check(False, name, "patched handout missing"); continue
    n = plain(new); new_text[lab] = " ".join(n)
    check(all(dedupe(l) == l for l in n), name, "a sentence is repeated back to back")
    lost = Counter(o) - Counter(n); added = Counter(n) - Counter(o)
    # the only wording that may change: the 531 bench goal, reworded for the virtual bench (one bullet per lab)
    lb = [l for l in lost if l.startswith("- ")]; ab = [l for l in added if l.startswith("- ")]
    if name.startswith("531") and lab != "531-1-3":
        check(len(lb) == 1 and len(ab) == 1 and "virtual bench" in ab[0], name, f"bench goal not reworded for the virtual bench: {lb} -> {ab}")
    else:
        check(not lb and not ab, name, f"bullets changed: {lb[:1]} {ab[:1]}")
    check(set(lost) - set(lb) <= {"Scenario and Instructions"}, name, f"text lost: {list(set(lost) - set(lb))[:3]}")
    check(set(added) - set(ab) <= {"Scenario", "Instructions"}, name, f"text added: {list(set(added) - set(ab))[:3]}")
    top = " ".join(n[:n.index("Introduction")]) if "Introduction" in n else ""
    for w in ("real carton", "real R640", "real drives", "real kit", "real end-of-life", "label printer", "physical hand-offs", "physical blind count", "physical stage cards"):
        check(w not in top, name, f"physical-kit wording still in the goals: {w}")
    d = Document(new)
    heads = [p.text.strip() for p in d.paragraphs if p.style.name.lower().startswith("heading")]
    heads = [h for h in heads if not h.startswith("GLAB")]
    check(heads[:2] == ["Learning Objectives", "Scenario"], name, f"goals and scenario are not first: {heads[:4]}")
    check("Introduction" in heads[2:4] and "Instructions" in heads, name, f"section order: {heads[:6]}")
    # everything between the Learning Objectives heading and the Introduction heading is bold on a shaded block
    on = False; nb = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if p.style.name.lower().startswith("heading"):
            if t == "Learning Objectives": on = True
            elif t == "Introduction": on = False
        if not on: continue
        nb += 1
        shd = p._element.find(qn("w:pPr") + "/" + qn("w:shd"))
        check(shd is not None and shd.get(qn("w:fill")) not in (None, "auto", "FFFFFF"), name, f"no shading on: {t[:40]}")
        for r in p._element.iter(qn("w:r")):
            if not "".join(x.text or "" for x in r.iter(qn("w:t"))).strip(): continue
            b = r.find(qn("w:rPr") + "/" + qn("w:b"))
            check(b is not None and b.get(qn("w:val")) in (None, "1", "true"), name, f"not bold: {t[:40]}")
    check(nb >= 4, name, "goal/scenario block too short")
    xo = zipfile.ZipFile(f).read("word/document.xml").decode(); xn = zipfile.ZipFile(new).read("word/document.xml").decode()
    check(xo.count("<w:tbl>") == xn.count("<w:tbl>"), name, "table count changed")
    for tag in ("<w:ins ", "<w:del ", "<w:delText"):
        check(tag not in xn, name, f"tracked change left in the handout ({tag.strip()})")

# ------------------------------------------------------------------ tools
def lum(rgb):
    v = [c / 255 for c in rgb]; v = [c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4 for c in v]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
def rgb(s): return tuple(int(float(x)) for x in re.findall(r"[\d.]+", s)[:3])

PROBE = """() => {
 const b = document.getElementById('labBrief'), g = document.getElementById('labGuide');
 if (!b) return null;
 const cs = e => getComputedStyle(e), r = b.getBoundingClientRect();
 const texts = [...b.querySelectorAll('li, p')].map(e => ({t: e.innerText, w: +cs(e).fontWeight, s: parseFloat(cs(e).fontSize), c: cs(e).color}));
 const first = [...document.querySelectorAll('main *, #sim *, section, details')].filter(e => e.offsetParent && !e.closest('header') && !e.closest('.toolbar') && !e.closest('#pbar'))
   .map(e => e.getBoundingClientRect().top).reduce((a, c) => Math.min(a, c), 1e9);
 return {top: r.top, bottom: r.bottom, vis: !!b.offsetParent, bg: cs(b).backgroundColor, before: !!(g && (b.compareDocumentPosition(g) & 4)),
   gtop: g ? g.getBoundingClientRect().top : null, first, texts,
   heads: [...b.querySelectorAll('h2')].map(h => ({t: h.innerText, c: cs(h).color, bg: cs(h).backgroundColor, w: +cs(h).fontWeight, s: parseFloat(cs(h).fontSize)})),
   goals: [...b.querySelectorAll('.lbgoals li')].map(e => e.innerText), scen: [...b.querySelectorAll('.lbscen p')].map(e => e.innerText).join(' '),
   over: b.scrollWidth > b.clientWidth + 1, docover: document.documentElement.scrollWidth > innerWidth + 1};
}"""
tools = sorted(glob.glob(os.path.join(OT, "5*.html")))
tools = [t for t in tools if not os.path.basename(t).endswith("Builder.html")]
with sync_playwright() as p:
    br = p.chromium.launch()
    for f in tools:
        name = os.path.basename(f); new = os.path.join(NT, name); lab = lab_of(name)
        if not os.path.exists(new): check(False, name, "patched tool missing"); continue
        o = open(f, encoding="utf-8").read(); n = open(new, encoding="utf-8").read()
        check(re.sub(r"<!-- (GS_BRIEF|WRONG_SIGNAL)[\s\S]*?<!-- /\1 -->\n?", "", n) == o, name, "file differs from the original outside the goals/scenario and wrong-signal blocks")
        pg = br.new_page(viewport={"width": 1366, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.abspath(new)); pg.wait_for_timeout(200)
        r = pg.evaluate(PROBE)
        check(not errs, name, f"JS errors: {errs[:1]}")
        if r is None: check(False, name, "no goals/scenario band (#labBrief)"); pg.close(); continue
        check(r["vis"] and r["top"] < 330, name, f"band is not at the top of the lab (y={r['top']:.0f})")
        check(r["before"] and r["top"] <= r["first"] + 1, name, "something sits above the band in the lab body")
        check([h["t"].upper() for h in r["heads"]] == ["GOALS", "SCENARIO"], name, f"headings: {[h['t'] for h in r['heads']]}")
        bg = rgb(r["bg"])
        for x in r["texts"]:
            check(x["w"] >= 600, name, f"not bold: {x['t'][:30]}")
            check(x["s"] >= 14, name, f"type under 14px: {x['t'][:30]}")
            check(ratio(rgb(x["c"]), bg) >= 7, name, f"contrast under 7:1: {x['t'][:30]}")
        for h in r["heads"]:
            check(ratio(rgb(h["c"]), rgb(h["bg"]) if "rgba(0, 0, 0, 0)" not in h["bg"] else bg) >= 4.5 and h["w"] >= 700, name, f"heading contrast/weight: {h['t']}")
        src = new_text.get(lab, "")
        check(len(r["goals"]) >= 3, name, f"only {len(r['goals'])} goals")
        for g in r["goals"]: check(norm(g) in src, name, f"goal not in handout: {g[:50]}")
        check(len(norm(r["scen"])) > 80 and norm(r["scen"]) in src, name, f"scenario not the handout's: {r['scen'][:50]}")
        pg.emulate_media(media="print")
        check(pg.evaluate("getComputedStyle(document.getElementById('labBrief')).display") == "none", name, "band prints")
        pg.emulate_media(media="screen"); pg.set_viewport_size({"width": 360, "height": 740}); pg.wait_for_timeout(50)
        r2 = pg.evaluate(PROBE)
        check(not r2["over"], name, "band overflows at 360px")
        pg.close()
    br.close()

print(f"{len(handouts)} handouts, {len(tools)} tools checked")
for x in fails[:60]: print("FAIL", x)
print("FAILURES", len(fails))
sys.exit(1 if fails else 0)
