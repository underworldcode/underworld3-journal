---
title: "Shear-band length scales: stiffer beta, strength shift, inexact Newton, 3-D extruded notch"
date: "2026-10-12"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/849dd042bbfe8c5ee5e3a5b327d040e342c00a0e"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`849dd042`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/849dd042bbfe8c5ee5e3a5b327d040e342c00a0e) by lmoresi, 2026-10-12: **Shear-band length scales: stiffer beta, strength shift, inexact Newton, 3-D extruded notch**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

### Inexact Newton: loose linear solves are enough
Once the band has a length scale, the linear solves need not be tight. Micromorphic, β = 0.1, $\ell$ = 1 km, starting from the viscous solution, on 4 ranks:
| linear solves | ref 2: Newton / total Krylov | ref 3: Newton / total Krylov | $W$ at ref 3 (km) |
|---|---|---|---|
| every solve to $10^{-8}$ | 6 / 231 | 6 / 227 | 4.617305 |
| fixed rtol $10^{-4}$ | 6 / 97 | 6 / 91 | 4.617304 |
| Eisenstat–Walker capped at $10^{-3}$ | 6 / 69 | 7 / 68 | 4.617305 |
| Eisenstat–Walker capped at $10^{-2}$ | 7 / 54 | 7 / 43 | 4.617272 |
- Capping the Eisenstat–Walker forcing at $10^{-2}$ cuts the Krylov work 4–5 times for at most one extra Newton step, and the width agrees to $10^{-5}$.
- The uncapped default (forcing up to 0.1–0.3) took 15, 57 and more than 40 Newton steps at refinements 1–3: its early directions were loose enough that the line search fell to λ = 0.01–0.1.
Multigrid and inexact Newton work here for the same reason. The regularised solution is not sensitive to small changes in the iterate, so a loose linear solve and a coarse-grid correction both point the right way. Without the length scale the band follows the mesh, and small changes move it.
- **$\beta$ sets how much the band is strengthened.** In the band the shift $H(e-\chi)$ peaks at about $3.7\beta C$, nearly independent of $\ell$: 0.37 C at β = 0.1, 0.75 C at 0.2 and 1.1 C at 0.3. The flanks are weakened by 0.1–0.2 C. The largest shift is at the notch tip: 3.4 C at β = 0.1.
- **A stiffer micromorphic coupling does not close the gap.** These pairs put micromorphic close to its $\beta$ threshold and Cosserat ten times above its $c$ threshold, so we repeated two of them at larger $\beta$, with $\ell$ retuned to the same width:
| $W$ (km) | micromorphic | Newton steps, refs 1 / 2 / 3 | Krylov per step, refs 1 / 2 / 3 | Newton, ref 4 |
|---|---|---|---|---|
| 3.63 | β 0.1, $\ell$ 0.5 | 6 / 8 / 9 | 39 / 49 / 54 | 5 |
| 3.63 | β 0.3, $\ell$ 0.272 | 7 / 8 / 10 | 38 / 45 / 43 | 4 |
| 3.63 | β 1, $\ell$ 0.148 | 14 / 22 / 27 | 35 / 40 / 41 | 3 |
| 2.66 | β 0.3, $\ell$ 0.138 | 8 / 17 / 17 | 42 / 72 / 155 | 5 |
  A larger $\beta$ costs Newton steps and strengthens the band more (see "What the parameters do"). At 2.66 km the multigrid cost still grows with refinement. Cosserat with $c$ = 1 stays cheaper for narrow bands.
## Example: the extruded notch in 3-D
The 2-D notch extruded along strike $z$ and meshed with tetrahedra (P2 velocity, P1 $\chi$). The faces $z = 0$ and $z = L_z$ carry $u_z = 0$, so they are symmetry planes. Micromorphic, $\ell$ = 1 km, $\xi = 0$, 1.2 km elements across the band (about 2-D refinement 1.8, where $W \approx$ 4.6–5.0 km), $L_z$ = 6 km, 8 ranks.
| | β = 0.1 | β = 0.3 |
|---|---|---|
| Newton steps | 6 | 5 |
| Krylov per step | 29–46 | 25–37 |
| $W$ at mid-strike (km) | 4.59 | 5.68 |
| $W$ along strike (km) | 4.54–4.60 | 5.60–5.76 |
| peak | 1.18 | 0.65 |
The 3-D model reproduces 2-D: the same Newton count, flat multigrid, and a width within about 1.5% of 2-D at the same element size (peak 1.20–1.22 in 2-D). Two things were needed:
- the shared-graph JIT, which generates 54 KB of C for this problem against 22 MB before it;
- a coarse multigrid base, because the direct solve on the coarsest level dominated the cost on a fine base.
