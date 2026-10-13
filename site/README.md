# Whole-book navigation

This folder supports **all five units**. Unit-specific teaching content stays in the corresponding `Unit N/` folder.

- `assets/navigation.css`: responsive unit cards and accessible sidebar disclosure styling.
- `assets/navigation.js`: turns Quarto's section toggle into a labelled native button; all topic lists start collapsed on every page load. Unit-title links open the landing pages; the separate arrow shows/hides topics. No browser storage or student data is used.
- `assets/navigation.html`: loads the script through Quarto's global footer include.
- `tests/check_navigation.py`: unit pages/cards, status labels, mouse and keyboard disclosure, desktop/mobile layouts, no-JavaScript links, and actual navigation.

The welcome page is `index.qmd`. Each `Unit N/unit-N.qmd` is its unit's editable landing page. Unit 1 holds the original six topic cards and dataset introduction; Units 2–5 are explicitly under construction. `project/unit-status.json` records unit names and available topics, separately from the detailed topic manifest.

`collapse-level: 1` is also set in `_quarto.yml`. The small enhancement prevents Quarto from automatically exposing the active chapter's ancestors. Without JavaScript, the unit links and their topic cards remain usable. Do not publish topic placeholders as if their lessons existed.

Run `quarto render` and `python tools/check_all.py`. Development branches named `preview/**` run the same build/tests without publishing; only main can save generated output or deploy. Existing public lesson URLs and source checksums remain protected by the original tests.
