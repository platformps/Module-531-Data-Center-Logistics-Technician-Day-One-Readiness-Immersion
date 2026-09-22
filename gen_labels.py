"""5_Instructor_ONLY/531_Bench_Labels.html — printable Code 128 cards and tags for the kit (Avery 5160 grid)."""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from spec import *
import barcode.charsets.code128 as c
OUT = os.environ["OUT"]
CODES = list(c.CODES) + [c.STOP + "11"]; B = c.B

def svg(text, h=44, w=2):
    vals = [104] + [B.get(ch, B[" "]) for ch in text]
    vals.append((vals[0] + sum(v*i for i, v in enumerate(vals) if i)) % 103)
    bits = "".join(CODES[v] for v in vals) + CODES[106]
    W = len(bits)*w + 12
    rects = "".join(f'<rect x="{6+i*w}" y="0" width="{w}" height="{h}"/>' for i, b in enumerate(bits) if b == "1")
    return f'<svg viewBox="0 0 {W} {h}" preserveAspectRatio="xMidYMid meet" fill="#000">{rects}</svg>'

def label(code, line1, line2=""):
    return f'<div class="lbl"><div class="t">{html.escape(line1)}</div>{svg(code)}<div class="c">{html.escape(code)}</div>' + (f'<div class="s">{html.escape(line2)}</div>' if line2 else "") + '</div>'

sections = []
sections.append(("§1 Station cards — one per bench", [label(f"STN-{i:02d}", "STATION CARD", f"Station {i}") for i in range(1, 11)]))
kit = []
for n in range(1,5): kit.append(label(f"KIT-R640-{n:02d}", "KIT CARD · blind", "R640 server (cover model name)"))
for n in range(1,5): kit.append(label(f"KIT-PSU-{n:02d}", "KIT CARD · blind", "hot-swap PSU"))
for n in range(1,5): kit.append(label(f"KIT-FAN-{n:02d}", "KIT CARD · blind", "fan module"))
for n in range(1,5): kit.append(label(f"KIT-DRV-{n:02d}", "KIT CARD · blind", "drive carrier"))
for n in range(1,3): kit.append(label(f"KIT-RAIL-{n:02d}", "KIT CARD · blind", "rail kit"))
for n in range(1,5): kit.append(label(f"KIT-CAGE-{n:02d}", "KIT CARD · blind", "cage nuts + blanking panel"))
for n in range(1,11): kit.append(label(f"KIT-SCAN-{n:02d}", "SCANNER", f"DS2208 · station {n}"))
for n in range(1,3): kit.append(label(f"KIT-CART-{n:02d}", "KIT CARD", f"platform cart {n}"))
sections.append(("§2 Kit cards — beside the item (fold the 'blind' cards so the second line is hidden for GLAB 531.1.1)", kit))
sections.append(("§3 Lifecycle cards — one set per station, shuffled", [label(code, "LIFECYCLE STAGE", st) for code, st in zip(LC_CODES, LC_STAGES)]))
sections.append(("§4 Bench register tags — apply to the real kit per the Kit Map §4 (upper-left, flat surface)", [label(t, "MODULE 531 · ASSET TAG", f"{i} · {l}") for t,i,m,l,s,cu in BENCH_REGISTER]))
sections.append(("§5 Drive tags — one per scrap drive (mock DBD)", [label(t, "DATA-BEARING DEVICE", "custody required · bag before moving") for t in DBD_TAGS]))
bins = [label("BIN-REDEPLOY","DISPOSITION BIN","Redeploy"), label("BIN-SCRAP","DISPOSITION BIN","Scrap"), label("BIN-DISPOSE","DISPOSITION BIN","Dispose")]
bins += [label(f"ITEM-RAIL-{n:02d}","SCRAP ACCESSORY","bent rail") for n in range(1,6)] + [label(f"ITEM-PANEL-{n:02d}","SCRAP ACCESSORY","damaged blanking panel") for n in range(1,6)]
sections.append(("§6 Bin cards and scrap-accessory cards — GLAB 531.5.2 (print three sets of the bin cards)", bins))
sections.append(("§7 Rack U labels — left rail of the PS mobile rack, one per U", [label(f"U-{u}", "RACK MIR-1", f"U{u}") for u in range(10, 31)]))
sections.append(("§8 Pick cards — inside the short bins for GLAB 531.3.2", [label("INC0701","PICK CARD","1 × issued"), label("INC0702","PICK CARD","1 × issued")]))
sections.append(("§9 Spare learner-issue labels — if a print station is down (GLAB 531.2.1 tags; 531.2.2 RMA labels; 531.4.1 path labels)", [label(f"ATL-0079{n}", "MODULE 531 · ASSET TAG", "issued by the lab tool") for n in range(0,3)] + [label(c,"RMA LABEL","authorization") for c in ("RMA-2026-08814","RMA-2026-08901","RMA-2026-08967")] + [label("CLM-2026-44172","PATH LABEL","claim authorization"), label("HOLD-DISPOSITION-REVIEW","PATH LABEL","no claim — hold")]))

CSS = """
body{font-family:Arial,sans-serif;margin:0;color:#111}
.intro{padding:24px 32px;max-width:900px}
.intro h1{font-size:20px;margin:0 0 6px}.intro p{font-size:13px;line-height:1.5}
.banner{border-left:6px solid #c05000;background:#fbf3ec;padding:10px 14px;font-size:13px;margin:12px 0}
h2.sec{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#0079C0;margin:0;padding:8px 0.19in 4px;page-break-before:always}
.grid{display:grid;grid-template-columns:repeat(3,2.625in);column-gap:0.125in;row-gap:0;padding:0 0.1875in}
.lbl{width:2.625in;height:1in;box-sizing:border-box;padding:0.05in 0.1in;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px dashed #bbb;overflow:hidden}
.lbl .t{font-size:7pt;letter-spacing:1px;color:#333;white-space:nowrap}
.lbl svg{width:2.3in;height:0.36in;margin:2px 0}
.lbl .c{font-family:Consolas,monospace;font-size:10.5pt;font-weight:700}
.lbl .s{font-size:7.5pt;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:2.4in}
@page{size:letter;margin:0.5in 0 0.5in 0}
@media print{.intro{display:none}.lbl{border-color:transparent}h2.sec{color:#999;font-size:9px;padding-top:0}}
"""
parts = [f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>Module 531 — Bench label sheet (instructor only)</title><style>{CSS}</style></head><body>",
         "<div class='intro'><h1>Module 531 — Bench label sheet</h1><div class='banner'><b>Instructor document. Do not issue to learners.</b> The codes here are the bench seeds and register; a learner who has this sheet has the bench key.</div>",
         f"<p>Version {VERSION} · {VDATE}. Print on Avery 5160-format sheets (30 labels, 2.625 × 1 in) with browser scaling at 100% and margins as set by the page; each section starts on a new sheet. Plain paper works for cards (cut on the dashed lines). Tags that go on kit (§4, §5) are best printed on the tamper-evident asset tag stock or on the Zebra ZD621 — any lab tool's Print label button prints one code at a time on the ZD621 if you prefer that route. Every code is Code 128; the DS2208 reads them at 2 in or more. Test one label with a scanner into a text box before printing the rest.</p>",
         "<p>Sections: " + " · ".join(html.escape(s[0].split(" — ")[0]) for s in sections) + "</p></div>"]
for title, labels in sections:
    parts.append(f"<h2 class='sec'>{html.escape(title)}</h2><div class='grid'>{''.join(labels)}</div>")
parts.append("</body></html>")
open(os.path.join(OUT, "5_Instructor_ONLY", "531_Bench_Labels.html"), "w", encoding="utf-8").write("".join(parts))
print("labels", sum(len(s[1]) for s in sections))
