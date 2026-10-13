# AP Statistics · Maple Hill School

**Seeing Quantitative Data** — an interactive Quarto book for Topics **1.5 and 1.6**, prepared for Chun Li's class.

## Student site

The intended GitHub Pages address is **https://lichunubc.github.io/ap_statistics/**. This is a deployment target, not a claim that Pages is already enabled. Check the latest **Build and publish Quarto book** workflow's deployment result before sending the address to students.

### One-time publishing setup

The repository was private when this pilot was prepared; its visibility has not been changed.

1. For the GitHub Free route, make this lecture-only repository **public** in **Settings → General → Change repository visibility**. Review its contents first. GitHub also supports Pages for private repositories on eligible plans; there is no need to change visibility when that option is already available.
2. Open **Settings → Pages**. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Open **Actions → Build and publish Quarto book → Run workflow**. The build renders and tests the book; deployment publishes the student site when Pages is enabled.
4. Open the resulting Pages URL in a signed-out/private browser window before distributing it.

Do not add student records, secure assessments, private notes, or credentials to a public repository. The pilot contains selected classroom material, not the user's other files. It does not change account settings or purchase a plan.

References: [GitHub Pages eligibility](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [Quarto publishing documentation](https://quarto.org/docs/publishing/github-pages.html).

## What students get

Eight browsable pages: start page; individual-value plots; histogram construction; adjustable histogram lab; distribution descriptions; worked examples; eight practice questions with solutions; sources/resources.

Activities include one-observation-at-a-time dotplots and stem-and-leaf plots, **whole-bar histogram animation linked to the frequency table**, frequency/percentage switching, bin-width/bin-count controls, keyboard-selectable bars with raw-data inspection, A–E shape questions using published datasets, neutral-state evidence questions, and a bar-height construction check. No running notebook kernel, account, or student-data service is needed.

## Edit and extend

Edit the `.qmd` chapters rather than generated files in `docs/`. Navigation is defined in `_quarto.yml`. Shared graph code is in `assets/site.js`; CSS in `assets/site.css`; recorded classroom data in `assets/data.js`. Add future chapters to `_quarto.yml`.

With [Quarto](https://quarto.org/docs/get-started/) installed:

```sh
quarto preview
# or generate the complete static website
quarto render
```

The GitHub Actions workflow installs **Quarto 1.9.38**, renders, runs browser checks, commits generated `docs/`, and deploys to Pages when configured. No personal access token is required; the workflow uses GitHub's repository token with explicit permissions. A source edit triggers the next build. Generated HTML commits do not create a build loop.

### Portable preview without Quarto

With Python and Pandoc installed:

```sh
python tools/preview.py
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. This preview uses the same chapter text and activities, with a lightweight navigation shell. The Quarto build adds full-text search and its native book navigation. The downloadable pilot archive includes a prebuilt portable preview; open `docs/index.html` after extracting it. Relative links and activities remain local.

## Quality checks

```sh
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tools/check_site.py
```

Set `CHROMIUM_PATH` to use an existing Chromium binary. Set `INLINE_BROWSER=1` in environments that allow in-memory page rendering but prohibit browser navigation; local assets are then inlined for the same interaction tests.

Checks cover eight pages, internal links, preserved observation totals, six whole-bar construction steps, play/reset, both individual-value displays, nine width settings, all 19 bin-count settings, known published-dataset totals, quiz neutral/reset states, printing/restoration, practice feedback, and page widths of 1440, 768, and 390 pixels. Test results go in `qa/` and are excluded from source control.

## Scope, attribution, and privacy

The content follows the revised 45-slide Topic 1.5–1.6 lecture and accompanying study guide. Official exam documents are linked, not uploaded. Exam-based charts are classroom redraws from the lecture's numerical transcriptions. Published R datasets are attributed in the book; other data are hypothetical. Third-party owners retain their rights. AP is a College Board trademark; this site is not endorsed by or affiliated with the College Board.

There are no analytics, ads, accounts, submissions, or persistent learner tracking. Responses remain in the current page and reset on reload. Hosting-provider security logs are separate. Printing expands solutions and shows reference constructions without permanently changing the on-screen activity.

The post-render script removes bundled font files; the site uses system fonts. It also leaves a `.nojekyll` marker in the output.
