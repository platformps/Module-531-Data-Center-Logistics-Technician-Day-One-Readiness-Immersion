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
