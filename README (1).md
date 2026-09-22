# Module 531 — build scripts (learner-safe half)

These scripts regenerate the lab tools, handouts, the label sheet and the browser builder from the bench
definitions in `spec.py`. This folder contains **no answer keys, seeds or rubric text** — those live in
`5_Instructor_ONLY/build/spec_keys.py`, which the instructor-side scripts load at run time. This folder may
sit on the public course site; the instructor-side folder must not.

    python3 gen_tools.py      # 29 lab tools (bench panel + question list)
    python3 gen_handouts.py   # 12 handouts (bench part; numbering checked against the tools)
    python3 gen_labels.py     # 5_Instructor_ONLY/531_Bench_Labels.html
    python3 gen_builder.py    # 4_Lab_Tools/531_Builder.html (the same rebuild, in a browser)
    python3 test_bench.py     # headless Chromium: every tool loads; scripted bench run
    python3 test_learner.py   # headless Chromium: the learner-flow checks from the 22 Sep learner audit (fails non-zero)
    python3 verify.py         # handout/tool question lockstep, office files open, filename cross-refs
    python3 audit.py          # learner-facing vocabulary audit

Environment: `SRC` = the previous package folder (v1.2 tools without a bench, or a v2.0+ package — its bench
additions are stripped first, so the rebuild is idempotent; `SRC_HAS_BENCH=0` tells gen_handouts the source handouts
have no bench part). `spec.SRC_ID` maps a renamed lab to its file name in the source package.
`OUT` = the output package folder, `DOCX_TEMPLATE` = any handout .docx (style source).
Requires python-docx, python-pptx, openpyxl, python-barcode, playwright (Chromium), pandoc.

Instructor-side scripts (`5_Instructor_ONLY/build`): `gen_ft.py` (facilitator builds, SET_KEY, tools README,
index page), `gen_docs1.py` (guide, rubrics, Kit Map, SBA), `gen_docs2.py` (blueprint, Canvas sheet, delivery
note, sign-off), `gen_decks.py`, `gen_quizzes.py`. Run them from that folder; they import this folder via
`../../4_Lab_Tools/build` and find `spec_keys.py` beside themselves (or via `BUILD_KEYS`).

Never hand-edit a tool's question list or a handout: change `spec.py`, regenerate both.
