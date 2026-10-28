---
title: "Shear band length scales: 3-D coarse-level solve and capped Krylov tolerance"
date: "2026-10-12"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/9b3113498e11fea9fb6eef838610a756cdb067bf"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`9b311349`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/9b3113498e11fea9fb6eef838610a756cdb067bf) by lmoresi, 2026-10-12: **Shear band length scales: 3-D coarse-level solve and capped Krylov tolerance**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

On a 1,387-tet base (refinement 2, 8 ranks), PETSc's native LU on the coarsest level costs 13% more than MUMPS: 1830 s against 1625 s, with the same 6 Newton steps and 51 Krylov iterations. A genuinely coarse base makes the native solve cheap enough, so MUMPS is not needed. The Krylov tolerance capped at $10^{-2}$ works in 3-D as in 2-D: 51 Krylov iterations against 229 with every solve to $10^{-8}$, 4.2× less time with the same coarse solver, and $W$ the same to five digits.
