# Module 531 Lab Tools

**Data Center Logistics Technician — Day-One Readiness Immersion**

Thirty self-contained, browser-based lab simulators for the twelve labs in Module 531. Each tool is a single HTML file with no dependencies, no network calls, and no build step. Open it in any current browser and the lab is ready to run — from GitHub Pages, from Canvas file storage, or straight off a USB stick.

> **Learner-safe.** This repository contains only learner-facing files. Answer keys, facilitator (`_FT`) builds, the `SET_KEY`, and the Facilitator Guide live in the separate `5_Instructor_ONLY` package and must never be committed here. See [What must stay out of this repo](#what-must-stay-out-of-this-repo).

---

## Quick start

| Audience | Do this |
|---|---|
| **Learner** | Open the file your instructor assigned (or use the [lab index](index.html)), work the panels, answer every numbered question, press **Build submission PDF**, upload the PDF to Canvas. Full steps [below](#how-a-learner-uses-a-tool). |
| **Instructor** | Assign one scenario **set** per learner (A / B / C). The set letter is deliberately meaningless to learners. Grade against the rubric in the instructor package. |
| **Hosting / Canvas admin** | Turn on GitHub Pages for this repo (Settings → Pages → Deploy from branch → `main` / root). Link Canvas assignments to the individual file URLs. Details [below](#hosting-on-github-pages). |

---

## The labs

Lettered files are alternate **scenario sets** of the same lab — different data, same questions and rubric. A learner runs exactly one set and hands in exactly one PDF. Labs without a letter have a single scenario.

| Lab | Title | Lesson | Time | Sets |
|---|---|---|---|---|
| GLAB 531.0.1 | Platform Readiness Check | 531.0 | ~30 min | [single](531-0-1_PlatformCheck.html) |
| GLAB 531.1.1 | Zone and Hardware Identification | 531.1 | ~20 min | [A](531-1-1-A_ZoneID.html) · [B](531-1-1-B_ZoneID.html) |
| GLAB 531.1.2 | Chain-of-Custody Walkthrough | 531.1 | ~15 min | [A](531-1-2-A_CustodyWalk.html) · [B](531-1-2-B_CustodyWalk.html) |
| GLAB 531.1.3 | Asset Lifecycle Sequencing | 531.1 | ~15 min | [single](531-1-3_Lifecycle.html) |
| GLAB 531.1.4 | PPE and Hazard Recognition Walkdown | 531.1 | ~50 min | [A](531-1-4-A_HazardWalk.html) · [B](531-1-4-B_HazardWalk.html) |
| GLAB 531.2.1 | Asset Tagging and Scan Verification | 531.2 | ~50 min | [A](531-2-1-A_AssetTag.html) · [B](531-2-1-B_AssetTag.html) · [C](531-2-1-C_AssetTag.html) |
| GLAB 531.2.2 | End-to-End RMA with Chain-of-Custody | 531.2 | ~70 min | [A](531-2-2-A_RMACycle.html) · [B](531-2-2-B_RMACycle.html) · [C](531-2-2-C_RMACycle.html) |
| GLAB 531.3.1 | DCIM Asset Records | 531.3 | ~50 min | [A](531-3-1-A_DCIM.html) · [B](531-3-1-B_DCIM.html) · [C](531-3-1-C_DCIM.html) |
| GLAB 531.3.2 | Cycle Count and Variance Investigation | 531.3 | ~60 min | [A](531-3-2-A_CycleCount.html) · [B](531-3-2-B_CycleCount.html) · [C](531-3-2-C_CycleCount.html) |
| GLAB 531.4.1 | Warranty Claim and Return Processing | 531.4 | ~60 min | [A](531-4-1-A_Warranty.html) · [B](531-4-1-B_Warranty.html) |
| GLAB 531.4.2 | Rack and Stack Move | 531.4 | ~70 min | [A](531-4-2-A_RackStack.html) · [B](531-4-2-B_RackStack.html) |
| GLAB 531.5.1 | Secure Decommission | 531.5 | ~50 min | [A](531-5-1-A_Decom.html) · [B](531-5-1-B_Decom.html) · [C](531-5-1-C_Decom.html) |
| GLAB 531.5.2 | Disposition and Sanitization Records | 531.5 | ~40 min | [A](531-5-2-A_Disposition.html) · [B](531-5-2-B_Disposition.html) · [C](531-5-2-C_Disposition.html) |

### File naming

```
531-<lesson>-<lab>[-<set>]_<ShortName>.html
        │       │      │
        │       │      └─ scenario set letter (omitted for single-scenario labs)
        │       └──────── lab number within the lesson
        └──────────────── lesson number (0–5)
```

Example: `531-3-2-B_CycleCount.html` is GLAB 531.3.2, scenario set B.

---

## How a learner uses a tool

1. Open the file the instructor assigned. Every tool opens with a short *How this tool works* brief at the top.
2. Work through the simulator panels. Where the lab has a simulator record, press **Build submission sheet** when the panels are complete — the sheet is harvested into the PDF automatically.
3. Answer every numbered question in the submission panel at the bottom. Question numbering matches the printed handout exactly.
4. Press **Build submission PDF** and save it with the browser's own *Save as PDF* option. The tool suggests a filename in the form `Lastname_Firstname_531.x.y`.
5. Upload that single PDF to the matching Canvas assignment.

**Autosave.** Work is saved in the browser (`localStorage`) as the learner types, so a refresh or accidental tab close loses nothing. Attached photos are downscaled before storage so a phone image cannot overflow the browser's quota. Autosave is per-browser and per-device — a learner who switches machines mid-lab starts fresh.

**Other controls.** *Preview without printing* shows the assembled submission on screen. *Clear my responses* wipes the saved answers. *Restart simulator* resets the scenario panels without touching typed answers.

---

## Hosting on GitHub Pages

The tools need nothing from the server beyond static file delivery, so GitHub Pages works as-is.

1. Push this folder to the repository root on the `main` branch.
2. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)`**.
3. The site publishes at `https://<org>.github.io/<repo>/`. `index.html` is the landing page listing every lab; each tool is reachable at `https://<org>.github.io/<repo>/<filename>.html`.
4. The `.nojekyll` file in the root tells Pages to serve the files exactly as committed (no Jekyll processing).

**Linking from Canvas.** Point each Canvas assignment at the direct file URL for the set you want that section to run, or link the landing page and tell learners which set to open. Files may also be uploaded to Canvas file storage and opened from there — they behave identically.

**Repository visibility.** Public is fine for this folder; that is the whole reason the instructor material is kept separate. If the repository is private, GitHub Pages requires a plan that supports private Pages, and learners will need to be signed in.

---

## What must stay out of this repo

This folder, and only this folder, may be published to learners. The following carry answer keys and must never be committed here, even to a private branch:

- The `5_Instructor_ONLY` folder
- Any `*_FT.html` facilitator build
- `SET_KEY.md`
- The Facilitator Guide

Keep instructor material in Canvas instructor files or a private share. If any of it is committed by mistake, treat the repository history as compromised: remove the file, then rewrite history or recreate the repository before the next cohort.

---

## Updating the tools

Each tool is a single file. To change a scenario, edit that file directly — there is no shared library or build step. When you change a lab, update every set of that lab so the sets stay parallel, and re-check that question numbering still matches the handout.

Compatibility target: any current desktop or mobile browser. No browser extensions, plug-ins, or network access are required.

---

## License

See [LICENSE](LICENSE). These materials are course content belonging to Per Scholas; contact the curriculum team before reusing or redistributing them outside the program.
