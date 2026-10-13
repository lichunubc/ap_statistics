# AP Statistics course roadmap

## Goal
Develop one maintainable, reusable course book that can eventually cover the full AP Statistics curriculum. Retain source chapters, original datasets, interactive components, diagrams, attribution, worked practice and tests for future iterations of Chun Li's Maple Hill School course.

## Authorized release sequence — October 13, 2026

| Topic | Session | Main deliverable |
|---|---|---|
| 1.1 | Immediate | Questions, populations, samples, data and context |
| 1.2 | 02:18 Vancouver time | Variables, parameter/statistic notation, classification and categorical relabelling |
| 1.3 | 03:19 Vancouver time | Frequency/relative-frequency tables, denominators and supported claims |
| 1.4 | 04:19 Vancouver time | Bar/pie charts, comparison, interpretation and chart design |

These are scheduled **start** times, not guaranteed completion times. The follow-on sessions are one-off ChatGPT development tasks; the repository's publishing workflow is triggered by source changes, not by an hourly content-generation cron. Each session must read the current repository and preserve earlier changes. Update the topic manifest using actual outcomes.

## Topic 1.3 implementation note

The Topic 1.3 authoring source, reusable tally/denominator/claim activities, original practice and automated browser tests are included. The topic manifest records **implemented** when committed; GitHub Actions and the public URL independently determine deployment status. The separate 1.2 and 1.4 sessions retain their original scope.

## Topic 1.4 implementation note

Topic 1.4 provides a stand-alone QMD chapter, reusable JS/CSS for categorical graphs and an independent browser test. It reuses the original hypothetical source summaries in `data/foundations.json` and maps to the Fall 2026 CED, printed page 35. A committed chapter is *implemented*; only the successful GitHub Actions deployment and a public URL check establish that it is live. The separate 1.2 session retains its own status.

## Following this release

Topics 1.5 and 1.6 are already implemented. Keep their URLs and regression tests intact. After the foundations release, prioritize consistency, student feedback and mathematical QA before adding further chapters.

Later work may adapt the existing 1.7–1.9 class material, then expand across the current official curriculum. This is a backlog, **not authorization for extra scheduled sessions**. Recheck the official CED before each addition; do not build the eventual course map from an obsolete unit structure.

## Definition of a reusable topic

A completed topic has: an editable QMD source; curriculum objective IDs and edition; meaningful examples; original practice and explanations; accessible interactive or visual assets where beneficial; explicit data provenance; a working printed reference state; tests; and a traceable commit/release record. An old lesson's source stays in version history when it is improved.

## Current curriculum reference

College Board, AP Statistics Course and Exam Description, effective Fall 2026. Foundations checked October 13, 2026: 1.1 pp.30–31; 1.2 pp.32–33; 1.3 p.34; 1.4 p.35. Do not upload the full CED or secure AP Classroom assets; link the official source.
