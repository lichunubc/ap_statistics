# AP Statistics course roadmap

## Goal

Maintain one reusable, expandable Quarto course book for Chun Li's Maple Hill School AP Statistics course. Preserve editable chapters, original practice, datasets/provenance, activity code, objective mappings and reproducible tests across course iterations.

## Current implementation — October 13, 2026

Topics **1.1–1.6** have independent main chapters under **Unit 1: Exploring One-Variable Data and Collecting Data**, with exact official topic titles. Topic **1.2 Variables** is implemented, not merely scheduled: units/variables/values, categorical versus quantitative data, discrete versus continuous data, parameters/statistics, category-code relabelling, three activities and ten worked original exercises.

The original Topic 1.1, 1.3 and 1.4 lessons are retained. Topic 1.5 keeps its three original lessons as included QMD sections; Topic 1.6 keeps its two original lessons. All existing public page addresses have compatibility outputs. No new Topic 1.4 content was developed in the 1.2/folder-reorganization session.

## Human-editable organization

All Unit 1 teaching sources are in `Unit 1/`, with independent `Topic 1.x/` folders. Shared quantitative engines/styles, canonical datasets/provenance, cross-topic practice and integration tests live in `Unit 1/Shared/`. The unit and topic READMEs explain which files to edit. Whole-book infrastructure remains at the root. See the actual [topic manifest](topic-status.json) for source state and paths.

## Validation and publication

The gate runs all existing quantitative/foundations/table/chart regressions plus new Topic 1.2 and structure checks. It verifies arithmetic, old/new links, official names, mobile/desktop behavior, keyboard controls, print restoration and native Quarto search. Quarto is pinned to 1.9.38. Source status is **implemented**; the GitHub Actions build/deployment and revision-matched live check independently establish publication. Do not infer completion from a past scheduled start time.

## Backlog, not a schedule

Prioritize teaching feedback, accessibility and mathematical consistency before expanding the book. Future work may adapt Topics 1.7 onward and later units after rechecking the current official CED. Each new topic should retain the same independent navigation and unit/topic folder structure. No additional scheduled development sessions are created by this roadmap.

## Curriculum reference

College Board, AP Statistics Course and Exam Description, **effective Fall 2026**, checked October 13, 2026. Printed pages: 1.1 pp.30–31; 1.2 pp.32–33; 1.3 p.34; 1.4 p.35; 1.5 p.36; 1.6 pp.37–38. Official source: https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description.pdf. Link the CED; do not upload secure AP Classroom material or the complete PDF.
