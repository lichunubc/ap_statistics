# Unit 1: Exploring One-Variable Data and Collecting Data

Each topic is an independent chapter and a separate editorial folder. Use the exact official topic name, not a combined range such as “1.1–1.4”. The current book includes Topics 1.1–1.6; later Unit 1 topics have not been authored here.

The student-facing unit entrance is **[unit-1.qmd](unit-1.qmd)**. Edit this file to maintain the six topic cards and the unit's dataset introduction. The root `index.qmd` contains only the five-unit overview, not this topic list. The unit title in the sidebar opens this entrance; its separate arrow shows/hides the topics.

- [Topic 1.1 Introducing Statistics: What Can We Learn from Data?](<Topic 1.1/README.md>)
- [Topic 1.2 Variables](<Topic 1.2/README.md>)
- [Topic 1.3 Tabular Representation and Summary Statistics for One Categorical Variable](<Topic 1.3/README.md>)
- [Topic 1.4 Graphical Representations for One Categorical Variable](<Topic 1.4/README.md>)
- [Topic 1.5 Graphical Representations for One Quantitative Variable](<Topic 1.5/README.md>)
- [Topic 1.6 Descriptions for One Quantitative Variable Distributions](<Topic 1.6/README.md>)

## Finding files for manual editing

A topic folder contains its main `topic-1-x.qmd`, `objectives.json`, local documentation, and topic-specific `assets/`, `data/`, and `tests/` where needed. Topics 1.5 and 1.6 retain their original lesson text in editable `_*.qmd` sections included by the topic's main chapter. Graphical assets shared by those two topics live in `Shared/assets/` rather than being duplicated.

`Shared/data/` holds the original hypothetical summaries and quantitative CSV, with explicit provenance; `Shared/practice.qmd` holds the existing cross-topic quantitative practice; `Shared/tests/` holds integration/regression tests. Each topic README points to shared dependencies. `legacy-pages.json` and `legacy-assets.json` preserve old public addresses without duplicated editable sources.

Repository-wide infrastructure remains at the root: `_quarto.yml`, `index.qmd`, `resources.qmd`, `tools/`, `project/`, `site/`, `.github/`, and global documentation. These support the whole book, not just one topic. Generated `docs/` mirrors the published structure and contains compatibility pages at old URLs; never edit it manually.

Run `quarto preview` for editing. Run `quarto render` followed by `python tools/check_all.py` for release checks. `tools/prepare.py` regenerates browser data from the shared JSON; `tools/postrender.py` creates compatibility pages/resources and removes bundled fonts.
