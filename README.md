# AP Statistics · Maple Hill School

**Learning from Data** is Chun Li's growing interactive Quarto course book.

Student site: **https://lichunubc.github.io/ap_statistics/**

The original Topics 1.5–1.6 pilot is preserved. Topic 1.1 develops questions, populations, samples and data. Topic 1.3 adds categorical tables, relative frequencies, ratios and evidence checks. Other foundation topics are developed in separate scheduled sessions. Read the [topic manifest](project/topic-status.json) for actual source status, the [roadmap](project/ROADMAP.md) for planned work, and [CHANGELOG.md](CHANGELOG.md) for released changes. Do not infer publication from a planned start time.

## Edit and extend

Read [CONTRIBUTING.md](CONTRIBUTING.md) and use [the topic template](templates/topic.qmd). Edit `.qmd` chapters rather than generated `docs/` files. The navigation and site settings are in `_quarto.yml`; reusable code/styles are in `assets/`; datasets and provenance are in `data/`. Preserve existing URLs and keep hypothetical examples separate from real observations.

```sh
quarto preview
quarto render
```

The existing GitHub Actions workflow installs Quarto 1.9.38, renders, checks JavaScript and browser behaviour, saves generated HTML to `docs/`, and publishes through GitHub Pages when configured. It uses the repository's workflow token; no personal access token or paid backend is needed. A successful build is not by itself proof of deployment: inspect **Publish site** and the live-site verification step.

## Portable local preview

The same chapter content can be rendered with Python and Pandoc:

```sh
python tools/preview.py
python -m http.server 8000 --directory docs
```

The preview follows the current `_quarto.yml` chapter list. The genuine Quarto build adds its native book navigation and search. Portable preview tests do not replace the Quarto CI build.

## Validation

```sh
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tools/check_site.py
python tools/check_foundations.py
python tools/check_categorical.py
```

`CHROMIUM_PATH` selects an existing Chromium binary. `INLINE_BROWSER=1` renders already-local assets in memory for environments that cannot navigate to a local web server. Reports/screenshots go in `qa/` and are excluded from source control. Checks cover original histogram/dotplot/stem-and-leaf interactions, nine width settings, 19 bin-count settings, neutral quiz states, links, dataset totals, printing, and desktop/tablet/phone widths. Foundations checks cover four selection sizes, census handling, question feedback, keyboard operation, MathML and six worked solutions. Topic 1.3 checks verify sample counts, 40-step tallying, denominator changes, four claim cases, seven worked answers, printing and responsive layouts.

## Preservation, attribution and privacy

Keep source, data, tests and provenance with each topic so the material can be revised for another course year. The repository's version history preserves earlier editions; consult the current official College Board course description before adding a topic.

Do not publish student records, credentials, private notes, secure AP Classroom questions, or font files. Use original formative practice and label hypothetical data. Public official exam documents are linked rather than uploaded; third-party owners retain their rights. AP is a College Board trademark, and this independent site is not endorsed by the College Board.

There are no analytics, accounts, submissions, ads or persistent learner tracking. Choices remain in the current page and reset on reload. Hosting-provider security logs are separate. See the book's Sources and resources chapter for attribution.
