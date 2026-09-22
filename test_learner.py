"""Learner-flow checks (v2.1 learner audit): the moments where a first-time learner got lost.
Headless Chromium; exits non-zero on any failure. Run after gen_tools."""
import asyncio, os, sys
from playwright.async_api import async_playwright
OUT = os.environ["OUT"]; T = os.path.join(OUT, "4_Lab_Tools")
fails = []
def check(name, ok, info=""):
    print(("ok   " if ok else "FAIL ") + name + (" — " + str(info) if info and not ok else ""))
    if not ok: fails.append(name)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1366, "height": 768})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        async def go(f): errs.clear(); await pg.goto("file://" + os.path.join(T, f)); await pg.wait_for_timeout(120)

        # 1. A valid scan moves focus to the next empty scan field, so the next scan does not concatenate
        await go("531-0-1_PlatformCheck.html")
        await pg.click("#b_stn"); await pg.keyboard.type("STN-03"); await pg.keyboard.press("Enter")
        await pg.keyboard.type("KIT-SCAN-03"); await pg.keyboard.press("Enter")
        check("scan advances to the next field", await pg.input_value("#b_stn") == "STN-03" and await pg.input_value("#b_scn") == "KIT-SCAN-03",
              (await pg.input_value("#b_stn"), await pg.input_value("#b_scn")))

        # 2. Build submission sheet does not paint a failed bench record before the bench was touched
        await go("531-2-1-A_AssetTag.html")
        await pg.click("#btnSheet"); await pg.wait_for_timeout(80)
        check("untouched bench is not built by the sheet button", (await pg.inner_text("#benchOut")).strip() == "")

        # 3. Bench-only lab (531.0.1): the submission PDF carries the bench record, not 'assessed on the floor'
        await go("531-0-1_PlatformCheck.html")
        await pg.click("#benchPanel button.primary"); await pg.click("#lqBuild"); await pg.wait_for_timeout(120)
        out = await pg.evaluate("(document.getElementById('lqOut')||{}).innerText||''")
        check("0-1 PDF includes the bench record", "Bench record" in out and "Assessed on the floor" not in out)

        # 4. Bench misses show up in the completeness list of the PDF
        await go("531-1-1-A_ZoneID.html")
        await pg.click("#benchPanel button.primary"); await pg.click("#lqBuild"); await pg.wait_for_timeout(120)
        out = await pg.evaluate("(document.getElementById('lqOut')||{}).innerText||''")
        for _ in range(3): await pg.click("#lqBuild"); await pg.wait_for_timeout(80)
        check("repeated PDF builds do not duplicate the records", await pg.evaluate("Array.from(document.querySelectorAll('#lqOut h3')).filter(h=>/^Bench record/.test(h.textContent)).length") == 1)
        check("bench misses listed as gaps", "bench record: " in out.lower() and "missing or failing" in out.lower() and ".." not in out, out[-400:])

        # 5. Gate labs: a 'NOT recorded' custody choice is red in the bench record
        await go("531-2-2-A_RMACycle.html")
        await pg.select_option("#b_lg_1_cond", "Sealed, serial NOT recorded"); await pg.click("#benchPanel button.primary"); await pg.wait_for_timeout(80)
        check("gate flags NOT recorded", await pg.evaluate("!!document.querySelector('#benchOut .badmark')") and "gate" in (await pg.inner_text("#benchPanel")).lower())

        # 6. Bench messages appear at the bench, not in the page header
        await go("531-3-2-B_CycleCount.html")
        await pg.click("#b_cnt_lock"); await pg.wait_for_timeout(50)
        check("lock message at the bench", "scan every item" in (await pg.inner_text("#b_cnt_st")).lower())

        # 7. Copy fixes carried from the walk
        s41 = open(os.path.join(T, "531-4-1-A_Warranty.html"), encoding="utf-8").read()
        check("4-1 Q7 reference fixed", "for Q7 in the submission panel" not in s41 and "Q2 (Step 7)" in s41)
        s52 = open(os.path.join(T, "531-5-2-A_Disposition.html"), encoding="utf-8").read()
        check("5-2 D1 dossier lists both drives", "HDD-2T-87001 and HDD-2T-87002" in s52)
        s22 = open(os.path.join(T, "531-2-2-A_RMACycle.html"), encoding="utf-8").read()
        check("2-2 no false 'complete' on the custody log", "Cycle records complete." not in s22)
        s51 = open(os.path.join(T, "531-5-1-A_Decom.html"), encoding="utf-8").read()
        check("5-1 third drive row worded honestly", "(optional)" not in s51 and "only if a third drive" in s51)
        s31 = open(os.path.join(T, "531-3-1-A_DCIM.html"), encoding="utf-8").read()
        check("3-1 Task 2 shows its task card", "Task card:" in s31.split("Task 2 &mdash;")[1][:600])
        s21 = open(os.path.join(T, "531-2-1-A_AssetTag.html"), encoding="utf-8").read()
        check("2-1 placement violation is red, not SCAN OK", "SCAN FAIL &mdash; tag matches plate but the placement" in s21 and "tag matches plate'+(val" not in s21)
        s12 = open(os.path.join(T, "531-1-2-A_CustodyWalk.html"), encoding="utf-8").read()
        check("1-2 logbook fields carry format hints", 'placeholder="e.g. 14:32"' in s12)
        import docx
        h42 = "\n".join(p.text for p in docx.Document(os.path.join(OUT, "3_Handouts", "531-4-2_GLAB_Rack_Stack.docx")).paragraphs)
        check("4-2 handout names the eight observed SBA points", "eight things" in h42 and "tailgating" in h42.lower())
        # ---- approved recommendations (validation-reopening and remaining items), 22 Sep
        rd = lambda f: open(os.path.join(T, f), encoding="utf-8").read()
        s32 = rd("531-3-2-A_CycleCount.html")
        check("3-2 escalation rule has one voice", "after logged consumption" not in s32 and "Unlogged consumption is a real variance" in s32)
        check("3-2 shelf aria-label hides the count", "contains 14 units" not in s32)
        await go("531-3-2-A_CycleCount.html")
        for b_, v in [("B1","14"),("B2","6"),("B3","10"),("B4","9"),("B5","3"),("B6","11")]: await pg.fill("#cnt_"+b_, v)
        await pg.click("text=Lock counts"); await pg.wait_for_timeout(80)
        check("3-2 counts lock after Lock", await pg.evaluate("document.getElementById('cnt_B3').disabled"))
        await pg.click("#btnSheet"); await pg.wait_for_timeout(80)
        check("3-2 sheet records first and final counts", "first count" in (await pg.inner_text("#sheetOut")).lower())
        await go("531-5-2-A_Disposition.html")
        check("5-2 hand-over line has a bag serial field", await pg.evaluate("!!document.getElementById('b_cert_1_bag')"))
        await pg.select_option("#b_cert_1_method", "Clear"); await pg.click("#benchPanel button.primary"); await pg.wait_for_timeout(80)
        check("5-2 method other than Destroy is red", "destroy" in (await pg.inner_text("#benchOut")).lower() and await pg.evaluate("!!document.querySelector('#benchOut .badmark')"))
        await go("531-1-1-A_ZoneID.html")
        await pg.click("#b_kc_1_code"); await pg.keyboard.type("KIT-PSU-01"); await pg.keyboard.press("Enter")
        await pg.select_option("#b_kc_1_cls", "Rail kit"); await pg.select_option("#b_kc_1_hd", "Team lift"); await pg.wait_for_timeout(50)
        check("1-1 kit row is not graded live", "does not fit" not in (await pg.inner_text("#b_kc_1_code_st")))
        await pg.click("#benchPanel button.primary"); await pg.wait_for_timeout(80)
        check("1-1 kit row graded at build", "does not fit" in (await pg.inner_text("#benchOut")))
        await go("531-1-2-A_CustodyWalk.html")
        await pg.fill("#b_tr_1_tag", "DBD-01"); await pg.fill("#b_tr_2_tag", "DBD-02"); await pg.keyboard.press("Enter"); await pg.evaluate("buildBench()"); await pg.wait_for_timeout(80)
        check("1-2 same-tag check across rows", "same tag" in (await pg.inner_text("#benchOut")).lower())
        s13 = rd("531-1-3-A_HazardWalk.html")
        check("1-3 six hazard rows, unused rows optional", 'id="b_hz_6_where"' in s13 and s13.count('data-opt="1"') == 5)
        s42 = rd("531-4-2-A_RackStack.html")
        check("4-2 SBA result row for the instructor", 'id="b_sba"' in s42 and "Click the lowest U" in s42)
        await go("531-2-2-A_RMACycle.html")
        check("2-2 custody log can drop its last row", await pg.evaluate("!!document.getElementById('custUndo')"))
        for i_, v in [("cl_when","09:00"),("cl_from","DCT"),("cl_to","Bench"),("cl_cond","Sealed")]: await pg.fill("#"+i_, v)
        await pg.select_option("#cl_sig", "Release only"); await pg.click("text=Add custody entry"); await pg.wait_for_timeout(50)
        await pg.click("#btnSheet"); await pg.wait_for_timeout(80)
        st = await pg.inner_text("#sheetOut")
        check("2-2 sheet flags a single-signature row", "signature" in st.lower() and "Open items" in st)
        check("2-2 gate box lists the ways to fail", await pg.evaluate("!!document.querySelector('.gatebox')"))
        check("2-2 pill 1 not green with open items", not await pg.evaluate("document.getElementById('ps1').classList.contains('done')"))
        s22 = rd("531-2-2-A_RMACycle.html")
        check("2-2 advance-time waits for the cage entry", "custRows().length<3" in s22 and 'val("cl_seal")||"—"' in s22)
        s21 = rd("531-2-1-A_AssetTag.html")
        await go("531-2-1-A_AssetTag.html"); await pg.click("#btnSheet"); await pg.click("#lqBuild"); await pg.wait_for_timeout(100)
        check("PDF lists the simulator record's open items", "simulator record:" in (await pg.inner_text("#lqOut")).lower() and "Complete." not in await pg.inner_text("#lqOut"))
        check("2-1 sheet counts the exception record", "Bench complete." not in s21 and "Simulator record complete." in s21 and ".toUpperCase()" in s21.split("function scan(")[1][:600])
        s51 = rd("531-5-1-A_Decom.html")
        check("5-1 custody log named and signature pointed at the bench", "the custody log (each step" in s51 and "re-take on a different set" not in s51 and 'id="bg_ini"' in s51)
        s41 = rd("531-4-1-A_Warranty.html")
        check("4-1 no literal entity in the record", '" &middot; expires "' not in s41)
        check("0-1 says single build, not Set -", "single build" in rd("531-0-1_PlatformCheck.html") and '"set":"-"' not in rd("531-0-1_PlatformCheck.html") and 'SETLETTER="-"' not in rd("531-0-1_PlatformCheck.html") and 'BENCH.set||"—"' not in rd("531-0-1_PlatformCheck.html"))
        s52 = rd("531-5-2-A_Disposition.html")
        check("5-2 form fields carry examples", 'placeholder="e.g. DECOM-2026' in s52)
        check("3, 4, 5 panels carry handout step numbers", "Steps 4&ndash;5 &mdash; the path" in s41 and "Part 2 (Steps 4&ndash;6)" in rd("531-5-1-A_Decom.html"))
        h21 = "\n".join(p.text for p in docx.Document(os.path.join(OUT, "3_Handouts", "531-2-1_GLAB_Asset_Tagging.docx")).paragraphs)
        h42 = "\n".join(p.text for p in docx.Document(os.path.join(OUT, "3_Handouts", "531-4-2_GLAB_Rack_Stack.docx")).paragraphs)
        h13 = "\n".join(p.text for p in docx.Document(os.path.join(OUT, "3_Handouts", "531-1-3_GLAB_PPE_Hazard_Walkdown.docx")).paragraphs)
        h22 = "\n".join(p.text for p in docx.Document(os.path.join(OUT, "3_Handouts", "531-2-2_GLAB_RMA_Custody.docx")).paragraphs)
        check("handout copy fixes", "three non-standard" in h21 and "Two of the three routes" in h42 and "each route you rejected" in h42 and "Put on the PPE" not in h13 and "Custody log (Stage 3 panel)" in h22)
        # ---- the browser Builder reproduces the shipped tools and reports Apply changes beside its button
        await go("531_Builder.html")
        drift = []
        for f in ["531-0-1_PlatformCheck.html", "531-1-1-A_ZoneID.html", "531-1-3-A_HazardWalk.html", "531-2-2-A_RMACycle.html", "531-5-1-A_Decom.html", "531-5-2-A_Disposition.html"]:
            lid = f[4:7]; setl = f[8] if f[7] == "-" and f[8].isalpha() else ""
            shipped = rd(f)
            out = await pg.evaluate("([s,l,t])=>rebuild(s,l,t)", [shipped, lid, setl])
            if out != shipped: drift.append(f)
        check("Builder rebuild is byte-identical to the shipped tools", not drift, drift)
        await pg.click("button:has-text('Rebuild all (no download)')"); await pg.wait_for_timeout(50)
        check("Builder says how to load tools when none are loaded", "Choose Files" in (await pg.inner_text("#log")).split("\n")[-1])
        # form editor: one panel per lab, plain fields; the JSON lives under Advanced
        check("Builder section 2 is a form, no JSON anywhere", await pg.evaluate("!!document.querySelector('#specForm details[data-lab=\"1-2\"]') && !document.getElementById('specBox') && !document.querySelector('textarea[spellcheck=false]')"))
        await pg.evaluate("document.querySelector('#specForm details[data-lab=\"1-2\"]').open=true")
        await pg.fill('#specForm [data-path="LABS.1-2.minutes"]', "31")
        await pg.fill('#specForm [data-path="LABS.1-2.steps.2.t"]', "Step 9. Edited at the bench.")
        await pg.fill('#specForm [data-path="LABS.1-2.fields.0.fields.1.label"]', "When (time)")
        await pg.click("button:has-text('Apply changes')"); await pg.wait_for_timeout(50)
        check("form edits apply", await pg.evaluate("SPEC.LABS['1-2'].minutes===31 && SPEC.LABS['1-2'].steps[2].t==='Step 9. Edited at the bench.' && SPEC.LABS['1-2'].fields[0].fields[1].label==='When (time)'"))
        out12 = await pg.evaluate("([s,l,t])=>rebuild(s,l,t)", [rd("531-1-2-A_CustodyWalk.html"), "1-2", "A"])
        check("rebuilt tool carries the form edits", "~31 min" in out12 and "When (time)" in out12 and "Edited at the bench" in out12)
        await pg.fill('#specForm [data-path="LABS.1-2.steps.2.t"]', "Edited without a step number")
        await pg.click("button:has-text('Apply changes')"); await pg.wait_for_timeout(50)
        check("form apply reports a bad step beside the button", "not applied" in (await pg.inner_text("#specOut")).lower())
        await pg.click("button:has-text('Reset to the shipped definitions')"); await pg.click("button:has-text('Apply changes')"); await pg.wait_for_timeout(50)
        check("Builder confirms a good apply beside the button", "applied" in (await pg.inner_text("#specOut")).lower() and "not applied" not in (await pg.inner_text("#specOut")).lower())
        check("no page errors", not errs, errs[:2])
        await b.close()
asyncio.run(main())
print("learner checks:", "all passed" if not fails else f"{len(fails)} failed")
sys.exit(1 if fails else 0)
