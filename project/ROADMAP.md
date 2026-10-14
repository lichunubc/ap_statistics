# AP Statistics course roadmap

## Goal

Maintain one reusable, expandable Quarto course book for Chun Li's Maple Hill School AP Statistics course. Preserve editable chapters, original practice, datasets/provenance, activity code, objective mappings and reproducible tests across course iterations.

## Authorized expansion — October 14, 2026

Chun Li has authorized completion of **Topics 1.7–1.13**, followed by **all Topics 2.1–2.12**, one topic per hourly work session starting immediately. Follow [the detailed authoring and publication specification](UNIT_1_2_EXPANSION.md) and [the nineteen-topic execution queue](expansion-state.json). The specification includes exact Fall 2026 CED titles/pages, full LO/EK coverage, textbook-style explanations, visual activities, optional expandable derivations, one-question-at-a-time practice, original problem-bank storage, official past-exam sourcing, and release validation.

These nineteen topics are **queued, not implemented or published at setup**. The execution queue must record actual source, test, deployment and live-verification outcomes. Preserve the existing six topics and the five-unit navigation. The authorization does not extend to Units 3–5 or to additional schedules beyond this finite series.

## Five-unit navigation — October 13, 2026

The homepage is a five-unit overview using the exact unit titles supplied by Chun Li. Each unit has its own landing QMD in `Unit N/`. Unit 1 holds the original six topic cards and dataset introduction; Units 2–5 are clearly labelled **under construction**. They are navigation placeholders, not implemented course content. The separate `project/unit-status.json` records these states without changing the existing topic objective mappings.

Sidebar topic lists start collapsed and expand only through an explicit mouse or keyboard action. Whole-book navigation lives in `site/`; lesson files stay in their unit/topic folders. Development branches named `preview/**` run the existing workflow's render and complete test gate without publishing. Only main may save generated HTML or deploy.

## Current implementation — October 13, 2026

Topics **1.1–1.6** have independent main chapters under **Unit 1: Exploring One-Variable Data and Collecting Data**, with exact official topic titles. Topic **1.2 Variables** is implemented, not merely scheduled: units/variables/values, categorical versus quantitative data, discrete versus continuous data, parameters/statistics, category-code relabelling, three activities and ten worked original exercises.

The original Topic 1.1, 1.3 and 1.4 lessons are retained. Topic 1.5 keeps its three original lessons as included QMD sections; Topic 1.6 keeps its two original lessons. All existing public page addresses have compatibility outputs. No new Topic 1.4 content was developed in the 1.2/folder-reorganization session.

## Human-editable organization

All Unit 1 teaching sources are in `Unit 1/`, with independent `Topic 1.x/` folders. Shared quantitative engines/styles, canonical datasets/provenance, cross-topic practice and integration tests live in `Unit 1/Shared/`. The unit and topic READMEs explain which files to edit. Whole-book infrastructure remains at the root. See the actual [topic manifest](topic-status.json) for source state and paths.

## Validation and publication

The gate runs all existing quantitative/foundations/table/chart regressions plus Topic 1.2, structure and course-navigation checks. It verifies arithmetic, old/new links, official names, mobile/desktop behavior, keyboard controls, print restoration and native Quarto search. Quarto is pinned to 1.9.38. Source status is **implemented**; the GitHub Actions build/deployment, revision-matched live check and live navigation browser check independently establish publication. Do not infer completion from a past scheduled start time.

## Beyond the authorized expansion

Prioritize teaching feedback, accessibility and mathematical consistency. Topics 1.7–1.13 and 2.1–2.12 are now covered by the explicit October 14 authorization above; they are no longer merely an unscheduled backlog. Expansion into later units remains future work requiring separate authorization. Each new topic retains independent navigation and a unit/topic folder. Add topic cards to their unit landing page, not the homepage.

## Curriculum reference

College Board, AP Statistics Course and Exam Description, **effective Fall 2026**, checked October 13, 2026 and rechecked for the expansion on October 14. Printed pages: 1.1 pp.30–31; 1.2 pp.32–33; 1.3 p.34; 1.4 p.35; 1.5 p.36; 1.6 pp.37–38. Remaining Unit 1 topic pages are 39–54; Unit 2 topic pages are 62–77. Official source: https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description.pdf. Link the CED; do not upload secure AP Classroom material or the complete PDF.
