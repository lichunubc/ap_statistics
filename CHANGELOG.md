# Changelog

## 2026-10-13 — Five-unit entrance and collapsed topic navigation

- Replaced homepage topic cards with five independently linked units using the exact supplied official unit titles. Moved the original six topic cards and dataset introduction into `Unit 1/unit-1.qmd` without changing any lesson or activity source.
- Added `Unit 2` through `Unit 5` landing pages labelled **Under construction**, with editing notes and no fictitious completed topics. Added the separate unit-status manifest.
- Set sidebar collapse depth and added an accessible, non-persistent disclosure button so topic lists start collapsed even on an active lesson. Unit-title links open the landing pages; mouse, Enter and Space operate the arrow button.
- Kept existing unit/topic folders, topic objective mappings, data, activity engines, legacy URLs and regression checks. Whole-book navigation assets/tests are in `site/`.
- Extended local and live navigation tests for five unit cards/pages, placeholder labels, keyboard/mouse disclosure, no-JavaScript links and desktop/tablet/phone layouts. The publishing workflow now supports non-publishing `preview/**` validation branches; only main can deploy. Build and live outcomes remain separately verified by GitHub Actions.

## 2026-10-13 — Topic 1.2 and independent Unit 1 structure

- Implemented Topic 1.2 **Variables**, aligned with Fall 2026 CED 1.2.A–C (pp.32–33): observational units, values, categorical/quantitative and discrete/continuous data, parameters/statistics, correct summary groups, and numerical category coding.
- Added three accessible activities (10 classification cases, four summary-role cases, four recoding modes) and ten original worked exercises. Quiz inputs start unselected and support keyboard operation, clear/next/restart and contextual explanations; print references and no-JavaScript answers are retained.
- Replaced topic-range navigation with one Unit 1 parent and six independent officially named topics. Moved teaching sources, topic assets, provenance and tests into `Unit 1/Topic 1.x/`; shared dependencies are documented under `Unit 1/Shared/`.
- Preserved all existing lesson content and activity engines, including the original 1.5/1.6 lessons as editable include sections. Generated compatibility pages preserve existing public URLs and anchors; datasets and unchanged engines have preservation checksums.
- Added layout/title/link/source checks, Topic 1.2 arithmetic and browser tests, native search/mobile-menu checks, a complete test runner and revision-matched live verification. The existing publishing workflow remains the publication route. Source inclusion does not by itself assert live deployment.

## 2026-10-13 — Topic 1.4 categorical charts

- Added `topic-1-4.qmd` with categorical bar and pie construction, appropriate baselines, sector angles, group comparisons, original practice and eight worked solutions.
- Added keyboard-accessible chart builders, a grouped count-versus-percentage comparison and five unselected-initial-state audit questions with explanatory feedback.
- Preserved the School A/B, movie-satisfaction and study-location hypothetical datasets and their provenance; added static screen tables and print-ready references.
- Added dedicated Topic 1.4 browser/arithmetic tests, navigation, curriculum mapping and deployment verification. Topic 1.2 is managed independently.

## 2026-10-13 — Topic 1.3 categorical tables

- Added `topic-1-3.qmd`: frequency/relative-frequency tables, percentages, labelled ratios, correct denominators, modal category versus majority, justified claims, and seven original problems with full answers.
- Added keyboard-accessible tally construction (one/five/all/reset), part-to-whole/part-to-part denominator explorer, and four neutral-initial-state evidence checkpoints with explanations.
- Reused the synthetic School A survey and distinct study-location/movie examples from `data/foundations.json`, without creating fictitious raw records or altering the quantitative sample.
- Added reusable `assets/categorical-tables.js` and CSS, accessible static and print references, automated arithmetic/browser/desktop/mobile checks, navigation and curriculum mapping.
- Retained all Topics 1.1 and 1.5–1.6 source chapters and URLs. The workflow records independent build, test, and deployment results.

## 2026-10-13 — Foundations release 1 (Topic 1.1)

- Added `topic-1-1.qmd`: population/sample/data/context, investigative-versus-survey questions, consistent recording rules and six original practice problems with worked answers.
- Added a fixed-population selection explorer and three-case question workshop with neutral initial answers, reset, keyboard controls and static print references.
- Retained the separate 40-response categorical and 24-time quantitative examples; recorded the reusable foundations datasets and provenance.
- Broadened book branding to **AP Statistics: Learning from Data**, preserving all existing 1.5–1.6 URLs.
- Added an authoring template, contributor guide, curriculum/topic manifest and roadmap for future course iterations.
- Made preview navigation follow the configured chapters; retained the existing regression suite and added foundations tests to publishing.

Source release status and the scheduled follow-on topics are tracked in `project/topic-status.json`. GitHub Actions is the source of truth for build/deployment outcomes.
