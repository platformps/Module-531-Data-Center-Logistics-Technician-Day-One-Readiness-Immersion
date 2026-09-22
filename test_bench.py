import asyncio, os, sys, glob, json
from playwright.async_api import async_playwright
OUT=os.environ["OUT"]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1100,"height":900})
        errs=[]
        pg.on("console", lambda m: errs.append((m.type,m.text)) if m.type in ("error","warning") else None)
        pg.on("pageerror", lambda e: errs.append(("pageerror",str(e))))
        files=sorted(f for f in glob.glob(os.path.join(OUT,"4_Lab_Tools","*.html")) if "Builder" not in f and "index" not in f)
        bad=0
        for f in files:
            errs.clear()
            await pg.goto("file://"+f)
            await pg.wait_for_timeout(150)
            n=await pg.evaluate("document.querySelectorAll('#benchPanel input, #benchPanel select').length")
            q=await pg.evaluate("LQ.items.length")
            card=await pg.evaluate("!!document.getElementById('lqCard')")
            if errs or not card or n==0: bad+=1; print("FAIL",os.path.basename(f),errs[:3],n,card)
        print("loaded",len(files),"bad",bad)
        # scripted bench run on 2-1-A
        f=os.path.join(OUT,"4_Lab_Tools","531-2-1-A_AssetTag.html")
        errs.clear(); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        await pg.fill("#b_kg","2.8"); await pg.dispatch_event("#b_kg","input")
        print("num:",await pg.inner_text("#b_kg_st"))
        await pg.fill("#b_tagscan","ATL-00790"); await pg.press("#b_tagscan","Enter")
        print("scan:",await pg.inner_text("#b_tagscan_st"))
        await pg.fill("#b_tagscan","ATL-00791"); await pg.press("#b_tagscan","Enter")
        print("scan bad:",await pg.inner_text("#b_tagscan_st"))
        await pg.click("#benchPanel button.primary")
        print("bench sheet:",(await pg.inner_text("#benchOut"))[:300].replace("\n"," | "))
        await pg.click("#btnSheet")
        print("sheets:",await pg.evaluate("document.querySelectorAll('.sheet').length"))
        # reload persistence
        await pg.reload(); await pg.wait_for_timeout(150)
        print("persist kg:",await pg.input_value("#b_kg"), "scan st:",await pg.inner_text("#b_tagscan_st"))
        # seq on 1-1 (the lifecycle walk, v2.1)
        f=os.path.join(OUT,"4_Lab_Tools","531-1-1-A_ZoneID.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
        from spec import LC_CODES
        for c in LC_CODES:
            await pg.fill("#b_seq",c); await pg.press("#b_seq","Enter")
        print("seq:",await pg.inner_text("#b_seq_st"))
        # lock on 3-2
        f=os.path.join(OUT,"4_Lab_Tools","531-3-2-B_CycleCount.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        for c in ["DBD-01","DBD-02","DBD-02","ATL-00911","DBD-03"]:
            await pg.fill("#b_cnt",c); await pg.press("#b_cnt","Enter")
        print("dup:",await pg.inner_text("#b_cnt_st"))
        await pg.click("#b_cnt_lock"); print("lock:",await pg.inner_text("#b_cnt_st"))
        # lookup on 3-1
        f=os.path.join(OUT,"4_Lab_Tools","531-3-1-C_DCIM.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        await pg.fill("#b_fd_1_tag","atl-00903"); await pg.press("#b_fd_1_tag","Enter"); print("lookup:",await pg.inner_text("#b_fd_1_tag_st"))
        # match_path on 5-2
        f=os.path.join(OUT,"4_Lab_Tools","531-5-2-A_Disposition.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        await pg.select_option("#b_it_1_path","Scrap"); await pg.fill("#b_it_1_bin","BIN-DISPOSE"); await pg.press("#b_it_1_bin","Enter"); print("path:",await pg.inner_text("#b_it_1_bin_st"))
        # unique on 5-1
        f=os.path.join(OUT,"4_Lab_Tools","531-5-1-B_Decom.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        await pg.fill("#b_dr_1_bag","SB-1001"); await pg.press("#b_dr_1_bag","Enter"); await pg.fill("#b_dr_2_bag","SB-1001"); await pg.press("#b_dr_2_bag","Enter"); print("unique:",await pg.inner_text("#b_dr_2_bag_st"))
        # Build bench record on every tool (row-group tools once threw here)
        nb=0
        for f in files:
            errs.clear(); await pg.goto("file://"+f); await pg.wait_for_timeout(100)
            await pg.click("#benchPanel button.primary"); await pg.wait_for_timeout(50)
            ok=await pg.evaluate("!!document.querySelector('#benchOut .sheet')")
            if errs or not ok: nb+=1; print("BENCH BUILD FAIL",os.path.basename(f),errs[:2])
        print("bench record builds on",len(files)-nb,"of",len(files)); bad+=nb
        # print label popup on 2-2
        f=os.path.join(OUT,"4_Lab_Tools","531-2-2-B_RMACycle.html"); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
        async with pg.context.expect_page() as np_:
            await pg.click("text=Print label")
        lab=await np_.value; await lab.wait_for_load_state()
        print("label:",await lab.evaluate("document.querySelectorAll('svg rect').length"), await lab.inner_text(".c"))
        print("errs",errs)
        await b.close()
        return bad or bool(errs)
sys.exit(1 if asyncio.run(main()) else 0)
