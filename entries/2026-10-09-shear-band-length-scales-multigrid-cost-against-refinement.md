---
title: "Shear-band length scales: multigrid cost against refinement"
date: "2026-10-09"
authors:
  - "lmoresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/41e22d2fe336424bbb772819c21a954586a0c587"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`41e22d2f`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/41e22d2fe336424bbb772819c21a954586a0c587) by lmoresi, 2026-10-09: **Shear-band length scales: multigrid cost against refinement**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

### Multigrid cost: flat where the length is resolved
Krylov iterations per Newton step (median / max), with every linear solve tight to $10^{-8}$:
- $h$ is the element crossing the band at x = −15 km: 2.1, 1.1, 0.53, 0.27 and 0.13 km at refinements 1–5;
- refinements 1–3 start cold from the viscous seed;
- refinements 4–5 are grid-sequenced, so their steps are fewer and easier.
| model | ref 1 | ref 2 | ref 3 | ref 4 | ref 5 |
|---|---|---|---|---|---|
| micromorphic $\ell$ = 2 km | 34/36 | 36/37 | 34/38 | 27/37 | |
| micromorphic $\ell$ = 1 km | 36/37 | 36/44 | 36/43 | 27/39 | 32/38 |
| micromorphic $\ell$ = 0.5 km | 39/43 | 49/64 | 54/88 | 33/51 | 37/47 |
| micromorphic $\ell$ = 0.25 km | 43/52 | 63/188 | stagnates | inexact Newton only | |
| Cosserat $\ell$ = 1 km | 36/36 | 34/36 | 34/35 | | |
| Cosserat $\ell$ = 0.5 km | 35/37 | 36/37 | 35/36 | | |
| no length scale, $\xi$ = 0.03 | 35/38 | 47/50 | linear solve fails | | |
Where the band is resolved on the coarse multigrid levels, the cost per Newton step does not change with refinement. That holds for micromorphic $\ell \ge$ 1 km and for Cosserat. It grows as the band approaches the coarse-level element size (micromorphic $\ell$ = 0.5 and 0.25 km). Without a length scale, the band shrinks with $h$ and the linear solve fails at refinement 3: 36, then 226, then 500 iterations, ending in `DIVERGED_LINEAR_SOLVE`.
