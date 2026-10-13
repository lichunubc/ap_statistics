# Authoring and preserving the course

## Start with current source

Read `_quarto.yml`, `project/topic-status.json`, the relevant `Unit 1/Topic 1.x/README.md`, and adjacent chapters. Refresh main immediately before writing; reconcile concurrent work and use ordinary non-force commits. A source implementation, a successful test run, and a live deployment are separate states.

## Exact topic names, independent navigation and editorial folders

Use the **exact official CED topic title** in both the main heading and metadata. Each topic is a direct sibling under its unit, not a grouped topic range. All Unit 1 teaching files belong under the literal **Unit 1** folder, with one **Topic 1.x** subfolder per topic. A topic's `objectives.json` gives the edition, objective IDs and printed pages.

Topic-specific QMD, JavaScript/CSS, data/provenance and tests live with their topic. Truly shared files live in **Unit 1/Shared** and are linked from topic READMEs; do not create divergent copies of shared data. The existing 1.5/1.6 lessons are preserved as included `_*.qmd` sections in the appropriate topic folder. `_quarto.yml` includes only each topic's main chapter, not its partial sections.

Repository-wide infrastructure (homepage, resource chapter, build/validation tools, publishing workflow and project-level status) remains at the root. `docs/` is generated publication output. Never edit a generated compatibility page as the source of a lesson. Keep `Unit 1/legacy-pages.json` and `legacy-assets.json` accurate so old links continue to work.

## Learning design and data

A topic needs explicit CED-aligned learning targets, contextual explanations, labelled worked examples, purposeful accessible interactions, common errors, original practice and full revealable answers. Use Maple Hill School / Chun Li branding. Keep notation meaningful and explain the group a statistic describes.

Preserve the exact hypothetical School A counts (Walk 8, Bicycle 6, Bus 18, Car 8; n=40) and its original provenance. Its 960-minute total does not provide 40 recoverable individual times. The 24 quantitative commute values and 24 study-location responses are separate datasets. Clearly distinguish illustrative rows, synthetic summaries, real published observations and future original materials.

## Privacy, rights and accessibility

Never publish real student records, private notes, secure AP Classroom assessments, credentials or font files. Link official public documents instead of uploading whole copyrighted PDFs. Retain third-party attribution and do not infer redistribution rights from public availability. Do not introduce learner accounts, analytics, submissions or persistent tracking without separate authorization.

Controls need labels and keyboard access. Quiz controls start unselected; next/clear/restart reset choices and explanations. Include non-colour feedback, useful static content without JavaScript, and print reference states that restore the original screen state afterwards. Use system fonts. Code mathematics in LaTeX QMD; Quarto renders MathML.

## Release gate

Run `quarto render`, then `python tools/check_all.py` after installing `requirements-test.txt` and Chromium. Independently check arithmetic and source-data totals. Retain and extend prior regressions. Inspect desktop and mobile screenshots; test links, neutral quiz states, keyboard input, printing and no-JavaScript content. CI must exercise native HTTP navigation, mobile menus and full-text search; offline inlining alone does not establish those checks.

Update the course manifest, topic objective mapping, README/roadmap and changelog. Commit source, not only HTML. Use the existing publishing workflow and inspect its **Publish site** and **Verify published chapter** steps. The live check matches `docs/release.json` to the actual source revision and verifies both new and old page URLs. Report only completed validation and actual publication outcomes.
