# Topic 1.8 teaching data and provenance

All datasets are invented for explanation, not real Maple Hill School observations. Units: one-way journey time, minutes.

- Typical: 5,8,10,12,12,14,15,16,18
- High extreme: 5,8,10,12,12,14,15,16,50
- Left-tail case: 1,32,33,34,35,36,37,38,39
- Two-cluster case: 5,6,6,7,7,7,20,20,21,21,22,22

The UI accepts 3–40 finite values in [0,60], uses the sorted median-of-halves quartile convention (exclude overall median when n is odd), and applies strict 1.5-IQR fences. All derived statistics recompute when edited. No records or answers are sent to a server. These are not the 24-time commute dataset or School A's 40 categorical responses used in earlier chapters.
