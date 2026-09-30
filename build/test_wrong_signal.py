"""Check for the wrong-answer signal (v2.5). Fails non-zero.

    python3 test_wrong_signal.py ORIG_TOOLS NEW_TOOLS

A tool that already checks an answer shows a big WRONG with the tool's own reason and plays a short buzzer when
the check fails, and the reason is a full sentence that says why; an incomplete record is not called wrong; Sound off silences it and is remembered; nothing shows
on load or in print; every file is byte-identical to the original outside the WRONG_SIGNAL block, and tools that
check no answers are untouched. Needs playwright (Chromium).
"""
import glob, os, re, sys
from playwright.sync_api import sync_playwright

OT, NT = sys.argv[1:3]
fails = []
def check(ok, where, what):
    if not ok: fails.append(f"{where}: {what}")

TARGET = re.compile(r"^(531-\d-\d|524-2-1)")
STUB = """window.__osc=0;window.AudioContext=window.webkitAudioContext=function(){this.currentTime=0;this.destination={};this.resume=function(){};
this.createOscillator=function(){return{type:'',frequency:{value:0},connect:function(){},start:function(){window.__osc++},stop:function(){}}};
this.createGain=function(){return{gain:{value:0},connect:function(){}}}};"""
STATE = """()=>{const b=document.getElementById('wrongBox');if(!b)return null;const h=b.querySelector('.wbig'),r=b.querySelector('.wwhy'),cs=getComputedStyle;
 return{shown:cs(b).display!=='none',role:b.getAttribute('role'),big:h?h.textContent.trim():'',size:h?parseFloat(cs(h).fontSize):0,weight:h?+cs(h).fontWeight:0,
 why:r?r.textContent.trim():'',lab:(b.querySelector('.wwhy b')||{}).textContent||'',where:(b.querySelector('.wwhere')||{}).textContent||'',fg:h?cs(h).color:'',bg:cs(b).backgroundColor,osc:window.__osc}}"""
def lum(c):
    v = [int(x) / 255 for x in re.findall(r"\d+", c)[:3]]; v = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in v]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]
def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + .05) / (y + .05)

def wrong_move(pg, name):
    """Make one wrong entry the tool itself rejects; returns the word its reason must contain, or None if the tool checks nothing."""
    if name.startswith("524-2-1"):
        pg.click('g.nd[data-id="MB-A"]'); pg.wait_for_timeout(120)             # first click only opens the legend: not a wrong answer
        st = pg.evaluate(STATE); check(not st["shown"], name, "WRONG shown for 'open the legend first' (a prompt, not a wrong answer)")
        pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(/Close legend|Close packet/.test(b.textContent)&&b.offsetParent)b.click()})")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(80)
        pg.evaluate("document.querySelector('g.nd[data-id=\"MB-A\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        return r"source"
    if name.startswith("531-1-3"): return None                                  # walkdown: nothing is checked against a code
    if name.startswith("531-2-2"):
        pg.get_by_role("button", name=re.compile("Submit RMA request")).first.click(); return r"rejected"
    if name.startswith("531-3-2"):
        for _ in range(2): pg.click("#b_cnt"); pg.keyboard.type("ATL-00911"); pg.keyboard.press("Enter"); pg.wait_for_timeout(60)
        return r"already in the list"
    fid = pg.evaluate("document.querySelector('#benchPanel input.scanin').id")
    pg.click("#" + fid); pg.keyboard.type("ZZZ-999"); pg.keyboard.press("Enter")
    return r"expects|not in the bench register"

files = sorted(f for f in glob.glob(os.path.join(OT, "5*.html")) if not f.endswith("Builder.html"))
n_target = 0
with sync_playwright() as p:
    br = p.chromium.launch()
    for f in files:
        name = os.path.basename(f); new = os.path.join(NT, name)
        o = open(f, encoding="utf-8").read(); n = open(new, encoding="utf-8").read()
        stripped = re.sub(r"<!-- WRONG_SIGNAL[\s\S]*?<!-- /WRONG_SIGNAL -->\n?", "", n)
        check(stripped == o, name, "file differs from the original outside the WRONG_SIGNAL block")
        if not TARGET.match(name):
            check(n == o, name, "a tool that checks no answers was changed"); continue
        n_target += 1
        ctx = br.new_context(viewport={"width": 1366, "height": 900}); ctx.add_init_script(STUB)
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.abspath(new)); pg.wait_for_timeout(250)
        st = pg.evaluate(STATE)
        if st is None: check(False, name, "no wrong-answer signal (#wrongBox)"); ctx.close(); continue
        check(not st["shown"] and st["osc"] == 0, name, "signal fired on load")
        check(st["role"] == "alert", name, "box is not role=alert")
        if name.startswith("531"):                                              # an incomplete record is not a wrong answer
            pg.locator("#benchPanel button.primary").first.click(); pg.wait_for_timeout(200); st = pg.evaluate(STATE)
            check(not st["shown"] and st["osc"] == 0, name, "WRONG shown for an incomplete bench record")
        want = wrong_move(pg, name); pg.wait_for_timeout(200); st = pg.evaluate(STATE)
        if want is None:
            check(not st["shown"], name, "WRONG shown in a tool that checks nothing")
        else:
            check(st["shown"], name, "wrong answer did not show WRONG")
            check(st["big"] == "WRONG" and st["size"] >= 56 and st["weight"] >= 800, name, f"not big letters: {st['big']!r} {st['size']}px/{st['weight']}")
            check(st["lab"].strip() == "Why:" and re.search(want, st["why"]) is not None, name, f"no plain reason why: {st['why'][:70]!r}")
            check(len(st["why"]) >= 45 and not re.search(r"CHECK —|SCAN FAIL", st["why"]), name, f"reason is the raw status, not an explanation: {st['why'][:70]!r}")
            if name.startswith("531"): check(len(st["where"]) > 8, name, "box does not say which field or panel the answer was in")
            check(ratio(st["fg"], st["bg"]) >= 4.5, name, "WRONG contrast under 4.5:1")
            check(st["osc"] == 1, name, f"buzzer count {st['osc']} (expected 1)")
            pg.emulate_media(media="print")
            check(pg.evaluate("getComputedStyle(document.getElementById('wrongBox')).display=='none' && getComputedStyle(document.getElementById('wrongSound')).display=='none'"), name, "signal prints")
            pg.emulate_media(media="screen")
            # Sound off: still shows, no buzzer, remembered after a reload; nothing fires on load even with the wrong entry saved
            pg.click("#wrongBox"); pg.wait_for_timeout(150); st = pg.evaluate(STATE)          # clicking away re-checks the field: same answer, no second WRONG
            check(not st["shown"] and st["osc"] == 1, name, f"clicking away: shown={st['shown']} buzzer={st['osc']}")
            if name.startswith("524-2-1"): pg.evaluate("document.querySelector('g.nd[data-id=\"MB-A\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
            else: wrong_move(pg, name)
            pg.wait_for_timeout(200); st = pg.evaluate(STATE)
            again = 3 if name.startswith("531-3-2") else 2                          # the count lab's second try is two duplicate scans
            check(st["shown"] and st["osc"] == again, name, f"a second wrong answer: shown={st['shown']} buzzer={st['osc']}")
            pg.click("#wrongBox"); pg.wait_for_timeout(100)
            pg.click("#wrongSound"); check("off" in pg.inner_text("#wrongSound").lower(), name, "Sound switch does not read off")
            pg.reload(); pg.wait_for_timeout(250); st = pg.evaluate(STATE)
            check(not st["shown"] and st["osc"] == 0, name, "signal fired on reload")
            check("off" in pg.inner_text("#wrongSound").lower(), name, "Sound off not remembered")
            wrong_move(pg, name); pg.wait_for_timeout(200); st = pg.evaluate(STATE)
            check(st["shown"] and st["osc"] == 0, name, f"Sound off: shown={st['shown']} buzzer={st['osc']}")
            pg.click("#wrongBox")
        check(not errs, name, f"JS errors: {errs[:1]}")
        ctx.close()
    # every rejection the tools can produce gets a full-sentence reason; reminders and incomplete records stay quiet
    WRONGS = ["CHECK — 'ZZZ-999' is not the code this field expects — scan the card or tag named in the label, not another one", "CHECK — read ZZZ-999, expected ATL-00790",
              "CHECK — not in the bench register (ATL-009xx tags only)", "CHECK — 'DBD-01' is already recorded in another row", "CHECK — bin BIN-SCRAP does not match the path Dispose",
              "SCAN FAIL — check: serial, model", "SCAN FAIL — tag matches plate but the placement violates the standard", "Out of order at position 3 — restart the sequence.",
              "ATL-00911 is already in the list — duplicate scan rejected.", "No record with that tag.", "Tag already exists.",
              "No entitlement found for “X1”. Type the serial exactly as it is printed on the ticket.", "The vendor portal rejected the claim: no active entitlement on this serial.",
              "Vendor portal rejected the request: the fault documentation must quote the fault code logged on the ticket (PSU0002)."]
    QUIET = ["All fields are required.", "Compare all three fields first.", "Classify all three first.", "Scan every item before locking.", "Count is locked — press Restart count to count again.",
             "3 bin(s) uncounted.", "Look up the entitlement first.", "Location, status and custody are all part of a move.", "EXPIRED", "check", "not green"]
    ctx = br.new_context(); ctx.add_init_script(STUB); pg = ctx.new_page()
    pg.goto("file://" + os.path.abspath(os.path.join(NT, "531-0-1_PlatformCheck.html")) if os.path.exists(os.path.join(NT, "531-0-1_PlatformCheck.html")) else "about:blank"); pg.wait_for_timeout(250)
    if pg.evaluate(STATE) is not None:
        pg.evaluate("(()=>{const d=document.createElement('div');d.id='probe';document.body.appendChild(d)})()")
        for m, wrong in [(x, True) for x in WRONGS] + [(x, False) for x in QUIET]:
            pg.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'a',bubbles:true}))"); pg.wait_for_timeout(15)
            pg.evaluate("(m)=>{const s=document.createElement('span');s.className='badmark';s.textContent=m;const d=document.getElementById('probe');d.innerHTML='';d.appendChild(s)}", m)
            pg.wait_for_timeout(40); st = pg.evaluate(STATE)
            if not wrong: check(not st["shown"], "messages", f"WRONG shown for a reminder: {m!r}")
            else:
                w = st["why"].replace("Why:", "").strip()
                check(st["shown"], "messages", f"no WRONG for: {m!r}")
                check(len(w) >= 45 and w.endswith(".") and not re.search(r"CHECK —|SCAN FAIL", w), "messages", f"thin reason for {m[:40]!r}: {w!r}")
    ctx.close()
    # the box stays until the learner acts, so the reason gets read, then clears on the next click or key
    t = [f for f in files if TARGET.match(os.path.basename(f)) and "531-0-1" in f or "524-2-1-A" in f]
    for f in t:
        name = os.path.basename(f); ctx = br.new_context(); ctx.add_init_script(STUB); pg = ctx.new_page()
        pg.goto("file://" + os.path.abspath(os.path.join(NT, name))); pg.wait_for_timeout(250)
        if pg.evaluate(STATE) is not None:
            wrong_move(pg, name); pg.wait_for_timeout(7000)
            check(pg.evaluate(STATE)["shown"], name, "box vanished before the learner did anything")
            pg.keyboard.press("Shift"); pg.wait_for_timeout(80)
            check(not pg.evaluate(STATE)["shown"], name, "box still up after the next key")
        ctx.close()
    br.close()

print(f"{len(files)} tools compared, {n_target} with checked answers exercised")
for x in fails[:40]: print("FAIL", x)
print("FAILURES", len(fails))
sys.exit(1 if fails else 0)
