# Topic 1.2 data dictionary and provenance

`illustrative-records.csv` reproduces the four **hypothetical illustrative records** already printed in Topic 1.1. They demonstrate rows, columns, identifiers, and values. They are **not a raw-data extract of the fixed School A sample**, and must not be appended to that sample or used to reconstruct its 40 individual commute times.

| Field | Meaning | Role / unit |
|---|---|---|
| student_label | Fictional row label A–D | Identifier, not a measured quantity |
| main_travel_method | Main travel-method category | Categorical |
| one_way_commute_minutes | Illustrative elapsed time from home to school | Continuous underlying duration, recorded in minutes |

The common 40-student School A summaries remain authoritative in `../../Shared/data/foundations.json`: N=1000; n=40; Walk=8, Bicycle=6, Bus=18, Car=8; sample commute total=960 minutes. Population bus proportion and mean commute time are not supplied. Source attribution in the shared file is retained verbatim.

The 24 commute times used in Topic 1.5, the 24 study-location responses, the 30 movie-rating responses, the four illustrative rows, and the School A sample are distinct examples. No student records are included. All other scenarios in the Topic 1.2 chapter and `../assets/variables.js` are original hypothetical practice, not observations from a real investigation.
