"""v2.4 — goals and scenario lead every lab (Module 524 and Module 531).

    python3 goals_scenario_patch.py HANDOUTS_DIR TOOLS_DIR

Patches both folders in place and can be re-run at any time (after a regeneration, after the readability
patch): a second run changes nothing.

Handouts (*_GLAB_*.docx): the Learning Objectives section and the scenario paragraph move to the top of the
document, under the title block, in bold on a shaded block between two rules. "Scenario and Instructions"
becomes "Scenario" (top) and "Instructions" (where it was). Tracked changes are accepted, so the handout is
clean. The only wording that changes is the Module 531 bench goal, restated for the virtual bench (VIRTUAL_BENCH
below — the same text as BENCH_OBJECTIVE in gen_handouts.py); everything else is moved, never rewritten.

Lab tools (5xx-m-i[-S]_*.html): a Goals + Scenario band is inserted above the "How to work this lab" card,
bold white on navy. Its wording is read from the lab's handout, so the handout stays the single source — edit
the handout, re-run this script. The band sits between GS_BRIEF markers; everything outside them is untouched.
It does not print, so the submission PDF is unchanged.

Needs python-docx.
"""
import copy, glob, html, os, re, sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

FILL, RULE = "EAF2F8", "0079C0"          # the packages' table-header tint and heading blue

def W(tag): return qn("w:" + tag)
def text(el): return "".join(t.text or "" for t in el.iter(W("t")))           # w:t only: tracked deletions (w:delText) stay out
def style(el):
    ps = el.find(W("pPr") + "/" + W("pStyle"))
    return ps.get(W("val")) if ps is not None else ""
def is_heading(el): return el.tag == W("p") and style(el).lower().replace(" ", "").startswith(("heading", "title"))
def is_bullet(el): return el.find(W("pPr") + "/" + W("numPr")) is not None

def _ppr(p):
    pPr = p.find(W("pPr"))
    if pPr is None: pPr = OxmlElement("w:pPr"); p.insert(0, pPr)
    return pPr

def _put(pPr, el):
    """Insert a pPr child where the schema wants it (Word rejects out-of-order pPr children)."""
    order = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr", "suppressLineNumbers",
             "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
             "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents",
             "suppressOverlap", "jc", "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle",
             "rPr", "sectPr", "pPrChange"]
    name = el.tag.split("}")[1]
    for old in pPr.findall(el.tag): pPr.remove(old)
    for c in pPr:
        if order.index(c.tag.split("}")[1]) > order.index(name): c.addprevious(el); return
    pPr.append(el)

def emphasize(p, first=False, last=False):
    """Bold text on the shaded block; a rule above the first paragraph and below the last."""
    pPr = _ppr(p)
    shd = OxmlElement("w:shd"); shd.set(W("val"), "clear"); shd.set(W("color"), "auto"); shd.set(W("fill"), FILL); _put(pPr, shd)
    if first or last:
        bdr = OxmlElement("w:pBdr")
        e = OxmlElement("w:top" if first else "w:bottom")
        for k, v in (("val", "single"), ("sz", "18"), ("space", "6"), ("color", RULE)): e.set(W(k), v)
        bdr.append(e); _put(pPr, bdr)
    if is_bullet(p):                       # bullets start at the margin so the block has one straight left edge
        ind = OxmlElement("w:ind"); ind.set(W("left"), "360"); ind.set(W("hanging"), "360"); _put(pPr, ind)
    for r in p.iter(W("r")):
        rPr = r.find(W("rPr"))
        if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
        for tag in ("b", "bCs"):
            for old in rPr.findall(W(tag)): rPr.remove(old)
        b = OxmlElement("w:b")
        lead = [c for c in rPr if c.tag in (W("rStyle"), W("rFonts"))]             # w:b follows rStyle/rFonts
        lead[-1].addnext(b) if lead else rPr.insert(0, b)

DOUBLED = re.compile(r"(?P<s>[A-Z][^.!?]{12,}[.!?])\s+(?P=s)")

def accept_tracked(body):
    """Accept every tracked change: insertions stay, deletions go, the revision marks disappear."""
    for el in list(body.iter(W("del"))):
        el.getparent().remove(el)
    for el in list(body.iter(W("ins"))):
        par = el.getparent()
        if par.tag in (W("rPr"), W("trPr")): par.remove(el); continue        # inserted paragraph mark / table row
        for kid in list(el): el.addprevious(kid)
        par.remove(el)
    for p in body.iter(W("p")):                # an accepted edit can leave a sentence twice in a row: keep one
        m = DOUBLED.search(text(p))
        while m:
            a, b, pos = m.end("s"), m.end(), 0
            for t in p.iter(W("t")):
                n = len(t.text or "")
                lo, hi = max(a, pos), min(b, pos + n)
                if lo < hi: t.text = t.text[:lo - pos] + t.text[hi - pos:]; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                pos += n
            m = DOUBLED.search(text(p))

# Module 531 bench goals, restated for the virtual bench (stations have no printer and no physical kit).
# old wording -> new wording; GLAB 531.1.3 keeps its walkdown goal, which is still done at the station.
VIRTUAL_BENCH = {
 "Prove the station works: scan a station card and a scanner card into the lab tool and confirm the ESD kit is present and connected.":
 "Prove the station works: scan the station card and the scanner card on the virtual bench into the lab tool and complete the ESD kit check.",
 "Identify real kit items by sight, function and handling requirement at the kit station, scanning each blind card into the tool; then sequence the lifecycle with physical stage cards and map three stages to the kit item each one reaches for first.":
 "Identify kit items by function and handling requirement on the virtual bench, scanning each kit card into the tool; then sequence the lifecycle by scanning the eight stage cards in order and map three stages to the kit item each one reaches for first.",
 "Execute three physical hand-offs of a bagged drive with a complete logbook line at each transfer, mirrored into the tool.":
 "Execute three hand-offs of a bagged drive with your partner on the virtual bench, with a complete custody line at each transfer: drive tag scanned, date and time, from, to, condition and both initials.",
 "Receive a real carton: weigh it against the ASN, verify contents, print the issued asset tag on the label printer, place it per the standard and scan it back.":
 "On the virtual bench, receive a carton: check its scale reading against the ASN, verify the contents, print the issued asset tag with Print label, place it per the standard and scan it back.",
 "Pack a failed FRU for return under ESD protection, seal it in a serialized security bag with the serial scanned at sealing, and label the carton with the printed RMA authorization.":
 "On the virtual bench, pack a failed FRU for return: ESD protection confirmed, the security-bag serial scanned at the moment of sealing, the RMA label printed and scanned back, and the logbook line complete with both initials.",
 "Find real kit items by scanning their tags against the bench register and record a physical move at the cart, not the desk.":
 "Look up three tagged items by scanning their tags from the virtual bench against the bench register, and record one move by scanning the item at the cart and setting its new location, status and custody.",
 "Perform a physical blind count of a station bin by scanning every tag, lock it, and reconcile against the register quantity.":
 "Perform a blind count of a bin on the virtual bench by scanning every tag, lock it, and reconcile against the register quantity.",
 "Read the R640 service tag from the chassis, pack the unit for its path and label it with the printed claim or hold label.":
 "Read the R640's asset tag and Dell service tag from the virtual bench, confirm ESD protection and bagging, then print the claim or hold label for its path and scan it back.",
 "Rack a real R640 into the mobile rack with rails, cage nuts and a team lift, dress it, and record the move at the rack.":
 "On the virtual bench, record the rack-and-stack move: scan the unit's asset tag, the rail-kit card and the U-position label, confirm each racking check in order, and log your team-lift partner's initials.",
 "Census real drives, double-bag each one in a serialized security bag with the serial scanned at sealing, and log every bag.":
 "Census the drives in the chassis on the virtual bench, bag each one in a serialized security bag with the serial scanned at sealing, and log every bag with both initials.",
 "Sort real end-of-life items into disposition bins by scan, witness a destruction hand-over and complete the hand-over line.":
 "Sort three end-of-life items into disposition bins by scan on the virtual bench, witness the destruction hand-over and complete the hand-over line.",
}

def reword(p):
    new = VIRTUAL_BENCH.get(text(p).strip())
    if new:
        ts = list(p.iter(W("t"))); ts[0].text = new
        for t in ts[1:]: t.text = ""

def patch_handout(path):
    """Returns the brief {'lead': [...], 'goals': [...], 'scenario': str} read from the handout, restructuring it if needed."""
    d = Document(path); body = d.element.body
    accept_tracked(body)
    kids = [k for k in body if k.tag == W("p")]
    def find(name): return next((k for k in kids if is_heading(k) and text(k).strip() == name), None)
    lo, intro = find("Learning Objectives"), find("Introduction")
    sc = find("Scenario")
    if sc is None: sc = find("Scenario and Instructions")
    assert lo is not None and intro is not None and sc is not None, (path, "template headings not found")
    def block(h):                           # the paragraphs under a heading, up to the next heading
        out = []; k = h.getnext()
        while k is not None and not is_heading(k) and k.tag == W("p"):
            out.append(k); k = k.getnext()
        return out
    goals_block = [k for k in block(lo) if text(k).strip()]
    for k in goals_block: reword(k)
    if text(sc).strip() == "Scenario and Instructions":          # first run: split the heading, move both blocks up
        scen = next(k for k in block(sc) if text(k).strip())
        head = copy.deepcopy(lo)
        ts = list(head.iter(W("t"))); ts[0].text = "Scenario"
        for t in ts[1:]: t.text = ""
        for t in list(sc.iter(W("t")))[:1]: t.text = "Instructions"
        for t in list(sc.iter(W("t")))[1:]: t.text = ""
        for el in [lo] + block(lo) + [head, scen]: intro.addprevious(el)
    else:
        head = sc; scen = next(k for k in block(sc) if text(k).strip())
    top = [lo] + [k for k in block(lo)] + [head, scen]
    for i, el in enumerate(top): emphasize(el, first=(i == 0), last=(i == len(top) - 1))
    d.save(path)
    return {"lead": [text(k).strip() for k in goals_block if not is_bullet(k)],
            "goals": [text(k).strip() for k in goals_block if is_bullet(k)],
            "scenario": text(scen).strip()}

CSS = """<style id="gsBriefCss">
/* v2.4 — goals and scenario lead the lab: bold white on navy, above everything else */
#labBrief{background:#0b3d61;color:#fff;border-radius:9px;padding:16px 20px 18px;margin:0 0 18px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:14px 32px;font-size:15px;line-height:1.5;text-align:left}
#labBrief h2{display:inline-block;margin:0 0 8px;padding:2px 10px;border:0;border-radius:4px;background:#fff;color:#0b3d61;font-size:13px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase}
#labBrief p,#labBrief li{margin:0 0 6px;color:#fff;font-size:15px;font-weight:700;overflow-wrap:anywhere}
#labBrief ul{margin:0;padding:0 0 0 20px;list-style:disc}
#labBrief li::marker{color:#fff}
#labBrief p:last-child,#labBrief li:last-child{margin-bottom:0}
@media print{#labBrief{display:none}}
</style>"""
BLOCK = re.compile(r"<!-- GS_BRIEF[\s\S]*?<!-- /GS_BRIEF -->\n?")
ANCHOR = '<details class="labguide" id="labGuide"'

def brief_html(b):
    e = lambda s: html.escape(s, quote=False)
    lead = "".join(f"<p>{e(t)}</p>" for t in b["lead"])
    goals = "".join(f"<li>{e(t)}</li>" for t in b["goals"])
    return ("<!-- GS_BRIEF v2.4: goals and scenario from the lab handout; rebuilt by goals_scenario_patch.py -->\n" + CSS +
            '\n<section id="labBrief" aria-label="Goals and scenario for this lab">'
            f'<div class="lbgoals"><h2>Goals</h2>{lead}<ul>{goals}</ul></div>'
            f'<div class="lbscen"><h2>Scenario</h2><p>{e(b["scenario"])}</p></div></section>\n<!-- /GS_BRIEF -->\n')

def patch_tool(path, b):
    t = BLOCK.sub("", open(path, encoding="utf-8").read())
    assert t.count(ANCHOR) == 1, (path, "guide card anchor not found — run the readability patch first")
    open(path, "w", encoding="utf-8").write(t.replace(ANCHOR, brief_html(b) + ANCHOR))

def main(handouts, tools):
    briefs = {}
    for f in sorted(glob.glob(os.path.join(handouts, "*_GLAB_*.docx"))):
        briefs[re.match(r"\d{3}-\d-\d", os.path.basename(f)).group(0)] = patch_handout(f)
    n = 0
    for f in sorted(glob.glob(os.path.join(tools, "5*.html"))):
        m = re.match(r"(\d{3}-\d-\d)[-_]", os.path.basename(f))
        if not m or ANCHOR not in open(f, encoding="utf-8").read(): continue      # builder, index: not labs
        assert m.group(1) in briefs, (f, "no handout for this lab")
        patch_tool(f, briefs[m.group(1)]); n += 1
    print(f"{len(briefs)} handouts, {n} tools patched")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
