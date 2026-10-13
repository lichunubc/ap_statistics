# Unit 1 shared data and provenance

`foundations.json` retains the original instructor-supplied hypothetical summaries and provenance: School A (n=40), comparison School B (n=60), study locations (n=24), and movie satisfaction (n=30). These are separate contexts, not real student records. The unknown School A population bus proportion is not invented. The sum 960 minutes supports the supplied sample mean, not recovery of 40 individual times.

`commute-times.csv` is the separate 24-value hypothetical quantitative dataset from the existing Topics 1.5–1.6 pilot. It is NOT the School A categorical sample or the study-location sample.

`../assets/data.js` retains the quantitative pilot's original values, source labels and public-data citations (rivers, faithful, iris, oxygen frequencies and chocolate examples). See the book's Sources and study resources chapter. `foundations-data.js` is generated from `foundations.json` by `tools/prepare.py`; edit the JSON rather than the generated JavaScript.

Topic 1.2's four illustrative individual records and their limitations are documented separately in `../../Topic 1.2/data/README.md`. Never replace hypothetical examples with identifiable student records.
