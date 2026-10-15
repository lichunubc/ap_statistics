# Problem Bank

A reusable bank for the Maple Hill School course. The first selection contains **20 questions** from the instructor-supplied Week 2 and Week 3 homework. The public repository contains reference metadata and the reader, **not the College Board questions, diagrams, answers, or original PDFs**.

## Student route

Open **Problem Bank: Selected Homework** in the course sidebar, or **Selected homework practice** near the end of Topics 1.2–1.6. Open the instructor-provided `mhs-week-2-3.practice.json` with the file picker. It is parsed locally; it is never sent to the website. Native radio choices, explicit checking, reset, expandable explanations, figure enlargement, and metadata search work after loading.

The file is retained in this tab's `sessionStorage` to support navigation between lessons. It is not placed in persistent `localStorage` or IndexedDB. Browser session restoration can preserve tab storage: use **Forget class file** to explicitly clear it, especially on shared computers. Learner answers exist only in page memory and are not submitted, graded remotely, or carried to another page.

## Layout and source of truth

- `catalog.json`: stable IDs, primary/secondary topic tags, source week/question/pages, skill tags, difficulty, and source-file SHA-256 fingerprints. No protected question content.
- `practice.qmd`: the public browsing page and coverage explanation.
- `practice-filter.lua`: attaches the appropriate bank to each topic without duplicating practice content in lesson source files.
- `assets/practice.js`, `assets/practice.css`, `assets/footer.html`: browser-only reader, scoped presentation, and inclusion.
- `tools/prepare_bank.py`: validates the catalogue and generates `assets/catalog.js` before rendering. Do not edit the generated file.
- `tests/check_bank.py`: source-boundary, navigation, browser import, keyboard, feedback, reset, malformed-file, and mobile regression checks. Its generated test fixtures are deliberately unrelated to the homework.
- `local-content/`: **ignored, never committed, and never copied to Pages**. The separately delivered instructor archive contains one JSON per question, original figure assets, source PDFs, selection-review notes, and a class-file builder in this layout.

IDs use `MHS-W02-Q015` (Week 2, original Question 15). Keep source numbering stable even when the lesson sequence changes. Primary topic controls placement; secondary topics describe overlap without silently duplicating a question across lessons.

## Selection

| Topic | Source questions | Selection rationale |
|---|---|---|
| 1.1 | None | No direct introductory statistical-investigation question was present; the existing original practice is retained. |
| 1.2 | Week 2: 1, 3, 4, 6 | Continuous measurements, quantitative versus categorical variables, recording rules, and category observations versus category counts. |
| 1.3 | Week 2: 15, 17, 18, 20 | Validate a relative-frequency table, avoid turning percentages into unsupported counts, read frequencies, and combine categories with a common denominator. |
| 1.4 | Week 2: 16, 22, 24, 25 | Rates versus counts, pie-chart proportions, known-denominator conversion, and percentage denominators. |
| 1.5 | Week 3: 10, 16, 17 | Histogram rebinning, a split stemplot bridge to descriptions, and constructing a stemplot while retaining duplicates. |
| 1.6 | Week 3: 1, 3, 8, 12, 19 | Back-to-back skewness, multiple modes and gaps, a right tail, a visually potential outlier, and approximate uniformity. |

Week 3 Question 16 is tagged secondarily to 1.6. Week 3 numerical-summary questions are not reassigned to graphical topics just to increase the count. Difficulty labels and selection rationales are editorial judgments, not official College Board classifications.

## Publication boundary

The supplied PDFs are labelled College Board test booklets and appear to be AP Classroom exports. Public redistribution permission has not been established. See the **Intellectual Property** section of the [AP Services Terms of Service](https://secure-media.collegeboard.org/apc/ap-services-terms-conditions.pdf). Do not commit source content, publish the class file, upload it as a public release artifact, or assume that a hidden HTML block/password prompt protects public assets.

This reader is **not an access-control system** and does not grant redistribution rights. It simply displays a file the learner already possesses through authorized classroom arrangements. Confirm applicable permission before distributing any derived class file or changing delivery to public hosting. An instructor archive is provided separately for local review; it does not belong in Git history.

No official answer key was provided. The local package clearly labels its explanations as independently derived. The original figures are retained rather than redrawn, tables are transcribed, and the damaged `$200 to $100` formatting in Week 3 Question 10 is explicitly noted at the question.

## Maintenance

Run `python "Problem Bank/tools/prepare_bank.py"`, `quarto render`, then `python tools/check_all.py`. To run only the bank gate: `python "Problem Bank/tests/check_bank.py"`. `BANK_BASE_URL` runs the same browser checks against the deployed website. Never use real classroom content as a public CI fixture.

## Public original question bank

Separately from copyright-restricted homework references, instructor-authored questions for each new lesson are stored as structured JSON. Topic 1.7: `original/unit-1/topic-1-7.json` (ten original questions, keys, hints, worked explanations, objective tags and provenance). The Quarto `original-practice-filter.lua` gives a no-JavaScript fallback from the same JSON, while `assets/original-practice.js` supports the one-at-a-time reader. Keep original and locally restricted bank types separate.

Topic 1.8: `original/unit-1/topic-1-8.json` stores nine original questions with stable IDs, solutions, difficulty and objective tags. Unlike the private College Board homework references, these instructor-authored problems appear directly on the public lesson and require no file upload.

Topic 1.9: `original/unit-1/topic-1-9.json` contains ten new instructor-authored comparative-distribution and z-score questions, using exactly the same public one-at-a-time reader and no-JavaScript fallback. The referenced official 2026 exam remains linked externally; its original questions, images and scoring guide are not republished.
