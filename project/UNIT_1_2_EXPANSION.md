# Unit 1 completion and Unit 2 expansion

Authorized by Chun Li on 2026-10-14. This is an actual lesson-authoring, testing and website-publication assignment, not a reminder to the instructor. The requested cadence is one topic per hour, starting immediately, in the order below. The finite automation provides 19 work sessions. Scheduled starts are not publication deadlines; failed validation must never be reported as completion.

## Source of truth and scope

- Repository: `lichunubc/ap_statistics`; student site: https://lichunubc.github.io/ap_statistics/.
- Curriculum: College Board, **AP Statistics Course and Exam Description, effective Fall 2026**, checked 2026-10-14: https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description.pdf.
- Use the revised **five-unit framework**, not the older nine-unit sequence. Unit 1 is **Exploring One-Variable Data and Collecting Data**. Unit 2 is **Probability, Random Variables, and Probability Distributions**.
- At setup, the source manifest and book navigation contain Topics 1.1–1.6; Unit 2 is a placeholder. The queue is therefore 1.7–1.13 and 2.1–2.12, nineteen new topics. Preserve the six existing topics and all earlier user edits.
- Read the complete official topic pages on every run, including all learning objectives (LOs), essential knowledge (EK), subpoints, and assigned skills. Do not rely only on the topic title or this plan. Record the exact LO/EK-to-section coverage in each topic's `objectives.json` and a compact coverage checklist. Formula extraction from the PDF can be garbled: inspect the original page image when needed.
- Page references below are the CED's **printed page numbers**. The PDF viewer's one-based page number is printed page + 5 for these pages.
- Curriculum scope comes from the CED. The visual activities below are proposed original teaching designs, not statements that College Board mandates these activities. Supplemental mathematics must be clearly separated from required coverage.

## Ordered queue

| Order | Topic | Exact official topic title | Printed CED pages | Proposed visual emphasis |
|---|---|---|---|---|
| 1 | 1.7 | Summary Statistics for One Quantitative Variable | 39–41 | Move observations on a dotplot; see the mean balance point, median/quartiles, squared deviations, resistance, and unit changes update together. |
| 2 | 1.8 | Graphical Representations of Summary Statistics for One Quantitative Variable | 42 | Build a five-number summary and boxplot step by step; distinguish fences, whiskers, and outlier observations. |
| 3 | 1.9 | Comparisons of the Distributions for One Quantitative Variable | 43–44 | Linked distributions on common scales, comparative evidence, and a z-score position explorer. |
| 4 | 1.10 | The Investigative Question Revisited and Data Collection | 45–47 | Build an investigative question and follow a study-design decision diagram; connect collection methods to permitted conclusions. |
| 5 | 1.11 | Random Sampling | 48–49 | Sample from a visible population using simple random, stratified, cluster, and systematic methods, with explicit replacement choices. |
| 6 | 1.12 | Potential Problems with Sampling | 50 | Compare a known population with biased sampling/response mechanisms; show why a larger sample need not remove systematic bias. |
| 7 | 1.13 | Experimental Design | 51–54 | Randomly allocate experimental units, compare blocking and matched pairs, and audit control, replication, blinding and causal conclusions. |
| 8 | 2.1 | Tabular and Graphical Representations for the Distributions of Two Categorical Variables | 62 | Link one two-way table to side-by-side bars, segmented bars and mosaic plots; switch counts and meaningful proportions. |
| 9 | 2.2 | Summary Statistics for Two Categorical Variables | 63 | Highlight the relevant cell, row/column and denominator for joint, marginal and conditional relative frequencies. |
| 10 | 2.3 | Estimating Probabilities Using Simulation | 64 | Animate a clearly defined trial and event; compare running relative frequencies across repeated simulation runs. |
| 11 | 2.4 | Introduction to Probability | 65 | Highlight events and complements in a sample space; show probabilities as proportions of probability mass. |
| 12 | 2.5 | Mutually Exclusive Events | 66 | Use event-region and outcome selectors to identify intersections and disjoint events. |
| 13 | 2.6 | Conditional Probability | 67 | Visually restrict the sample space; connect two-way tables and probability trees to conditional probability and the multiplication rule. |
| 14 | 2.7 | Independent Events and Unions of Events | 68 | Change event overlap, compare conditional and marginal probabilities, and visualize inclusion–exclusion. |
| 15 | 2.8 | Introduction to Random Variables and Probability Distributions | 69 | Map outcomes to numerical random-variable values; link probability mass and cumulative-probability displays. |
| 16 | 2.9 | Parameters of Random Variables | 70–71 | Move probability masses and watch the expected-value balance point and weighted squared deviations change. |
| 17 | 2.10 | The Binomial Distribution | 72–73 | Animate trials, vary n and p, shade exact/cumulative events, and compare simulated and theoretical distributions. |
| 18 | 2.11 | The Normal Distribution | 74–76 | Vary mean and standard deviation, shade tails/intervals, compare empirical-rule areas, and find percentile cutoffs. |
| 19 | 2.12 | Sampling Distributions and the Central Limit Theorem | 77 | Link population, an individual sample, and the distribution of sample means; vary sample size and separately demonstrate random reassignment. |

## Required student experience for every new topic

Write a self-contained, coherent **textbook-style chapter**, not a slide outline or a collection of formula lists. Begin with an understandable investigative context, identify prerequisites and learning targets, develop intuition before notation, explain every symbol and relevant unit, and give worked examples with reasoning and contextual conclusions. Include common misconceptions, brief checkpoints, and a final synthesis. Match depth to the topic's complete official scope; do not add filler to meet a word count. A student should be able to learn from the page without a lecture or an external textbook purchase.

Use purposeful interactive tools and visualizations wherever they improve understanding. Prefer a small number of well-designed linked activities over decorative animation. Each activity should ask students to predict or notice something and explain what the changing picture means. Include readable axes, scales, labels, legends, source/provenance, reset/pause/step controls where relevant, and a static explanation or table. Distinguish simulated data, hypothetical teaching examples and real observations. Simulations illustrate results; they are not proofs.

### Expandable derivations

For every distinct formula introduced in a chapter, provide a nearby collapsed, keyboard-accessible disclosure such as **Why does this work? — Derivation**. Use native `details`/`summary` or an equivalently accessible button with expanded-state semantics. The main reading path must contain the formula, its meaning, conditions and application; the derivation must not be required just to follow the lesson.

Where the derivation/proof goes beyond AP Statistics requirements, label it **Optional enrichment — this derivation is not required for AP Statistics**. Check that designation against the current CED. Do not hide required conceptual explanations or AP-required justifications behind an optional label. Clearly identify prerequisites such as expectation or calculus in advanced derivations. Provide a mathematically sound derivation, not merely a numerical example. A reused formula can link to its original derivation instead of repeating it.

Definitions, conventions and screening rules are not theorems. For these, retain an expandable **Why this definition/rule?** explanation and explicitly say there is no universal mathematical proof of the chosen convention; do not invent a proof for a 1.5-IQR cutoff or a quartile convention. For qualitative topics, do not manufacture formulas just to add derivations. Maintain a formula/disclosure inventory for testing.

### One compact practice panel per topic

At the end of each new lesson, present all its practice questions through **one question-at-a-time panel**, in one stable place on the page. Provide **Previous**, **Next question**, **Question k of N**, **Check answer** where appropriate, **Show hint**, **Show solution**, and **Reset question**. Use roughly 6–10 carefully chosen questions, adjusting upward only when needed for coverage; include conceptual/visual interpretation, calculation where applicable, and short written justification, not only multiple choice.

Changing questions must not reload the page or jump the reader to the top. Keep controls predictable, avoid a long stack of expanded questions, and let the student easily scroll upward to consult the notes. Allow the panel to grow naturally for a long question or solution rather than clipping it or forcing a tiny nested scrolling area. New questions start with no selected answer or revealed solution. Do not leak answers through question titles, option styling, or hints visible before interaction. Written responses should use a revealable rubric/model answer rather than claim reliable automatic semantic grading.

Store authored question content **once** in a dedicated original-content area under `Problem Bank/`, organized by unit/topic, with stable IDs, primary/secondary topic tags, LO/EK tags, difficulty, question type, prompt, data/figure references, choices where applicable, answer/rubric, hint, full explanation and provenance/rights classification. Reuse a shared reader; do not copy question strings into every lesson. Public original practice must work immediately without requiring the private class JSON. Preserve the existing separate local-file reader and the 20 selected homework references. Avoid changing the earlier six lessons wholesale; reuse their helpful UI patterns and keep regression coverage.

No learner accounts, submissions, analytics or persistent answer tracking. In-page answer state is sufficient. Provide an accessible no-JavaScript fallback and a printable view of the full practice set with controlled answer disclosure and restoration of screen state after printing.

## Worked-example sourcing

Before inventing a worked-example question, first search the official public past-exam archive for a genuinely suitable **released AP Statistics exam question**: https://apcentral.collegeboard.org/courses/ap-statistics/exam/past-exam-questions.

Inspect the original question and, where available, its official scoring guidelines. Cite year, question number, part and direct official source links. Map older questions to the **current** topic by content, not by their old unit numbers. A CED sample question is a sample question, not a past administered exam question. Never invent an exam attribution, a question number or an official answer. Keep a small per-topic source-search/selection record, including why no suitable public example was found when that is the case.

Respect existing public-republication boundaries: do not commit secure AP Classroom questions, the instructor's full homework PDFs/private question files, or entire copyrighted exam PDFs to this public repository. Link official originals and supply independently authored explanations/appropriately limited excerpts where necessary. Public availability alone does not establish republication permission. When a suitable real question cannot be used in full on the public page, preserve its source reference and walkthrough as appropriate, and provide a clearly labelled original worked example for a self-contained lesson. Original and adapted examples must be distinguished from real exam questions.

## Content checks that are easy to overlook

- **1.7:** cover all 1.7.A–F, not only mean/SD: position, percentiles, quartiles, range/IQR, sample variance and SD, units/transformations, outlier methods, comparisons, resistance and justified choices. The current CED lists both the 1.5-IQR method and a more-than-two-SD screening method. Explain them separately and in context rather than silently omitting either or claiming they always agree. State the quartile calculation convention and keep worked examples, tools and answers consistent. Distinguish sample and population denominators. Explain that n−1 makes sample variance unbiased under the usual sampling assumptions; do not claim sample SD itself is unbiased. Any advanced expectation proof is optional and names its assumptions.
- **1.8:** whiskers end at observed non-outlier values in a modified boxplot, not necessarily at the numerical fences. Boxplots do not reveal modes or gaps reliably. Treat mean-versus-median patterns as tendencies, not converses or universal laws.
- **1.9:** include z-scores and comparisons of relative position (1.9.D/E), as well as comparative descriptions. Standardizing does not itself make a distribution normal. Use context, common scales and numerical evidence.
- **1.10–1.13:** distinguish random selection from random assignment, observational from experimental units, observational study from experiment, confounding from an arbitrary third variable, sampling variability from bias, and generalization from causation. Cover the CED's prospective/retrospective studies, ethics and limits of conclusions. Do not imply randomization guarantees perfectly balanced groups. Include all required designs and their justification.
- **2.1/2.2/2.6:** make denominators unmistakable. A mosaic plot's cell area, group width and conditional height have different interpretations; unequal group totals must be represented correctly. Association is not causation.
- **2.3:** define random device, outcome coding, one trial, event, repetition and estimate. Handle replacement/independence assumptions and distinguish Monte Carlo variation from a mathematical guarantee of monotonic convergence.
- **2.4–2.7:** count favorable outcomes only when the relevant elementary outcomes are equally likely. Handle zero-probability conditioning explicitly. Independent and disjoint are not synonyms; for positive-probability events they cannot both hold. Show the overlap subtraction in the general addition rule.
- **2.8:** include cumulative distributions and distinguish random-variable values from elementary outcomes. Validate nonnegative probabilities that sum to one.
- **2.9/2.10:** distinguish expected value from a guaranteed or necessarily attainable outcome, and population distribution SD from sample SD. For binomial, check fixed n, independent binary trials and constant p; address exactly/at most/at least boundaries and include n,p edge cases in software tests.
- **2.11:** include all 2.11.A–F: shape and parameters, standard normal, empirical rule, interval/tail probabilities, inverse cutoff questions, extreme two-tail areas and relative-position comparisons. Use area rather than curve height for probability and state continuous point probability. Check calculator instructions against current documentation; keep the lesson usable without an external service.
- **2.12:** cover all 2.12.A.1–A.4, including randomization distributions, not just an animation of sample means. Keep population distribution, sample distribution and sampling distribution distinct. Explain CLT assumptions and why increasing the number of simulated samples is not the same as increasing sample size; do not claim all statistics become normal or that n=30 universally suffices. Advanced parameter derivations are labelled enrichment/forward connections when outside this topic's core requirements.

## Editable organization and integration

Read `README.md`, `CONTRIBUTING.md`, `_quarto.yml`, `project/ROADMAP.md`, `project/topic-status.json`, `project/unit-status.json`, this specification, the expansion state, adjacent topic sources and existing tests before editing. Do not assume a previous session succeeded.

Keep literal `Unit 1/Topic 1.x/` and `Unit 2/Topic 2.x/` directories. Each topic has its main `topic-1-7.qmd`-style filename, `README.md`, `objectives.json`, and its own assets, data/provenance and tests as needed. Share genuinely reusable widgets under the appropriate shared/site area. Keep reusable original questions under `Problem Bank/`; document the connection from topic READMEs.

Retain the five-unit homepage, unit landing pages, exact official names, independent sibling topics, initially collapsed sidebar topic lists, all legacy URLs and current branding. Add each new topic card to its unit landing page, not the homepage. When 2.1 is ready, make Unit 2 a proper book part with its own topic children and distinguish ready lessons from remaining under-construction topics. Keep Units 3–5 as they are. Update resource-copy globs and JS checks for new Unit 2/shared assets. Never edit generated `docs/` as the source.

Use existing Quarto/Pandoc math rendering and system fonts; never upload font files. Preserve original data/provenance and source attribution. Re-read current main before integrating, reconcile concurrent changes, and never force-push or replace the whole repository with an older snapshot.

## Per-session execution and publication gate

1. Read `project/expansion-state.json`. Select the earliest queued or incomplete topic in the specified order. Resume an unfinished topic rather than silently abandoning it. Work on **one topic**, plus shared infrastructure strictly needed for that topic.
2. Claim the topic in the state file with a run identifier, UTC start time and current source revision using a current blob SHA/optimistic concurrency check. If another session is demonstrably active, do not overwrite its work or start conflicting edits. A stale claim needs inspection of branch commits/Actions before recovery. Metadata-only checkpoint commits may use `[skip ci]`; real source releases must run the complete workflow.
3. Inspect the complete official topic source, map all LOs/EK, author the chapter, visual activities, derivations, examples and practice records. Prefer a `preview/**` development branch and retain recoverable work if blocked.
4. Independently verify every worked example, answer/rubric, formula/derivation, dataset total and chart. Add deterministic calculation tests and browser tests for the new widgets and compact practice reader. Test edge cases and reproducible simulation fixtures without presenting fixtures as real data.
5. Run a genuine `quarto render` and `python tools/check_all.py`, with required test dependencies. Extend the runner to include new topic tests. Existing navigation/structure tests may assume six topics or a Unit 2 placeholder: update these to derive correct expectations from manifests, without removing coverage or weakening checks to force a pass. Test all old and new URLs/assets, desktop/tablet/phone widths, keyboard/neutral/reset behavior, next/previous navigation, derivation disclosures, no-JS fallback, printing and screen-state restoration. Inspect screenshots and console/network errors. Native HTTP navigation/search must pass in CI; an inlined preview is not equivalent.
6. Update topic and unit manifests, objective maps, landing pages, relevant READMEs/roadmap and changelog. Integrate non-destructively into current main through the established workflow only after appropriate checks. Wait for the actual build/deployment result and verify the new live chapter and revision marker before using `published_verified`.
7. Record source commit, test results, Actions URL, live URL, checked revision, any artifact/branch and precise blockers in the expansion state and work log. Distinguish `queued`, `in_progress`, `source_ready`, `validation_failed`, `deployment_pending`, `blocked`, and `published_verified`. Release the active claim. Do not advance the queue merely because time elapsed or a file exists.
8. Send Chun Li a brief release report: topic, live link only when verified, main additions/visuals, derivation and practice coverage, validation and any blocker. On the last scheduled session, include an honest cumulative audit of all 13 Unit 1 and all 12 Unit 2 topics, with any remaining gaps. Stop when the requested scope is complete. Do not create more schedules, change hosting/sharing permissions, buy services or contact third parties.

The first run is Topic **1.7**. This authorization supersedes the older roadmap statement that expansion beyond 1.6 was only an unscheduled backlog. It does not authorize expansion into Units 3–5.
