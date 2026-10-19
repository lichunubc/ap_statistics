# Sampling-laboratory data

`population.json` is an intentionally designed 36-member model population. Six advisory groups have six positions each. Each cluster contains two grades A, two B, two C; stratum totals are 12 per grade. Travel minutes are generated using `8+6*(position mod 3)+2*(advisory mod 3)+2*I(position>=3)` with zero-indexed positions and groups. Population total = 612 minutes, mean = 17 minutes, and grade means are 11, 17, 23 minutes. Periodic list order intentionally makes every-sixth systematic samples grade-homogeneous. Do not use as observed data. No accounts or tracking.
