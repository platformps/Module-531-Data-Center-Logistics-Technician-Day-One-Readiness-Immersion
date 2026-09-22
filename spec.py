# Module 531 v2.1 — bench spec. Single source for: bench panels in the lab tools, bench parts in the
# handouts, bench keys in the FT builds, kit map, guide run sheets, rubric bench criteria.
VERSION = "2.1"
VDATE = "22 September 2026"
COURSE = "Module 531: Data Center Logistics Technician Day-One Readiness Immersion"

# ---------------------------------------------------------------- the kit (D13 procurement list v1.2)
KIT = [
 # id, item, qty, source, used in labs
 ("SCAN",  "Zebra DS2208 handheld barcode scanner (USB, keyboard-wedge)", "10", "Purchase", "every lab"),
 ("PRN",   "Zebra ZD621 desktop label printer + thermal label rolls (4/cohort) + tamper-evident asset tag rolls (2/cohort)", "2", "Microsoft (printer, tag rolls) / purchase (thermal rolls)", "0.1 · 2.1 · 2.2 · 4.1 · label sheet"),
 ("ESD",   "ESD anti-static mat + wrist-strap kit", "10", "Microsoft", "1.3 · 2.1 · 2.2 · 3.1 · 4.1 · 4.2 · 5.1 · 5.2"),
 ("R640",  "Refurbished Dell PowerEdge R640 1U server", "4", "Purchase", "1.1 · 3.1 · 3.2 · 4.1 · 4.2 · 5.1"),
 ("FRU",   "R640 field-replaceable-unit set (hot-swap PSU, fan module, 2.5-in drive carrier with drive)", "4", "Purchase", "1.1 · 2.1 · 2.2 · 3.1 · 3.2 · 4.1"),
 ("RACK",  "Rack accessories lot (cage nuts, blanking panels, cable management, rail kits) supplementing the PS mobile rack", "1 lot", "Purchase", "1.1 · 4.2 · 5.2"),
 ("CART",  "Mobile platform cart / hand truck", "2", "Purchase", "1.1 · 1.3 · 3.1 · 4.2"),
 ("RCV",   "Mock receiving props: pallet + bin (Microsoft), bench scale (purchase)", "1 each", "Microsoft / purchase", "1.3 · 2.1 · 3.2"),
 ("PPE",   "Reusable PPE set: hi-vis vest (Microsoft), hard hat, safety glasses (purchase); nitrile gloves per learner", "24 sets · 20 gloves", "Microsoft / purchase", "1.3 · SBA (in 4.2) · 4.2 · 5.1"),
 ("PKG",   "Mock packaging/shipping kit: boxes, tape, printed PO/ASN (purchase); shrink wrap (Microsoft)", "1 kit/cohort", "Purchase / Microsoft", "2.1 · 2.2 · 4.1"),
 ("HDD",   "Scrap / decommissioned hard drives (mock DBDs)", "30/cohort", "PS / Microsoft e-waste", "1.2 · 1.3 · 3.2 · 5.1 · 5.2"),
 ("ASB",   "Anti-static shielding bags, assorted", "2 packs (100)", "Microsoft", "1.2 · 2.2 · 4.1 · 5.1"),
 ("SEC",   "Serial-numbered tamper-evident security bags", "50/cohort (34 used)", "Microsoft", "2.2 · 5.1 · 5.2"),
 ("COC",   "Mock chain-of-custody logbooks + templates (class set)", "1 set", "Microsoft", "1.2 · 2.2 · 5.1"),
 ("SW",    "Snipe-IT / openDCIM (PS self-hosted) — optional live demonstration only; the lab tools carry the DCIM of record", "—", "Open source", "3.1 demo"),
]

STATIONS = 10          # lab stations (D13 assumption)
DRIVES   = 30          # scrap drives tagged DBD-01..30: 5.1 needs 2 per station + 3 seeded extras (23); 3.2 bins draw on the same pool
SEC_USED = STATIONS*2 + 3 + STATIONS + 1   # 5.1 (two per station + three extras) + 2.2 (one per station) + the 5.2 vendor transfer bag = 34 of 50
COHORT   = "15–20"     # learners; pairs at stations

# Barcode namespaces printed from 5_Instructor_ONLY/531_Bench_Labels.html
# STN-01..10 station cards · KIT-<type>-<nn> kit item cards · LC-<stage> lifecycle cards ·
# BIN-<path> disposition bins · ATL-009xx bench asset tags · DBD-01..20 drive tags · INC-<n> pick cards
BENCH_REGISTER = [
 # tag, item, model, location, status, custody
 ("ATL-00901","R640 server 1","Dell PowerEdge R640","MIR-1 U10-U11","Deployed","DC Hall"),
 ("ATL-00902","R640 server 2","Dell PowerEdge R640","MIR-1 U14-U15","Deployed","DC Hall"),
 ("ATL-00903","R640 server 3","Dell PowerEdge R640","STAGE-1 (cart)","Staged","Store House"),
 ("ATL-00904","R640 server 4","Dell PowerEdge R640","SH-A-01","In stock","Store House"),
 ("ATL-00911","PSU FRU 1","R640 hot-swap PSU 750 W","SH-B-01","In stock","Store House"),
 ("ATL-00912","PSU FRU 2","R640 hot-swap PSU 750 W","SH-B-01","In stock","Store House"),
 ("ATL-00913","PSU FRU 3","R640 hot-swap PSU 750 W","SH-B-02","In stock","Store House"),
 ("ATL-00914","PSU FRU 4","R640 hot-swap PSU 750 W","SH-B-02","In stock","Store House"),
 ("ATL-00921","Fan module FRU 1","R640 fan module","SH-B-03","In stock","Store House"),
 ("ATL-00922","Fan module FRU 2","R640 fan module","SH-B-03","In stock","Store House"),
 ("ATL-00923","Fan module FRU 3","R640 fan module","SH-B-04","In stock","Store House"),
 ("ATL-00924","Fan module FRU 4","R640 fan module","SH-B-04","In stock","Store House"),
 ("ATL-00931","Rail kit 1","R640 sliding rail kit","SH-C-01","In stock","Store House"),
 ("ATL-00932","Rail kit 2","R640 sliding rail kit","SH-C-01","In stock","Store House"),
 ("ATL-00941","Platform cart 1","Mobile platform cart","Dock","In service","Receiving"),
 ("ATL-00942","Platform cart 2","Mobile platform cart","Store House aisle","In service","Store House"),
 ("ATL-00951","Bench scale","Receiving bench scale","Receiving","In service","Receiving"),
]
DBD_TAGS = ["DBD-%02d"%i for i in range(1,DRIVES+1)]

KIT_CARDS = [  # blind hardware-ID cards: code, what it is laid beside, classification key, handling key
 ("KIT-R640-01","R640 server (chassis, bezel off)","Rack server (1U)","Team lift"),
 ("KIT-PSU-01","R640 hot-swap PSU","PSU FRU","ESD precautions"),
 ("KIT-FAN-01","R640 fan module","Fan module FRU","ESD precautions"),
 ("KIT-DRV-01","2.5-in drive carrier with drive","Drive carrier (DBD)","DBD custody"),
 ("KIT-RAIL-01","Sliding rail kit","Rail kit","Standard handling"),
 ("KIT-CAGE-01","Cage nuts + blanking panel","Rack accessory","Standard handling"),
 ("KIT-SCAN-01","DS2208 scanner","Scanner (tool)","Standard handling"),
 ("KIT-CART-01","Platform cart","Material-handling equipment","Standard handling"),
]
# the eight stages exactly as the Lesson 531.1 lifecycle-rail slide names them (the slide is the answer sheet for the bench walk)
LC_STAGES = ["Receive","Tag & record","Store","Stage & kit","Deploy (hand-off)","Operate & support","RMA / repair","Decommission & dispose"]
LC_CODES  = ["LC-RECEIVE","LC-TAG","LC-STORE","LC-STAGE","LC-DEPLOY","LC-OPERATE","LC-RMA","LC-DECOM"]

# ---------------------------------------------------------------- per-lab bench design
# Each lab: minutes (new total), bench_min, part (handout part title), intro (handout paragraph),
# steps (list): {"t": text, "cap": "rec" | "text" | "image"}  — "rec" = recorded in the tool,
#   "text"/"image" = a numbered question appended to the tool's question registry (lockstep).
# fields: bench panel fields (id, type, label, hint, expect, opts, n)
#   types: scan (regex expect or 'ATL' issued id), check, sel, text, num, seq (ordered scan list), rows (group x n)
# kit: kit ids used. Answer keys, station seeds and rubric text live in the instructor-only spec_keys.py (merged at build time).
LABS = {}
import os as _os
# v2.1: new id -> id in the source package, only while the source is the v2.0 layout (Hazard Walkdown renumbered)
SRC_ID = {"1-3": "1-4"} if _os.path.exists(_os.path.join(_os.environ.get("SRC", ""), "4_Lab_Tools", "531-1-4-A_HazardWalk.html")) else {}

LABS["0-1"] = dict(
 minutes=25, bench_min=5, kit=["SCAN","ESD","PRN"],
 part="Part 3: Station check-in (at the bench)",
 intro="The four platforms are the doors; the bench is where the work happens. Before any technical lab, prove the station works: the scanner reads into the tool, the ESD kit is present and connected, and you know your station number. Everything you scan this week lands in a tool field exactly as if you had typed it — the scanner is a keyboard.",
 steps=[
  {"t":"Step 9. At your station, click into the Station card field in the bench panel and scan the STN card taped to the bench. The scanner sends the code and an Enter; the tool checks the format.","cap":"rec"},
  {"t":"Step 10. Scan the KIT-SCAN card on your scanner's holster, then confirm the ESD kit: mat on the bench, ground cord connected, wrist strap present. Tick each item only after you have touched it.","cap":"rec"},
  {"t":"Step 11. One sentence: what is different between a scanned value and a typed one, from the point of view of the record that ends up in the system?","cap":"text"},
 ],
 fields=[
  {"id":"stn","type":"scan","label":"Station card — scan the STN card on your bench","expect":r"^STN-(0[1-9]|10)$","hint":"Click here, then scan."},
  {"id":"scn","type":"scan","label":"Scanner card — scan the KIT-SCAN card on the holster","expect":r"^KIT-SCAN-\d{2}$"},
  {"id":"esd1","type":"check","label":"ESD mat on the bench, ground cord connected"},
  {"id":"esd2","type":"check","label":"Wrist strap present and clips to the mat"},
  {"id":"kitok","type":"sel","label":"Station kit complete?","opts":["Yes — nothing missing","No — flagged to instructor"]},
 ],
)

LABS["1-1"] = dict(
 minutes=35, bench_min=15, kit=["R640","FRU","RACK","SCAN","CART"],
 part="Part 4: The kit identification station and the lifecycle walk (at the bench)",
 intro="The cards in the tool are descriptions. The bench is the metal. Eight kit items are laid out with their model names covered and a blind barcode card beside each one. Identify by sight, function and handling requirement — the same three judgements, now with your hands on the item. Then put the asset lifecycle in order with the eight stage cards at your station, and walk three of the stages to the kit item you would reach for first.",
 steps=[
  {"t":"Step 9. At the kit station, scan each blind card into the bench panel in any order, then classify the item beside it and set its handling requirement. Pick the item up (with a partner where its size demands it) before you decide — weight and connectors are evidence.","cap":"rec"},
  {"t":"Step 10. One of the eight items is the only one you would refuse to lift alone. Name it, quote the plate weight or the reason, and state the rule.","cap":"text"},
  {"t":"Step 11. Two of the items are ESD-sensitive and one is a data-bearing device. Name the DBD and say what changes the moment you pick it up compared with the PSU beside it.","cap":"text"},
  {"t":"Step 12. Put the eight lifecycle cards in order on the bench. Click into the sequence field and scan them one after another — the tool records the order it received them. If you scan one out of place, restart the sequence; the record keeps the attempt count.","cap":"rec"},
  {"t":"Step 13. For three stages of your choice, scan the kit-item card that is that stage's first tool (the scanner at receiving and tagging, the cart at staging, the rail kit at deploy, the PSU or fan module at RMA, the drive carrier at decommission, and so on).","cap":"rec"},
  {"t":"Step 14. One stage, one kit item, one sentence: why is it that item you reach for first, and what record does using it create?","cap":"text"},
 ],
 fields=[
  {"id":"kc","type":"rows","n":8,"label":"Kit item","fields":[
    {"id":"code","type":"scan","label":"Kit card — scan it","expect":r"^KIT-(R640|PSU|FAN|DRV|RAIL|CAGE|SCAN|CART)-\d{2}$","kitkey":True,"unique":True},
    {"id":"cls","type":"sel","label":"Classification","opts":["Rack server (1U)","PSU FRU","Fan module FRU","Drive carrier (DBD)","Rail kit","Rack accessory","Scanner (tool)","Material-handling equipment"]},
    {"id":"hd","type":"sel","label":"Handling","opts":["Standard handling","ESD precautions","Team lift","DBD custody"]},
  ]},
  {"id":"seq","type":"seq","label":"Lifecycle sequence — scan the eight stage cards in order","expect_order":LC_CODES},
  {"id":"map","type":"rows","n":3,"label":"Stage → kit item","fields":[
    {"id":"stage","type":"sel","label":"Stage","opts":LC_STAGES},
    {"id":"item","type":"scan","label":"Kit-item card — scan it","expect":r"^KIT-[A-Z0-9]+-\d{2}$"},
  ]},
 ],
)

LABS["1-2"] = dict(
 minutes=30, bench_min=15, kit=["HDD","ASB","COC","SCAN"],
 part="Part 3: The hand-off drill (at the bench)",
 intro="You have just marked gaps in someone else's custody story. Now make one of your own with no gaps. A drive in a sealed anti-static bag changes hands three times in the next ten minutes — bench to partner, partner back to you, you to the instructor's cage. Every transfer is written in the physical logbook at the moment it happens and mirrored into the bench panel. The tool checks that no field is empty; only the logbook proves it happened.",
 steps=[
  {"t":"Step 7. Take the bagged drive at your station. Scan its DBD tag into transfer 1 of the bench panel, then hand it to your partner. Both of you write the logbook line — date/time, from, to, condition, tag — and initial it; mirror the line into the tool before the drive moves again.","cap":"rec"},
  {"t":"Step 8. Your partner hands it back (transfer 2), then you carry it to the instructor's cage (transfer 3). Same discipline each time: scan, write, both initials, mirror. If a field is missing when the tool checks, that is a gap of exactly the kind you just audited.","cap":"rec"},
  {"t":"Step 9. Which field was hardest to capture at the moment of transfer rather than afterwards at the desk — and what would you change about the bench to make it easy?","cap":"text"},
 ],
 fields=[
  {"id":"tr","type":"rows","n":3,"label":"Transfer","fields":[
    {"id":"tag","type":"scan","label":"Drive tag — scan it","expect":r"^DBD-\d{2}$","same":True},
    {"id":"time","type":"text","label":"Date / time","ph":"e.g. 14:32"},
    {"id":"from","type":"text","label":"From","ph":"your name"},
    {"id":"to","type":"text","label":"To","ph":"partner's name / instructor"},
    {"id":"cond","type":"sel","label":"Condition","opts":["Sealed bag intact","Bag open / damaged","Other (note in the last question)"]},
    {"id":"ini","type":"text","label":"Both initials (yours and your partner's)"},
  ]},
 ],
)

LABS["1-3"] = dict(
 minutes=55, bench_min=20, kit=["PPE","ESD","CART","RCV","HDD","ASB","SCAN"],
 part="Part 3: The physical walkdown and PPE fit (at the bench)",
 intro="The tool's four stations were described by a camera. The room has four more, staged for real along the delivery route. Walk it with your partner, find what would fail an audit, and leave what is compliant alone. Then don the PPE for the pallet-unbanding task and have your partner check the fit — the observed lift on Day 4 (SBA 531.1, inside GLAB 531.4.2) will check it again with the instructor watching.",
 steps=[
  {"t":"Step 8. Walk the staged route with your partner. For each hazard you find, record it in the bench panel: where, what, and your response (fix / report / stop work). Photograph one of them for Q5. Do not touch a staged hazard — report it as you would on the floor.","cap":"rec"},
  {"t":"Step 9. Don the full PPE set for a Store House pallet-unbanding task (vest, hard hat, glasses, gloves) and clip the ESD wrist strap to the mat. Your partner checks fit — hat level and snug, glasses seated, strap on skin — and initials the bench panel. Swap roles.","cap":"rec"},
  {"t":"Step 10. Attach your photograph of one staged hazard from the walkdown.","cap":"image"},
  {"t":"Step 11. On the staged route (not the tool's stations): name the one staged item that is compliant and that a nervous new hire would flag anyway, and say why it is fine.","cap":"text"},
 ],
 fields=[
  {"id":"hz","type":"rows","n":6,"label":"Hazard found","optional_from":2,"opt_label":"leave blank if unused","fields":[
    {"id":"where","type":"sel","label":"Where","opts":["Dock / pallet bay","Walkway / aisle","Bench","Door"]},
    {"id":"what","type":"text","label":"What is wrong"},
    {"id":"resp","type":"sel","label":"Response","opts":["Fix it now (trained & equipped)","Report it","Stop work"]},
  ]},
  {"id":"ppe","type":"check","label":"PPE donned: vest, hard hat, safety glasses, gloves"},
  {"id":"strap","type":"check","label":"ESD wrist strap clipped to the mat, on skin"},
  {"id":"fit","type":"text","label":"Partner fit-check initials"},
 ],
)

LABS["2-1"] = dict(
 minutes=65, bench_min=20, kit=["RCV","PKG","PRN","SCAN","ESD","FRU"],
 part="Part 4: The physical receiving bench (at the bench)",
 intro="Now do it with a carton. A real carton from the mock shipping kit is waiting for you at the receiving station with its printed PO/ASN. Weigh it before you open it, verify what is inside against the ASN line, print the asset tag on the label printer, place it on the item per the standard and scan it back into the tool. The tool issued the asset ID; the scanner proves the tag on the metal carries it.",
 steps=[
  {"t":"Step 10. At the receiving station, put the sealed carton on the scale (set to kilograms) and record the reading in the bench panel next to the ASN's declared weight. The tool flags a difference above 0.2 kg — a flagged carton is opened and counted before anything else.","cap":"rec"},
  {"t":"Step 11. Open the carton at your station (ESD strap on for a FRU). Verify the contents against the ASN line — model, serial from the item's own label, quantity, condition — and record the verification.","cap":"rec"},
  {"t":"Step 12. Press Print label in the bench panel. The tool prints the tag it issued (asset ID + barcode) on the ZD621 at the print station. Place it on the item per the placement standard, then scan it back into the tool: the scan must return the issued ID exactly.","cap":"rec"},
  {"t":"Step 13. Your partner checks placement against the standard and initials the panel. Photograph the placed tag with the item's own label visible.","cap":"image"},
  {"t":"Step 14. State the scale reading, the declared weight, and what you did about any difference — and say what a weight difference tells receiving that a carton count cannot.","cap":"text"},
 ],
 fields=[
  {"id":"decl","type":"fixed","label":"ASN declared weight (kg)","value_by_set":{"A":"2.4","B":"2.4","C":"2.4"}},
  {"id":"kg","type":"num","label":"Scale reading (kg)","compare":"decl","tol":0.2},
  {"id":"vf","type":"sel","label":"Contents vs ASN line","opts":["MATCH — model, serial, quantity, condition","DISCREPANCY — quantity short","DISCREPANCY — wrong item","DISCREPANCY — damaged"]},
  {"id":"ser","type":"text","label":"Serial from the item's own label"},
  {"id":"tagid","type":"issued","label":"Asset ID issued for the physical item","value_by_set":{"A":"ATL-00790","B":"ATL-00791","C":"ATL-00792"},"print":True},
  {"id":"tagscan","type":"scan","label":"Printed tag — scan it back","expect_field":"tagid"},
  {"id":"place","type":"sel","label":"Placement","opts":["Upper-left of the rack-visible face, flat surface","Across the ventilation grille","On the removable panel / handle","Over the seam"]},
  {"id":"pini","type":"text","label":"Partner placement-check initials"},
 ],
)

LABS["2-2"] = dict(
 minutes=80, bench_min=20, kit=["FRU","R640","ESD","ASB","SEC","PKG","PRN","SCAN","COC"],
 part="Part 4: The physical pack (at the bench)",
 intro="The custody log you just closed describes a pack. Now do the pack, and let the bench record prove the log was true. Strap on, unit into the shielding bag, bag into the serialized security bag, serial scanned at the moment of sealing, RMA label printed from the tool with the authorization number on it, carton sealed, label on the outside, and a logbook line for the transfer to the shipping cage — the same five fields the gate checks.",
 steps=[
  {"t":"Step 11. Clip the ESD strap to the mat. Take the failed FRU (at a server station: release the PSU handle on the powered-off R640 and slide it out; elsewhere: from the bin). Place it in an anti-static shielding bag and fold the bag closed.","cap":"rec"},
  {"t":"Step 12. Put the bagged unit in a serialized security bag and seal it. At the moment of sealing, scan the bag's serial into the bench panel. Then press Print label next to the RMA authorization: the tool prints the authorization number as a barcode; put the label on the outside of the carton, seal the carton, and scan the label back to confirm it reads.","cap":"rec"},
  {"t":"Step 13. Write the logbook line for bench → shipping cage — date/time, from, to, condition, bag serial, both initials — and mirror it into the bench panel. Photograph the sealed, labeled carton with the bag serial visible through the window or on the manifest.","cap":"image"},
  {"t":"Step 14. One sentence: the bag serial is scanned at sealing and again at the cage — what does the second scan prove that the first cannot?","cap":"text"},
 ],
 fields=[
  {"id":"esd","type":"check","label":"ESD strap clipped before the FRU was touched"},
  {"id":"asb","type":"check","label":"Unit in an anti-static shielding bag, folded closed"},
  {"id":"bag","type":"scan","label":"Security-bag serial — scan it as you seal","expect":r"^[A-Za-z0-9 /-]{5,}$","gate_el":True},
  {"id":"rma","type":"issued","label":"RMA authorization on the label","value_by_set":{"A":"RMA-2026-08814","B":"RMA-2026-08901","C":"RMA-2026-08967"},"print":True},
  {"id":"rmascan","type":"scan","label":"Printed RMA label — scan it back","expect_field":"rma"},
  {"id":"lg","type":"rows","n":1,"label":"Logbook line (bench → shipping cage)","fields":[
    {"id":"time","type":"text","label":"Date / time","ph":"e.g. 14:32"},
    {"id":"from","type":"text","label":"From","ph":"Bench (your name)"},
    {"id":"to","type":"text","label":"To","ph":"Shipping cage"},
    {"id":"cond","type":"sel","label":"Condition","gate_el":True,"opts":["Sealed, serial recorded","Sealed, serial NOT recorded","Unsealed"],"gate":["Sealed, serial NOT recorded","Unsealed"],"hint":"The gate passes only 'Sealed, serial recorded'"},
    {"id":"ini","type":"text","label":"Both initials (yours and your partner's)"},
  ]},
 ],
 gate=True,
 gate_fail=["A custody element missing — an entry, a bag serial, a timestamp, or one set of initials instead of both","The bag unsealed, or sealed with its serial not recorded at the moment of sealing","The RMA label not scanned back, or the carton shipped without it"],
)

LABS["3-1"] = dict(
 minutes=65, bench_min=25, kit=["R640","FRU","SCAN","CART","ESD"],
 part="Part 4: Scan-to-search and the physical move (at the bench)",
 intro="The DCIM inside the tool has its own database. The bench has a second, smaller one — the bench register — and every kit item in the room now carries its tag. Find three real items by scanning their tags, then move one FRU from its shelf bin to the staging cart and make the register follow it, at the cart, before you walk away.",
 steps=[
  {"t":"Step 8. Click into the bench Find field and scan the tag on any three physical items — a server in the rack, a FRU in a bin, a cart. The bench register returns the record for each; check that the location it states is where you found the item and mark each lookup true or false.","cap":"rec"},
  {"t":"Step 9. Strap on. Take one PSU or fan FRU from its shelf bin to the platform cart marked STAGE-1. Scan its tag into the move record and set the new location, status and custody — standing at the cart.","cap":"rec"},
  {"t":"Step 10. One sentence: one of your three lookups may have returned a location that was not where the item was. If it did, what is the correct action — and if it did not, what would have been?","cap":"text"},
 ],
 fields=[
  {"id":"fd","type":"rows","n":3,"label":"Lookup","fields":[
    {"id":"tag","type":"lookup","label":"Asset tag on the item — scan it"},
    {"id":"ok","type":"sel","label":"Is the item where the register says?","opts":["True — found where the register says","False — found elsewhere (note it)"]},
  ]},
  {"id":"mv","type":"rows","n":1,"label":"Physical move","fields":[
    {"id":"tag","type":"lookup","label":"Tag on the FRU you moved — scan it"},
    {"id":"loc","type":"sel","label":"New location","opts":["STAGE-1 (cart)","STAGE-2 (cart)","SH-B-01","SH-B-02","SH-B-03","SH-B-04"]},
    {"id":"st","type":"sel","label":"New status","opts":["Staged","In stock","Deployed","Quarantined"]},
    {"id":"cu","type":"sel","label":"Custody","opts":["Store House","Receiving","DC Hall","Staging cage"]},
  ]},
 ],
)

LABS["3-2"] = dict(
 minutes=80, bench_min=25, kit=["RCV","HDD","FRU","SCAN"],
 part="Part 4: The physical bin count (at the bench)",
 intro="The blind count on the screen becomes a blind count in a box. Your station bin holds tagged items and the register says how many should be there — but the tool will not tell you until you have scanned every item and locked the count. Then reconcile, and if the numbers disagree, find out why from what is physically in front of you.",
 steps=[
  {"t":"Step 10. Click into the scan list and scan every tag in your station bin, one item at a time, setting each item aside as it is scanned. When the bin is empty, press Lock count. The register quantity appears only then.","cap":"rec"},
  {"t":"Step 11. If there is a variance, look for the evidence in the bin and around it: a pick card, an item whose tag belongs to another bin, a duplicate scan. Record the cause and what you did — and apply the escalation matrix exactly as you did on the screen.","cap":"rec"},
  {"t":"Step 12. One sentence: what did scanning give you that counting by eye would not have — and what did it still not protect you from?","cap":"text"},
 ],
 fields=[
  {"id":"cnt","type":"seq","label":"Scan every tag in the bin, then lock the count","expect_qty":5,"lock":True},
  {"id":"cause","type":"sel","label":"Cause of any variance","opts":["No variance","Unlogged consumption (pick card in bin)","Item belongs to another bin (mislocated)","Duplicate / missed scan — recounted","Other (note)"]},
  {"id":"act","type":"sel","label":"Action","opts":["No action — count agrees","Adjust with documented cause","Escalate — serialized item","Escalate — above 5%"]},
  {"id":"note","type":"text","label":"Evidence note"},
 ],
)

LABS["4-1"] = dict(
 minutes=65, bench_min=15, kit=["R640","FRU","ASB","PKG","PRN","SCAN","ESD"],
 part="Part 4: The service tag and the return pack (at the bench)",
 intro="Entitlement starts with the identifier on the metal, not the one on the ticket. Every R640 carries its service tag on the pull-out tag at the front of the chassis — read it from there and record it. Then pack the unit for the path you committed to: a claim ships with the authorization on the outside; a disposition unit is shelved with a HOLD label; nothing on an anomaly path ships at all.",
 steps=[
  {"t":"Step 9. At a server station, pull out the R640's information tag and read the Dell service tag (seven characters). Type or scan it into the bench panel — the tool checks the format. Record which server (its ATL tag) you read it from.","cap":"rec"},
  {"t":"Step 10. Strap on and pack the FRU for your path: shielding bag, carton, then press Print label next to the path label. Claim sets print the authorization number; no-claim sets print HOLD — disposition review. Put the label on the outside and scan it back.","cap":"rec"},
  {"t":"Step 11. Photograph the packed, labeled unit.","cap":"image"},
  {"t":"Step 12. One sentence: why is the service tag read from the chassis and not copied from the ticket, and what happens to a claim when the two differ?","cap":"text"},
 ],
 fields=[
  {"id":"srv","type":"lookup","label":"Asset tag on the server — scan it"},
  {"id":"stag","type":"scan","label":"Dell service tag (from the pull-out tag)","expect":r"^[A-Za-z0-9]{7}$"},
  {"id":"esd","type":"check","label":"ESD strap on; unit in a shielding bag"},
  {"id":"lbl","type":"issued","label":"Path label","value_by_set":{"A":"CLM-2026-44172","B":"HOLD-DISPOSITION-REVIEW"},"print":True},
  {"id":"lblscan","type":"scan","label":"Printed path label — scan it back","expect_field":"lbl"},
 ],
)

LABS["4-2"] = dict(
 minutes=85, bench_min=0, kit=["R640","RACK","CART","PPE","ESD","SCAN"],
 part="Part 4: The bench record of the move (at the rack)",
 intro="The move in Part 2 is now a real R640 on a real cart into the real rack. Your instructor scores the observed lift (SBA 531.1 — Safe Lift & Access Performance Check) on this move. The bench record structures what your instructor observes: the scans that prove the right unit went to the right U, and the checklist that proves it was secured and dressed before you walked away. Your instructor watches eight things on your lift: you read the plate weight and call the team lift before touching the unit; you wear the PPE the task needs and no more; the route and the set-down point are clear and the cart wheels are locked; the lift is on an agreed count, load close, no twist; the set-down is controlled with fingers clear; at the controlled door it is one badge, one person, and you challenge or report a tailgating attempt; you name the staged hazard on the route when asked; and no unsafe act anywhere in the observation. If something is missed, your instructor coaches you and you lift again.",
 steps=[
  {"t":"Step 11. Do Steps 11–12 while you make the Part 2 move at the rack, not afterwards. Before the lift: scan the unit's bench tag and the rail-kit card into the panel, confirm PPE and the team-lift partner by initials, and scan the U-position label on the rack you are racking into.","cap":"rec"},
  {"t":"Step 12. Rack the unit: rails in, cage nuts at the marked U, unit seated on an agreed count, screws in, level. Then dress it: blanking panel in the gap above or below, cable management arm or bar fitted, cable ends labeled. Tick each item only when it is true.","cap":"rec"},
  {"t":"Step 13. One sentence: which step of the physical racking took longest, and what would you stage differently before the next lift?","cap":"text"},
 ],
 fields=[
  {"id":"unit","type":"lookup","label":"Asset tag on the unit — scan it"},
  {"id":"rail","type":"scan","label":"Rail-kit card — scan it","expect":r"^KIT-RAIL-\d{2}$"},
  {"id":"upos","type":"scan","label":"U-position label on the rack — scan it","expect":r"^U-\d{2}$"},
  {"id":"ppe","type":"check","label":"PPE on; route clear; set-down point clear"},
  {"id":"partner","type":"text","label":"Team-lift partner initials"},
  {"id":"r1","type":"check","label":"Rails seated both sides; cage nuts at the marked U"},
  {"id":"r2","type":"check","label":"Unit seated and screwed in; level"},
  {"id":"r3","type":"check","label":"Blanking panel fitted in the adjacent gap"},
  {"id":"r4","type":"check","label":"Cable management fitted; cable ends labeled"},
  {"id":"r5","type":"check","label":"Cart returned; packaging cleared; nothing on top of the rack"},
  {"id":"sba","type":"sel","label":"SBA 531.1 result (your instructor enters this)","opts":["Pass","Re-run after coaching"]},
 ],
)

LABS["5-1"] = dict(
 minutes=75, bench_min=25, kit=["HDD","ASB","SEC","SCAN","ESD","COC"],
 part="Part 4: The physical census and bagging (at the bench)",
 intro="The drives on the screen were serials in a table. The drives on the bench are the real thing, and the census rule is the same: record what is physically there, not what the paperwork expected. Every drive goes into its own shielding bag, then its own serialized security bag; the bag serial is scanned at the moment of sealing, against the drive's tag, and the logbook line is written before the next drive is touched.",
 steps=[
  {"t":"Step 10. Strap on. Open the station's chassis bag and lay out every drive. In the bench panel, scan each drive's DBD tag into its own row — the census. Do not look at how many rows you 'should' have; the panel accepts what you scan.","cap":"rec"},
  {"t":"Step 11. For each drive: shielding bag, then security bag, seal, and scan the bag serial into the same row at the moment of sealing. The tool refuses a bag serial that is already used. Write the logbook line per bag and put both initials in the row.","cap":"rec"},
  {"t":"Step 12. Photograph the sealed bags with the serials visible.","cap":"image"},
  {"t":"Step 13. One sentence: your census found the number of drives it found. If it was more than the work order expected, what did you do with the extra one — and if it was not, what would you have done?","cap":"text"},
 ],
 fields=[
  {"id":"dr","type":"rows","n":3,"label":"Drive","optional_from":3,"opt_label":"only if a third drive is in your bag","fields":[
    {"id":"tag","type":"scan","label":"Drive tag — scan it","expect":r"^DBD-\d{2}$","unique":True},
    {"id":"bag","type":"scan","label":"Security-bag serial — scan it as you seal","expect":r"^[A-Za-z0-9 /-]{5,}$","unique":True,"gate_el":True},
    {"id":"ini","type":"text","label":"Both initials (yours and your partner's)"},
  ]},
  {"id":"esd","type":"check","label":"ESD strap on for the whole census"},
 ],
 gate=True,
 gate_fail=["A drive physically present with no row, or a row without both initials","Fewer drives bagged than the census found, or a bag serial reused","A wrong PROCEED / STOP call in the tool against the work order"],
)

LABS["5-2"] = dict(
 minutes=65, bench_min=25, kit=["HDD","RACK","SCAN","SEC"],
 part="Part 3: Sorting the shelf and the destruction record (at the bench)",
 intro="The review shelf is now three real items in front of you and three bins behind them. Scan each item, scan the bin you put it in, and let the record show the path you chose. Then the hand-over for destruction: one drive from the cohort's DBD cage is sealed into the destruction vendor's serialized transfer bag at the instructor bench. You do what a DCLT does at that hand-over: scan the serial before it goes in, witness the seal, and write the hand-over line the certificate of destruction will be matched against.",
 steps=[
  {"t":"Step 10. For each of the three physical items at your station: scan its tag or card, decide its path, and scan the bin card you place it in. The bin must match the path the item's dossier card supports.","cap":"rec"},
  {"t":"Step 11. At the destruction hand-over (instructor bench): scan the drive's DBD tag before it goes into the vendor transfer bag, watch the bag being sealed, and complete the hand-over line in the bench panel — method Destroy, date, sealed by (instructor), witness (you).","cap":"rec"},
  {"t":"Step 12. One sentence: after the hand-over, what evidence do you hold that a specific serial went for destruction — and why is the vendor's certificate of destruction still needed?","cap":"text"},
 ],
 fields=[
  {"id":"it","type":"rows","n":3,"label":"Item","fields":[
    {"id":"tag","type":"scan","label":"Item tag or card — scan it","expect":r"^(ATL-\d{5}|DBD-\d{2}|KIT-[A-Z0-9]+-\d{2}|ITEM-[A-Z0-9-]+)$"},
    {"id":"path","type":"sel","label":"Path","opts":["Redeploy","Scrap","Dispose"]},
    {"id":"bin","type":"scan","label":"Bin card — scan the bin you chose","expect":r"^BIN-(REDEPLOY|SCRAP|DISPOSE)$","match_path":True},
  ]},
  {"id":"cert","type":"rows","n":1,"label":"Destruction hand-over line","fields":[
    {"id":"tag","type":"scan","label":"Drive tag — scan it before it is sealed","expect":r"^DBD-\d{2}$","hint":"If the drive is already bagged, scan the tag through the bag window"},
    {"id":"bag","type":"scan","label":"Vendor transfer-bag serial — scan it as the bag is sealed","expect":r"^[A-Za-z0-9 /-]{5,}$","hint":"The vendor's certificate quotes this bag serial and the drive tag — that pairing is your evidence"},
    {"id":"method","type":"sel","label":"Method","opts":["Clear","Purge","Destroy"],"want":"Destroy"},
    {"id":"date","type":"text","label":"Date","ph":"e.g. 26 Sep 2026"},
    {"id":"op","type":"text","label":"Sealed by (instructor)"},
    {"id":"wit","type":"text","label":"Witness (you)"},
  ]},
 ],
)

# ---------------------------------------------------------------- run sheets (minutes) — one lesson-day = 220 content min (4 h with two 10-min breaks)
RESERVE = "Reserve — gate bench re-run window on a fresh set (or early close)"
RUN = {
 0:[("Welcome, course arc, the DCLT boundary (kit and hand off, never install); Deck 531-0: platforms, how a bench lab is submitted",15),("GLAB 531.0.1 Parts 1–2 (platforms; Canvas test drop and intro post inside the lab)",20),("GLAB 531.0.1 Part 3 station check-in at the bench",5)],
 1:[("Deck 531-1 part 1: zones, hardware families, the lifecycle rail, custody and DBD rules, kit walk-through at the bench",20),("GLAB 531.1.1 (tool, then kit station and the lifecycle walk)",35),("GLAB 531.1.2 (tool, then hand-off drill)",30),("Deck part 2: procedure types, LOTO, PPE, lifting, access control, CE vocabulary",20),("GLAB 531.1.3 (tool, then the physical walkdown and PPE fit)",55),("Quiz 531.1 with reflection items (both attempts inside the window)",20)],
 2:[("Deck 531-2: receiving, PO/ASN, the tag standard, the scale and the printer",20),("GLAB 531.2.1 (tool, then receiving bench in rotation)",65),("Deck: the RMA cycle and custody fields; the pack",25),("GLAB 531.2.2 (GATE; tool, then physical pack)",80),("Quiz 531.2 with reflection items (both attempts inside the window)",20),(RESERVE,10)],
 3:[("Deck 531-3: DCIM, data integrity, scan-to-search",20),("GLAB 531.3.1 (tool, then bench register)",65),("Deck: cycle counts, consumption, discrepancy method",25),("GLAB 531.3.2 (tool, then physical bin count)",80),("Quiz 531.3 with reflection items (both attempts inside the window)",20),("Reserve — gate bench re-runs carried from Day 2 (or early close)",10)],
 4:[("Deck 531-4: entitlement, claims, return paths, the service tag",25),("GLAB 531.4.1 (tool, then service tag and pack) — stations not at the rack",65),("Deck: move planning, racking standard, rails and cage nuts",15),("GLAB 531.4.2 at the PS mobile rack, four server stations in rotation, with SBA 531.1 observed on each pair's lift",85),("Quiz 531.4 with reflection items (both attempts inside the window)",25),("Reserve (or early close)",5)],
 5:[("Deck 531-5: decommission sequence, DBD rules, 45-day clock, double-sealing",20),("GLAB 531.5.1 (GATE; tool, then physical census and bagging)",75),("Deck: dispositions, NIST 800-88, certificates",25),("GLAB 531.5.2 (tool, then sorting and the destruction hand-over)",65),("Quiz 531.5 with reflection items (both attempts inside the window), course close",25),(RESERVE,10)],
}
DAY_OF = {0:1, 1:1, 2:2, 3:3, 4:4, 5:5}            # lesson -> class day; every lesson closes on its own day
DAY_MIN = 220                                        # content minutes per day (4 h less two 10-min breaks)
def run_start(l): return sum(m for _,m in RUN[0]) if l == 1 else 0   # Lesson 531.1 follows 531.0 on Day 1
def run_hours(l): return sum(m for _,m in RUN[l])/60.0

LAB_ORDER = ["0-1","1-1","1-2","1-3","2-1","2-2","3-1","3-2","4-1","4-2","5-1","5-2"]
LAB_META = {  # id: (GLAB id, title, slug, sets, lesson)
 "0-1":("GLAB 531.0.1","Platform Readiness Check","PlatformCheck",[""],0),
 "1-1":("GLAB 531.1.1","Zone and Hardware Identification","ZoneID",["A","B"],1),
 "1-2":("GLAB 531.1.2","Chain-of-Custody Walkthrough","CustodyWalk",["A","B"],1),
 "1-3":("GLAB 531.1.3","PPE and Hazard Recognition Walkdown","HazardWalk",["A","B"],1),
 "2-1":("GLAB 531.2.1","Asset Tagging and Scan Verification","AssetTag",["A","B","C"],2),
 "2-2":("GLAB 531.2.2","End-to-End RMA with Chain-of-Custody","RMACycle",["A","B","C"],2),
 "3-1":("GLAB 531.3.1","DCIM Asset Records","DCIM",["A","B","C"],3),
 "3-2":("GLAB 531.3.2","Cycle Count and Variance Investigation","CycleCount",["A","B","C"],3),
 "4-1":("GLAB 531.4.1","Warranty Claim and Return Processing","Warranty",["A","B"],4),
 "4-2":("GLAB 531.4.2","Rack and Stack Move","RackStack",["A","B"],4),
 "5-1":("GLAB 531.5.1","Secure Decommission","Decom",["A","B","C"],5),
 "5-2":("GLAB 531.5.2","Disposition and Sanitization Records","Disposition",["A","B","C"],5),
}
# v2.1: text substitutions applied to every file taken from the v2.0 source package
TEXT_SUB = [("GLAB 531.1.4", "GLAB 531.1.3"), ("531.1.4", "531.1.3"), ("531-1-4-", "531-1-3-"), ("531-1-4_", "531-1-3_"),
            ("GLAB 531.1.1–1.3", "GLAB 531.1.1–1.2"), ("531.1.1–1.3", "531.1.1–1.2"),
            ("is assessed live at the MIR rack under SBA 531.1", "is assessed live at the mobile rack under SBA 531.1 during the Day 4 rack-and-stack lab (GLAB 531.4.2)"),
            ("assessed live at the MIR rack", "assessed live at the mobile rack during the Day 4 rack-and-stack lab"),
            ("15 to plan, 35 for the move and racking, 10 for cabling, 10 for system updates and housekeeping.", "15 to plan, 35 for the move and racking (your instructor scores SBA 531.1 on your lift), 10 for cabling, 10 for system updates and housekeeping, and 15 for the rotation at the rack."),
            ("35 in the tool, 15 for the PPE fit check and debrief.", "35 in the tool."),
            ("10 for verification, 30 for tagging and scanning, 10 for the discrepancy write-up.", "10 for verification, 25 for tagging and scanning, 10 for the discrepancy write-up."),
            ("15 for intake and fault documentation, 20 for the vendor submission and packing, 15 for receipt and log closure, 20 for the peer log audit.", "15 for intake and fault documentation, 15 for the vendor submission and packing, 15 for receipt and log closure, 15 for the peer log audit."),
            ("15 to count, 10 to reconcile, 20 to investigate and document, 15 for the ticket panel and review.", "15 to count, 10 to reconcile, 15 to investigate and document, 15 for the ticket panel and review."),
            ("A metal lesson smaller than a thumb", "A metal module smaller than a thumb"),
            ("A bare lesson the size of a hardback book", "A bare module the size of a hardback book"),
            ("MIR rack", "mobile rack"), ("The MIR cross-check", "The mobile-rack cross-check"),
            # approved 22 Sep: escalation rule in one voice (the quiz key: above-threshold variances escalate even when explained)
            ("The threshold applies to the variance that is still unexplained after logged consumption and documented corrections (a mislabel moved between bins nets to zero); a fully explained variance is adjusted with its cause, never escalated.",
             "The threshold applies after documented corrections between bins (a mislabel moved between bins nets to zero). Unlogged consumption is a real variance: record the cause against the ticket and, above the threshold, escalate as well."),
            # simulator bodies: messages, guards and labels that lost a first-time learner
            ('<h2 id="pathTitle">Step 3 &mdash; the path</h2>', '<h2 id="pathTitle">Steps 4&ndash;5 &mdash; the path</h2>'), ('"Step 3 &mdash; "', '"Steps 4&ndash;5 &mdash; "'),
            ('<h2>Step 4 &mdash; final state</h2>', '<h2>Step 6 &mdash; final state</h2>'),
            ('<h2>Step 1 &mdash; authorization vs the metal</h2>', '<h2>Part 1 (Steps 1&ndash;3) &mdash; authorization vs the metal</h2>'),
            ('<h2>Step 2 &mdash; the sequence (each step takes a timestamp)</h2>', '<h2>Part 2 (Steps 4&ndash;6) &mdash; the custody log (each step takes a timestamp)</h2>'),
            ('<h2>Step 3 &mdash; closing the record</h2>', '<h2>Part 3 (Step 7) &mdash; closing the record</h2>'),
            ('<h2>Step 1 &mdash; the three dossiers</h2>', '<h2>Part 1 (Steps 1&ndash;2) &mdash; the three dossiers</h2>'),
            ('<h2>Step 2 &mdash; the matching forms</h2>', '<h2>Part 1 (Step 3) &mdash; the matching forms</h2>'),
            ('<h2>Step 3 &mdash; sanitization determinations (NIST 800-88)</h2>', '<h2>Part 2 (Steps 5&ndash;7) &mdash; sanitization determinations (NIST 800-88)</h2>'),
            ('One missing custody element &mdash; an entry, a signature, a seal or bag serial, a timestamp &mdash; is a Not Yet and a re-take on a different set.', 'One missing custody element &mdash; an entry, a set of initials on the bench panel&rsquo;s logbook line, a seal or bag serial, a timestamp &mdash; fails the gate; the bench half is re-run on a fresh set in the day&rsquo;s reserve window.'),
            ('<div><label for="bg_bag">Bag serial</label><select id="bg_bag"><option value="">&mdash;</option><option>TEB-40211</option><option>TEB-40212</option></select></div>\n</div>',
             '<div><label for="bg_bag">Bag serial</label><select id="bg_bag"><option value="">&mdash;</option><option>TEB-40211</option><option>TEB-40212</option></select></div>\n<div><label for="bg_ini">Logged by (initials)</label><input type="text" id="bg_ini" size="8" placeholder="yours"></div>\n</div>'),
            ('var d=val("bg_drive"),b=val("bg_bag");\n if(!d||!b){status("Drive serial and bag serial both required at sealing.",false);return}', 'var d=val("bg_drive"),b=val("bg_bag"),ini=val("bg_ini");\n if(!d||!b||!ini){status("Drive serial, bag serial and your initials are all required at sealing.",false);return}'),
            ('bags.push([d,b,nowstr()]);simSet("bagged",bags);', 'bags.push([d,b,nowstr(),ini]);simSet("bagged",bags);$("bg_ini").value="";SIM["f:bg_ini"]="";'),
            ('tbl(["Drive serial","Bag serial","Sealed at"],bags.map(function(r){return r.map(esc)}))', 'tbl(["Drive serial","Bag serial","Sealed at","Logged by"],bags.map(function(r){return r.map(esc)}))'),
            ('esc(ENT.cov+" &middot; expires "+ENT.end+" &middot; "+(ENT.live?"ACTIVE":"EXPIRED"))', 'esc(ENT.cov+" · expires "+ENT.end+" · "+(ENT.live?"ACTIVE":"EXPIRED"))'),
            ('<h2>The rack elevation &mdash; click the U range you racked into</h2>', '<h2>The rack elevation &mdash; Click the lowest U of the range you racked into (the tool fills the second)</h2>'),
            ('SIM["locked"]=true;simSave();renderRecon();', 'if(!SIM["first"]){SIM["first"]={};BINS.forEach(function(b){SIM["first"][b[0]]=val("cnt_"+b[0])})}SIM["locked"]=true;simSave();renderRecon();'),
            ('$("reconPanel").hidden=false;$("invPanel").hidden=false;', '$("reconPanel").hidden=false;$("invPanel").hidden=false;BINS.forEach(function(b){$("cnt_"+b[0]).disabled=true});'),
            ('return [b[0],orDash(mine),SIM["locked"]?String(b[2]):"hidden",', 'return [b[0],orDash(SIM["first"]&&SIM["first"][b[0]]),orDash(mine),SIM["locked"]?String(b[2]):"hidden",'),
            ('tbl(["Bin","Final count","System qty","Variance"],crow)', 'tbl(["Bin","First count","Final count","System qty","Variance"],crow)'),
            ('val("cl_seal")||"&mdash;"', 'val("cl_seal")||"—"'),
            ('<button type="button" class="small" onclick="addCust()">Add custody entry</button>', '<button type="button" class="small" onclick="addCust()">Add custody entry</button> <button type="button" class="small" id="custUndo" onclick="undoCust()">Remove last entry</button>'),
            ('function renderCust(){', 'function undoCust(){var c=custRows();if(!c.length){status("Nothing to remove.",false);return}c.pop();simSet("cust",c);renderCust();status("Last custody entry removed - "+c.length+" logged.")}\nfunction renderCust(){'),
            ('if(custRows().length<2){$("advOut")', 'if(custRows().length<3){$("advOut")'),
            ('var c=custRows();if(c.length<5)probs.push("custody log has "+c.length+" entries (a complete cycle has at least 5)");',
             'var c=custRows();if(c.length<5)probs.push("custody log has "+c.length+" entries (a complete cycle has at least 5)");c.forEach(function(r,i){if(r[5]!=="Both"&&!(r[5]==="Vendor scan"&&i===c.length-1))probs.push("entry "+(i+1)+" carries one signature, not both");if(/cage|carrier/i.test(r[2])&&(!r[4]||r[4]==="—"))probs.push("entry "+(i+1)+" reaches the "+r[2]+" with no seal or bag serial")});'),
            ('(miss?\'<p class="badmark">\'+miss+\' item(s) incomplete or not scanned green.</p>\':\'<p class="okmark">Bench complete.</p>\')', '(miss?\'<p class="badmark">\'+miss+\' item(s) incomplete or not scanned green.</p>\':\'<p class="okmark">Simulator record complete.</p>\')'),
            ('var dx=[["Asset",orDash(val("dx_asset"))],', 'var dxIds=["dx_asset","dx_field","dx_exp","dx_found","dx_disp"];dxIds.forEach(function(k){if(!val(k))miss++});var dx=[["Asset",orDash(val("dx_asset"))],'),
            ('function scan(i){\n var a=AST[i],el=$("sc_"+i);', 'function scan(i){\n var a=AST[i],el=$("sc_"+i);["ts_"+i,"tm_"+i].forEach(function(k){var f=$(k);if(f&&f.value)f.value=f.value.toUpperCase()});'),
            ('<label for="f2_\'+a.id+\'">Authorization / reference</label><input type="text" id="f2_\'+a.id+\'" size="22">', '<label for="f2_\'+a.id+\'">Authorization / reference</label><input type="text" id="f2_\'+a.id+\'" size="22" placeholder="e.g. DECOM-2026-0341">'),
            ('<label for="f3_\'+a.id+\'">Final custody handoff (to whom, signed)</label><input type="text" id="f3_\'+a.id+\'" size="26">', '<label for="f3_\'+a.id+\'">Final custody handoff (to whom, signed)</label><input type="text" id="f3_\'+a.id+\'" size="26" placeholder="e.g. DBD cage - J. Instructor (signed)">'),
            ('<label for="mv_\'+i+\'">Verifier</label><input type="text" id="mv_\'+i+\'" size="16">', '<label for="mv_\'+i+\'">Verifier</label><input type="text" id="mv_\'+i+\'" size="16" placeholder="e.g. partner initials">'),
            ('<p class="hint">Task card: <b class="mono">ATL-00429</b> was physically moved to <b class="mono">STAGE-2</b>.</p>', '<p class="hint">Task card: <b class="mono">ATL-00429</b> was physically moved to <b class="mono">STAGE-2</b> &mdash; status Staged, custody Staging cage.</p>'),
            # handouts
            ("Step 6. One of the placement options for each asset is wrong in a way the standard names explicitly. For any one asset, say which placement option you rejected and quote the line of the standard that rules it out.", "Step 6. Three of the four placement options for each asset are wrong in ways the standard names explicitly. For any one asset, pick one of the three non-standard options you rejected and quote the line of the standard that rules it out."),
            ("This is also custody entry 1 - the moment the unit became yours.", "This is also custody entry 1 - the moment the unit became yours. Log entry 1 in the Custody log (Stage 3 panel) now, not later."),
            ("Step 2. Choose the route on the route map. One of the route options violates a rule you learned in Lesson 531.1 - do not take it.", "Step 2. Choose the route on the route map. Two of the three routes violate a rule you learned in Lesson 531.1 - do not take either."),
            ("Step 3. State in one sentence why the route you rejected is wrong, naming the rule it breaks.", "Step 3. State in one sentence for each route you rejected why it is wrong, naming the rule it breaks."),
            ("Step 6. Put on the PPE for a Store House pallet-unbanding task from your station kit. Photograph yourself or your kit laid out, and attach it. The SBA will check fit and use live - this records that you can select the set.", "Step 6. Photograph your station kit's PPE set for a Store House pallet-unbanding task laid out on the bench, and attach it - this records that you can select the set; you put it on at the bench in Step 9."),
            ("Step 11. Name the one staged item on the route that is compliant and that a nervous new hire would flag anyway, and say why it is fine.", "Step 11. On the staged route (not the tool's stations): name the one staged item that is compliant and that a nervous new hire would flag anyway, and say why it is fine."),
            ("Step 8. Click into the bench Find field and scan the tag", "Step 8. Click into the bench panel's field labelled 'Asset tag on the item - scan it' and scan the tag"),
            # learner audit (v2.1): references and messages that lost a first-time learner
            ("for Q7 in the submission panel", "for Q2 (Step 7) in the submission panel"),
            ("Check the service tag against the plate.", "Re-read the seven characters on the chassis pull-out tag and type them again, no spaces."),
            ("Media: HDD 2TB S/N HDD-2T-87001 &middot;", "Media: two HDD 2TB, S/N HDD-2T-87001 and HDD-2T-87002 &middot;"),
            ("Cycle records complete.", "No open items in the custody log audit."),
            ("'<span class=\"okmark\">SCAN OK &mdash; tag matches plate'+(val(\"tp_\"+i)!==GOODPLACE?' (placement violates the standard)':'')+'</span>'",
             "(val(\"tp_\"+i)!==GOODPLACE?'<span class=\"badmark\">SCAN FAIL &mdash; tag matches plate but the placement violates the standard</span>':'<span class=\"okmark\">SCAN OK &mdash; tag matches plate; placement per the standard</span>')"),
            ("<h2>Task 2 &mdash; create the missing record</h2>\n<div class=\"frow\">",
             "<h2>Task 2 &mdash; create the missing record</h2>\n<p class=\"hint\">Task card: create <b class=\"mono\">ATL-00436</b> &mdash; serial <b class=\"mono\">PP-24-70338</b>, 24-port patch panel, category Network, location <b class=\"mono\">SH-B-06</b>, status In stock, custody Store House.</p>\n<div class=\"frow\">")]
TEXT_RE = [(r'aria-label="Bin (B\d) contains \d+ units, count them visually"', r'aria-label="Bin \1 shelf view - count the units"')]
def subst(s):
    for a, b in TEXT_SUB:
        if a in b and b in s: continue          # an extension already applied (rebuild from a v2.1 package)
        s = s.replace(a, b)
    import re as _re
    for a, b in TEXT_RE: s = _re.sub(a, b, s)
    return s
def tool_file(lid, s):
    g,t,slug,sets,les = LAB_META[lid]
    return f"531-{lid}{('-'+s) if s else ''}_{slug}.html"
def tool_files_label(lid):
    g,t,slug,sets,les = LAB_META[lid]
    if sets==[""]: return tool_file(lid,"")
    return f"531-{lid}-{' / '.join(sets)}_{slug}.html"

def load_keys():
    """Find spec_keys.py: next to this file, or in 5_Instructor_ONLY/build relative to 4_Lab_Tools/build, or $BUILD_KEYS."""
    import os, sys, importlib
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.environ.get("BUILD_KEYS",""), here, os.path.join(here, "..", "..", "5_Instructor_ONLY", "build")]
    for c in cands:
        if c and os.path.exists(os.path.join(c, "spec_keys.py")):
            if c not in sys.path: sys.path.insert(0, c)
            return importlib.import_module("spec_keys").merge(sys.modules[__name__])
    raise SystemExit("spec_keys.py not found (instructor-only, 5_Instructor_ONLY/build). Set BUILD_KEYS to its folder.")
