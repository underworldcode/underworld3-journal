---
title: "Shear-band length scales: micromorphic and Cosserat at equal band width"
date: "2026-10-11"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/00ec1f166da2d6ded13716ba982c15977c205f07"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`00ec1f16`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/00ec1f166da2d6ded13716ba982c15977c205f07) by lmoresi, 2026-10-11: **Shear-band length scales: micromorphic and Cosserat at equal band width**

The Cosserat width map over l and c, the matched-width pairs, their
profiles, and solver cost seeded, grid-sequenced and from rest.

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

At the same $\ell$ and $c = 1$ the Cosserat bands are about 45% wider than the micromorphic ones (6.69 against 4.64 km at $\ell$ = 1 km) and 2–2.7 times weaker in peak strain rate. The width barely changes between $c$ = 0.5 and 1, with the degree of $\omega$, or with $\xi$. $\ell$ does not mean the same thing in the two models, and at equal width the bands are nearly the same.
### Micromorphic and Cosserat at equal band width
The Cosserat width is set by $\ell$ first and by $c = \eta_c/\eta_{lin}$ second.
![Cosserat width map](../figures/notch-length-scale-cosserat-width-map.png)
*Cosserat at refinement 3, exact LU, ξ = 0: band width, peak over background and Newton steps over $\ell$ and $c$. Orange contours: the micromorphic widths at β = 0.1, $\ell$ = 0.25, 0.5 and 1 km.*
- **Cosserat has a threshold in $c$**, as micromorphic has one in $\beta$: $c$ = 0.01 never converges, $c$ = 0.03 converges only at $\ell \ge$ 0.5 km, and $c \ge$ 0.1 converges everywhere.
- **Small $c$ narrows the band**: at $\ell$ = 1 km, $W$ = 6.65, 5.88 and 4.16 km for $c$ = 1, 0.1 and 0.03.
Cosserat settings matched to the micromorphic widths at refinement 3:
| $W$ (km) | micromorphic, β = 0.1 | Cosserat ($\ell$, $c$) | Cosserat $W$ | peak, micromorphic / Cosserat |
|---|---|---|---|---|
| 2.66 | $\ell$ = 0.25 km | (0.14 km, 1) | 2.66 | 2.82 / 2.71 |
| 3.63 | $\ell$ = 0.5 km | (0.236 km, 1) | 3.63 | 1.85 / 1.75 |
| | | (0.25 km, 0.1) | 3.60 | 1.85 / 1.78 |
| 4.62 | $\ell$ = 1 km | (0.37 km, 1) | 4.67 | 1.22 / 1.18 |
| | | (0.5 km, 0.054) | 4.70 | 1.22 / 1.15 |
![Matched profiles](../figures/notch-length-scale-matched-profiles-ref3.png)
*Refinement 3, strain rate over background on the vertical cut at x = −15 km. Solid: micromorphic. Dashed: Cosserat, $c$ = 1. Dotted: Cosserat, small $c$.*
- **At equal width the bands are nearly the same.** Peaks agree within 3–6%. At $c$ = 1 the Cosserat $\ell$ is 0.4–0.55 of the micromorphic one. At 4.62 km the $c$ = 1 band sits about 1 km from the micromorphic one along this cut; the small-$c$ band lies on it.
- **The Cosserat widths are mesh-independent.** From refinement 3 to 4 they change by under 0.3%, except at 2.66 km (2%).
Solver cost on the matched pairs, with tight FMG (rtol 1e-8, no Eisenstat–Walker):
- Refinements 1–3 ran on 4 ranks, starting from the viscous solution.
- Refinement 4 ran on 8 ranks, grid-sequenced from refinement 3.
- "Cold" means starting from rest, with the one automatic Picard step written as "1 +".
| $W$ (km) | model | Newton steps, refs 1 / 2 / 3 | Krylov per step, ref 3 | Newton, ref 4 | cold, refs 1 / 2 / 3 |
|---|---|---|---|---|---|
| 2.66 | micromorphic $\ell$ 0.25 | 9 / 11 / stalled | — | stalled | 1+8 / 1+10 / stalled |
| 2.66 | Cosserat (0.14, 1) | 7 / 10 / 9 | 63 | 4 | 1+7 / 1+9 / — |
| 3.63 | micromorphic $\ell$ 0.5 | 8 / 8 / 10 | 54 | 5 | 1+7 / 1+7 / 1+9 |
| 3.63 | Cosserat (0.236, 1) | 6 / 6 / 5 | 45 | 3 | 1+6 / 1+7 / — |
| 3.63 | Cosserat (0.25, 0.1) | 6 / 7 / 8 | 46 | 4 | failed / failed / 1+12 |
| 4.62 | micromorphic $\ell$ 1 | 5 / 6 / 6 | 36 | 5 | 1+7 / 1+7 / 1+7 |
| 4.62 | Cosserat (0.37, 1) | 5 / 5 / 5 | 37 | 3 | 1+6 / 1+6 / 1+6 |
| 4.62 | Cosserat (0.5, 0.054) | 6 / 6 / 6 | 38 | 4 | failed / failed / — |
*Krylov: median per Newton step. "Stalled": a linear solve made no progress for an hour and was stopped. "Failed": 40 Newton steps without convergence. "—": not finished.*
- **Cosserat with $c$ = 1 takes as many Newton steps or fewer**, and its Krylov counts per step are similar.
- **At 2.66 km the micromorphic FMG solve stalls at refinement 3, and Cosserat converges.**
- **Small-$c$ Cosserat converges from the viscous solution but not from rest.**
- **The pairs are not equally far from their thresholds.** They put micromorphic close to its threshold ($\beta$ = 0.1 at small $\ell$) and Cosserat ten times above its own ($c$ = 1). The same comparison at larger $\beta$ has not been run yet.
