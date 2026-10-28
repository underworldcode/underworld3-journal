---
title: "Shear-band length scales: Cosserat through refinement 5; corrected comparison"
date: "2026-10-09"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/59f9b01c1ba3d8bcd68f984dd6eabc7c21bc3fef"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`59f9b01c`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/59f9b01c1ba3d8bcd68f984dd6eabc7c21bc3fef) by lmoresi, 2026-10-09: **Shear-band length scales: Cosserat through refinement 5; corrected comparison**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

*Band width and peak strain rate against $h_{\min}$: micromorphic (β = 0.1) solid, for every $\ell$; Cosserat (c = 1) dashed.*
| Cosserat $\ell$ = 1 km | 36/36 | 34/36 | 34/35 | 32/39 | 47/49 |
| Cosserat $\ell$ = 0.5 km | 35/37 | 36/37 | 35/36 | 32/38 | 27/38 |
Where the band is resolved on the coarse multigrid levels, the cost per Newton step does not change with refinement. That holds for micromorphic $\ell \ge$ 1 km and for Cosserat. The one exception is a single point: Cosserat at $\ell$ = 1 km rises to 47 at refinement 5, on 16 ranks. It grows as the band approaches the coarse-level element size (micromorphic $\ell$ = 0.5 and 0.25 km). Without a length scale, the band shrinks with $h$ and the linear solve fails at refinement 3: 36, then 226, then 500 iterations, ending in `DIVERGED_LINEAR_SOLVE`.
With $c = 1$ and P1 $\omega$ the Cosserat model converges at every refinement at $\xi = 0$:
- 4–5 exact Newton steps at refinements 1–3;
- 3–4 grid-sequenced steps at refinements 4 and 5.
Its width does not change with refinement either:
| $\ell$ (km) | ref 1 | ref 2 | ref 3 | ref 4 | ref 5 | peak, ref 5 |
|---|---|---|---|---|---|---|
| 0.5 | | 5.33 | 5.33 | 5.34 | 5.34 | 0.92 |
| 1 | 6.61 | 6.63 | 6.65 | 6.68 | 6.69 | 0.46 |
At the same $\ell$ the Cosserat bands are about 45% wider than the micromorphic ones (6.69 against 4.64 km at $\ell$ = 1 km) and 2–2.7 times weaker in peak strain rate: diffuse shear zones rather than sharp bands. The width is insensitive to $c$ (0.5 or 1), to the degree of $\omega$, and to $\xi$. $c \to 0$ recovers the plain problem.
![Cosserat strain-rate maps, refinements 3-5](../figures/notch-length-scale-refinement-maps-cosserat.png)
*Cosserat, c = 1, ξ = 0: $\log_{10}\dot\varepsilon_{II}$ at refinements 3, 4 and 5 (columns), $\ell$ = 1 and 0.5 km (rows).*
*Refinement 3, ξ = 0, colour range clipped to the bands. Top: micromorphic, β = 0.1, $\ell$ = 1 and 0.5 km. Bottom: Cosserat, c = 1, $\ell$ = 1 and 0.5 km.*
