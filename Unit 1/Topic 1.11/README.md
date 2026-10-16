# Topic 1.11 — Random Sampling

Main chapter: `topic-1-11.qmd`. Official Fall 2026 CED: printed pp. 48–49, PDF pages zero-indexed 52–53. Required LOs 1.11.A and 1.11.B; EK 1.11.A.1–A.6 and 1.11.B.1; skills 2.A, 2.B. See `objectives.json` for section-by-section alignment. Interactive lab: `assets/sampling111.js`, `assets/sampling111.css`, `data/population.json`, and footer loader. Source data and formula checks: `tests/check_sampling111.py`; native Chromium UI tests: `tests/check_sampling111_browser.py`.

Original public practice (ten questions with stable IDs, tags, keys, explanations, and rubrics) is in `Problem Bank/original/unit-1/topic-1-11.json`; the lesson's `original-practice-host` reads this single canonical source. Protected course homework remains in the separate local-file reader.

The model population contains 36 intentionally constructed entries, mean 17 minutes, six heterogeneous clusters, and three strata. The list's periodic grouping deliberately makes a systematic step of six sensitive to its order. All original values are authored for teaching; see `data/README.md`. There are no real student data, accounts, persistent answers or analytics.

Official released-question images: 2025 AP Statistics Question 2, original pp. 4–5, generated from its public PDF by `tools/prepare_exam_figures.py` using `project/released-exam-figures.json`, never storing the original PDF. The source includes a separate accessible description and teacher's walkthrough in context. Editorial use is based on the instructor-reported permission recorded in `project/STUDENT_PRESENTATION.md`.

To validate: `quarto render`, `python tools/check_all.py`, and inspect `qa/topic-1-11-browser.json` and mobile screenshots. Do not mark published until production Pages workflow and revision-matched live checks pass.
