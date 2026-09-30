# Module 531 — Lab tools

Twenty-nine lab tools for the twelve labs of **Module 531: Data Center Logistics Technician Day-One Readiness Immersion** (version 2.2). Each file opens straight
into its lab in any current browser — nothing to install, nothing to connect to.

Your instructor tells you which file to open. Files with a letter (A, B, C) are different versions of
the same lab: you run one, and you hand in one PDF.

## How to use a tool

1. Open the file your instructor assigns.
2. Work the panels in order. When the on-screen part is complete, press **Save simulator record**.
3. Do the hands-on part at your station and record it in the **bench panel**: click into a scan field
   and scan — the scanner types the code for you. Press **Save bench record** when you are done.
   **Print label** buttons print a label on the station's label printer.
4. Answer every question in the submission panel at the bottom. Each one carries its handout step number.
5. Press **Build submission PDF** and save it with your browser's Save as PDF. The suggested filename
   is `Lastname_Firstname_531.x.y`. Upload that one PDF to the matching Canvas assignment.

Your work is saved in this browser as you type, so a refresh loses nothing. Photos you attach are
shrunk before they are saved.

`index.html` lists every lab by lesson. `531_Builder.html` and the `build/` folder are for the people who
maintain the tools; they are not part of any lab.

## v2.3 — readability rework (29 September 2026)

Learner feedback on the labs: the instructions were vague and the colors made the tools hard to read. Every tool now:

- opens on a **How to work this lab** card — numbered steps naming the exact panel and button for each action, what you should see after it, a "you are finished when" list, and tips. It collapses (click the heading) and stays collapsed in that browser until you open it again. It does not print.
- uses a **light, high-contrast page** (white panels, near-black text, AA-checked colors) with a 12 px type floor and 15 px body text. Where a tool shows a console, chart or diagram, that part keeps its dark "screen" look on purpose.

The change is applied by `build/readability_patch.py` (with the guide text in `guides_531.py`), so it can be re-run over a regenerated set of tools. `build/test_readability.py` renders every tool headless and checks JS errors, the guide card, the type floor and contrast.

### Virtual bench (v2.3, same day)

The stations have no label printer and no physical kit, so every bench panel now opens on a **Virtual bench** card: the cards, tags, labels and serials the bench expects are on screen as Code 128 barcodes (scan them off the display with the field selected, or press the barcode's Scan button), and **Print label** puts the printed tag on the virtual bench instead of opening a print window. `build/bench_walk.py <folder>` walks every bench as a learner and reports which records complete.

## v2.4 — goals and scenario at the top (30 September 2026)

Review feedback on the labs: keep the detailed instruction and the lab walkthroughs, and move each lab's goals and scenario to the top in bold or contrasting text. Every tool now:

- opens on a **Goals + Scenario band** directly under the lab title and above the *How to work this lab* card — bold white text on navy, always visible, not collapsible. It does not print, so the submission PDF is unchanged.
- takes that wording from its own handout: the handout's *Learning Objectives* are the goals, and the first paragraph under its scenario heading is the scenario. Edit the handout, re-run the patch, and the tool follows.

The last goal in each lab — the bench goal — is restated for the **virtual bench** (scan from the screen, **Print label** puts the label on the virtual bench), in the handout and in the band alike. GLAB 531.1.3 keeps its walkdown goal, which is still done at the station.

Nothing else in any tool changed. Remove the block between the `GS_BRIEF` markers and each file is exactly its v2.3 version.

The twelve handouts carry the matching change: *Learning Objectives* and a new *Scenario* heading lead the document, in bold on a shaded block between two rules; *Introduction*, *Equipment / Requirements* and *Instructions* follow with their text unchanged.

The change is applied by `build/goals_scenario_patch.py <handouts folder> <tools folder>`. It is re-runnable (a second run changes nothing). Run it last, after any regeneration and after the readability patch, because it anchors on the guide card. `build/test_goals_scenario.py` checks the result.

## v2.5 — a wrong answer says so (30 September 2026)

Class request: when an answer is wrong, make it obvious — a sound, or the word in big letters. Every tool now does both.

When a check in the tool fails — a scan that is not the code the field expects, a tag that fails its scan check, a sequence out of order, a duplicate scan, a request the vendor portal rejects, a lookup that finds nothing — the screen shows **WRONG** in big letters, names the field or panel the answer was in, and says why in a full sentence ("Why: “KIT-SCAN-01” is not the code this field expects. Scan the card or tag named in the field's label, not a different one."). A short buzzer sounds. The box stays up until your next click or key, so there is time to read it.

- **Sound on / Sound off** is the switch in the bottom-left corner of the page. Your choice is remembered in that browser.
- A record that is only incomplete ("3 item(s) incomplete") is not called wrong, and neither is a reminder to do a step first.
- The tools check exactly what they checked before. Written answers and judgment calls are still assessed by your instructor.
- Nothing prints: the submission PDF is unchanged.

The change is applied by `build/wrong_signal_patch.py <tools folder>` (re-runnable; run it after any regeneration). `build/test_wrong_signal.py` checks it.
