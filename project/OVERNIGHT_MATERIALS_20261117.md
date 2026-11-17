# November 17 overnight materials — finite publication campaign

## Baseline and release boundary
Public repository: lichunubc/ap_statistics. Baseline main: afd3ebec03b5c6eed70da3dfacc2ec545751ef3c (2026-11-17). Source-verified live: Topics 1.1–1.11. Main production workflow 42569947586 passed November 9. At baseline: no open PRs and no active expansion claim. Working branch: preview/overnight-materials-20261117.

Only Topics 1.1–1.13 and 2.1–2.7 are in scope. Do not extend into 2.8–2.12 or Units 3–5. No status becomes published until preview checks, production deploy and revision-matched live confirmation.

## Actual source bytes inspected
- Latest probability slide source package MHS_AP_Statistics_Topics_2_3_to_2_7_Revised_v2_Quarto_Slides.zip: 637302 bytes; SHA-256 **95f9c61c4c735e479b6f73b19481f8a714750cb5e4520361ebd074ee2a5ffd19**; conversation file ID file_00000000d1b081fdbf925773491fc1b7. ZIP includes editable slides.qmd, CSS, JavaScript, six simulation CSVs, HTML/PDF and validator/test suite. It has 42 slides with new fair-device/sample-space introduction. **Inventory only; not yet integrated or publicly shipped.** Inspect for third-party content, source/data reproducibility and output validation before commit.
- Mixed probability guide MHS_AP_Statistics_Topics_2_3_to_2_7_Study_Guide_Overleaf.zip: 3290219 bytes; SHA-256 **f3e9fa86eb814c55541487a2dca1fab380cbae45becc2435be8b7744d2fb4f30**; conversation ID file_00000000150481fda2ab5a16fe0966c6. Contains private homework-derived sections/17b_practice_hw.tex and corresponding sections/21b_solutions_hw.tex. **Do not publish this original, its PDF or those two sections.** Public-safe derivative must remove the restricted practice and solutions, then rebuild from retained original teaching examples and public-original exercises. Check Venn labels “52 cards” and “H: hearts” visually in newly rendered output; an earlier edit still left overlap.
- Week 9 HW.pdf and its question content are private instructor materials, not a public repo resource.

## Work completed in this session
- Verified main Git tree, open PRs, recent Actions, live-topic manifest, exact new-lesson gap, student presentation guide, original public practice format, Quarto navigation and incumbent check suite.
- Checked official Fall 2026 CED Topic 1.12 printed p. 50 and independently authored a **public-safe Topic 1.12** chapter (bias, sampling variability, all five problem types, worked example), an accessible comparison of complete-frame SRS and walker-only convenience samples, eight original public questions with solutions, objectives mapping, source and tests.
- Staged topic integration on the preview branch; treat the new chapter as a **preview candidate**, not verified live, until CI and subsequent release prove that status.

## Remaining work
Complete preview CI; fix any genuine issues; recover 1.13 approved sources and instructor-specific corrections; recover 2.1–2.2 café resources; build independent 2.3–2.7 topic pages and integrate the 42-slide deck and clean public-safe study guide; finish integration privacy and live checks. Reserve final run for independently verified coverage and exact blockers. Do not create more automation sessions.
