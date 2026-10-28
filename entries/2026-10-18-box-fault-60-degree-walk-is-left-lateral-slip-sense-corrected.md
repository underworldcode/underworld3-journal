---
title: "Box fault: 60 degree walk is left-lateral (slip sense corrected)"
date: "2026-10-18"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/cd862afb7d71ac36c24de9bb6ead99b48a27a349"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`cd862afb`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/cd862afb7d71ac36c24de9bb6ead99b48a27a349) by Louis Moresi, 2026-10-18: **Box fault: 60 degree walk is left-lateral (slip sense corrected)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

| strike 60° (clamping in quadrature) | −4.6 × 10⁻⁵ (−5.2 × 10⁻⁵ steady) | 0.007 | 2.6 × 10⁻⁵ |
In quadrature the slip still reverses twice a cycle at similar peak rates; the clamping shifts when the fault slides, not how far. Slip is reported right-lateral positive throughout; every oblique fault walks left-lateral. (The splitter labels the fault's sides by a coordinate-order rule that swaps as the fault rotates, between 30° and 45° on this geometry, so the raw jump changes sense with the angle; the driver now orients it from the geometry.) This is the box form of the shell's site sweep: in-phase clamping gives a size asymmetry that relaxation accumulates into a walk, quadrature gives a timing asymmetry and almost none.
