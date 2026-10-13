# AP Statistics · Maple Hill School

**Learning from Data** is Chun Li's interactive Quarto course book.

Student site: **https://lichunubc.github.io/ap_statistics/**

## Five-unit course entrance

The welcome page (`index.qmd`) shows the five officially named units. Each card opens its own `Unit N/unit-N.qmd` landing page. **Unit 1** contains the six existing topic cards and the dataset introduction; **Units 2–5 are under construction**, with no unpublished topics presented as finished lessons.

Sidebar topic lists start collapsed on every page load. A unit title opens its landing page; the adjacent keyboard-accessible arrow button shows/hides its topics. Whole-book navigation assets and tests live in `site/`, not inside any one topic. [Unit status](project/unit-status.json) records the five landing pages independently of the detailed topic manifest.

## Unit 1: one independently named chapter per topic

The book has separate chapters for Topics 1.1–1.6, using the exact titles in the **College Board CED effective Fall 2026**. Topic 1.2 **Variables** includes observational units, categorical/quantitative and discrete/continuous classification, parameters/statistics, category-code relabelling, three activities and ten fully worked original exercises. This is not yet a complete Unit 1 or AP Statistics course.

Open [Unit 1](<Unit 1/README.md>) to find a lesson's editable files. Each **Topic 1.x** folder contains its main QMD chapter, objective mapping, local activity/data/test files and editing notes. **Shared** contains assets, datasets and tests used across topics. The original Topics 1.5 and 1.6 lessons remain as `_*.qmd` sections in their own topic folders. Nothing from their activities or datasets has been discarded.

The sidebar has one **Unit 1** parent with the six official topics as direct children—not a “1.1–1.4” group. Existing chapter and asset URLs remain available through generated compatibility copies. Edit sources, never the generated `docs/` or compatibility pages.

## Preview and validate

```sh
quarto preview
quarto render
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tools/check_all.py
```

The workflow pins Quarto **1.9.38**. `tools/prepare.py` regenerates browser data from the canonical shared JSON. `tools/postrender.py` preserves old URLs, records the build revision and removes bundled fonts. Repository-wide settings, infrastructure and release history stay in `_quarto.yml`, `tools/`, `project/`, `site/`, `.github/` and this root documentation.

A Pandoc-only preview is also available with `python tools/preview.py`. It does not replace a genuine Quarto render. `CHROMIUM_PATH` selects a browser binary. In network-restricted sandboxes, `INLINE_BROWSER=1` exercises already-local rendered assets without navigation; native HTTP navigation/search are still required in CI. Reports and screenshots go in ignored `qa/`.

The complete test gate includes all existing quantitative, foundations, categorical-table and categorical-chart regressions, plus Topic 1.2 arithmetic, all 14 quiz cases, four recoding modes, neutral/reset/keyboard behavior, print restoration, no-JavaScript answers, official navigation, all legacy URLs, source-layout checks and desktop/tablet/mobile layouts. The course-navigation gate checks all five unit cards/pages, construction labels, collapsed topic lists, mouse/Enter/Space controls, no-JavaScript unit-to-topic links and page-reload behavior. GitHub Actions checks actual HTTP navigation, full-text search and the mobile menu before publishing.

## Publish and verify

The existing **Build and publish Quarto book** workflow renders and validates, saves generated HTML in `docs/`, and publishes via GitHub Pages. It refuses to publish stale output when main changes during validation. Development branches named `preview/**` run the same build/test gate without saving generated files or deploying; only main can publish.

Deployment verifies the release commit, every unit and topic, compatibility URLs, Topic 1.2 controls and data on the actual public site. It also runs the course-navigation browser checks against the live site at desktop, tablet and phone widths. A source commit or a successful build alone is not proof of live publication.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [topic status](project/topic-status.json), [roadmap](project/ROADMAP.md), and [CHANGELOG.md](CHANGELOG.md) before editing. Keep source, provenance and tests for future course iterations.

## Privacy and attribution

Do not publish real student records, credentials, private notes, secure AP Classroom questions or font files. Label hypothetical examples and distinguish the School A sample of 40 from the separate 24 quantitative commute values and 24 study-location responses. Original public dataset attributions remain in the source and book's resource chapter. There are no accounts, submissions, analytics or persistent quiz tracking. AP is a College Board trademark; this independent course book is not endorsed by the College Board.
