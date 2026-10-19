# AP Statistics course roadmap

## Goal

Maintain one reusable, expandable Quarto course book for Chun Li's Maple Hill School AP Statistics course. Preserve editable chapters, original practice, datasets/provenance, activity code, objective mappings and reproducible tests across course iterations.

## Current release — October 19, 2026

Topic **1.11 Random Sampling** is now `published_verified`. The validated preview source `1698e719ff80015908ea16959ad5f160fb9b3ac5` was integrated into `main` by an expected-head, non-force fast-forward. Production workflow [39300078519](https://github.com/lichunubc/ap_statistics/actions/runs/39300078519) passed the pinned Quarto render, all **19** regression suites, generated-site commit, GitHub Pages deployment, revision-matched chapter verification, live unit navigation, live original problem bank, student-presentation checks and the Topic 1.11 random-sampling browser gate.

Topics **1.7–1.11 are verified live**. The next unfinished item in [the execution state](expansion-state.json) is **Topic 1.12 Potential Problems with Sampling**. Do not advance based only on a scheduled start, source commit or preview build.

## Resumed expansion — October 15–16, 2026

Chun Li explicitly requested continuation of the paused work. The non-force retry first integrated the already-tested Topic 1.9 branch into main. Topic 1.10 then required repair of a merged test-runner syntax error before production publication. Topic 1.11 was recovered from its complete preview source, corrected for objective-schema and 390-pixel overflow defects, and subsequently published through the complete release gate.

The existing hourly automation was resumed for **16 finite sessions**, starting October 15 at **10:51:45 a.m. Vancouver time** (17:51:45 UTC) and ending with its final planned start on October 16 at 1:51:45 a.m. Vancouver time. These were scheduled starts, not guaranteed release deadlines. Resume any incomplete release before advancing and report actual gaps honestly; never recreate a topic already verified live solely because an older note says it is unfinished.

## Authorized expansion — October 14, 2026

Chun Li authorized completion of **Topics 1.7–1.13**, followed by **all Topics 2.1–2.12**, one topic per work session. Follow [the detailed authoring and publication specification](UNIT_1_2_EXPANSION.md) and [the nineteen-topic execution queue](expansion-state.json). The specification includes exact Fall 2026 CED titles/pages, full LO/EK coverage, textbook-style explanations, visual activities, optional expandable derivations, one-question-at-a-time practice, original problem-bank storage, official past-exam sourcing, and release validation.

At setup these nineteen topics were queued. Consult the expansion state for current progress; it records actual source, test, deployment and live-verification outcomes. Preserve the existing lessons and five-unit navigation. The authorization does not extend to Units 3–5 or to additional schedules beyond the original finite series.

## Five-unit navigation — October 13, 2026

The homepage is a five-unit overview using the exact unit titles supplied by Chun Li. Each unit has its own landing QMD in `Unit N/`. Unit 1 holds its topic cards and dataset introduction; Units 2–5 are clearly labelled **under construction**. They are navigation placeholders, not implemented course content. The separate `project/unit-status.json` records these states without changing the existing topic objective mappings.

Sidebar topic lists start collapsed and expand only through an explicit mouse or keyboard action. Whole-book navigation lives in `site/`; lesson files stay in their unit/topic folders. Development branches named `preview/**` run the existing workflow's render and complete test gate without publishing. Only main may save generated HTML or deploy.

## Earlier implementation — October 13, 2026

Topics **1.1–1.6** have independent main chapters under **Unit 1: Exploring One-Variable Data and Collecting Data**, with exact official topic titles. Topic **1.2 Variables** is implemented, not merely scheduled: units/variables/values, categorical versus quantitative data, discrete versus continuous data, parameters/statistics, category-code relabelling, three activities and ten worked original exercises.

The original Topic 1.1, 1.3 and 1.4 lessons are retained. Topic 1.5 keeps its three original lessons as included QMD sections; Topic 1.6 keeps its two original lessons. All existing public page addresses have compatibility outputs. No new Topic 1.4 content was developed in the 1.2/folder-reorganization session.

## Human-editable organization

All Unit 1 teaching sources are in `Unit 1/`, with independent `Topic 1.x/` folders. Shared quantitative engines/styles, canonical datasets/provenance, cross-topic practice and integration tests live in `Unit 1/Shared/`. The unit and topic READMEs explain which files to edit. Whole-book infrastructure remains at the root. See the actual [topic manifest](topic-status.json) for source state and paths.

## Validation and publication

The gate retains all earlier regressions and adds each new topic's arithmetic and browser checks. It verifies arithmetic, old/new links, official names, mobile/desktop behavior, keyboard controls, print restoration, MathML and native Quarto search. Quarto is pinned to 1.9.38. Source status is **implemented**; GitHub Actions build/deployment, revision-matched live checks and live browser gates independently establish publication. Do not infer completion from a past scheduled start time.

## Beyond the authorized expansion

Prioritize teaching feedback, accessibility and mathematical consistency. Topics 1.7–1.13 and 2.1–2.12 are covered by the October 14 authorization and October 15 resumption; they are no longer merely an unscheduled backlog. Expansion into later units remains future work requiring separate authorization. Each new topic retains independent navigation and a unit/topic folder. Add topic cards to their unit landing page, not the homepage.

## Curriculum reference

College Board, AP Statistics Course and Exam Description, **effective Fall 2026**, checked October 13, 2026 and rechecked for the expansion. Printed pages: 1.1 pp.30–31; 1.2 pp.32–33; 1.3 p.34; 1.4 p.35; 1.5 p.36; 1.6 pp.37–38; remaining Unit 1 topic pages 39–54; Unit 2 topic pages 62–77. Current official source: https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf. Link the CED; do not upload secure AP Classroom material or the complete PDF.
