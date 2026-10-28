---
title: "Box fault: orientation series (30, 45, 60 degrees) against the in-phase clamping"
date: "2026-10-18"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/1db4f6b9860d4f41ea95fbe08a148cb4319e9530"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`1db4f6b9`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/1db4f6b9860d4f41ea95fbe08a148cb4319e9530) by Louis Moresi, 2026-10-18: **Box fault: orientation series (30, 45, 60 degrees) against the in-phase clamping**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

*2026-10-18: one box, one load, μ = 0.4, overburden 0.01, S = N = 0.01, φ = 80°, 20k cells on 16 ranks, 16 steps per cycle, six cycles per run. Every run in the tables has finished except the 45° fault, whose steady value is already clear.*
**The walk needs the clamping in phase with the shear.** Rotating the fault changes how the end load divides between clamping and shear on it, and so the phase of the clamping relative to the shear. At De 1, steady values from the third cycle on (slip reported right-lateral positive; every oblique fault walks left-lateral):
| strike | far-field clamping phase relative to the shear | in-phase part of the clamping (cos(phase) × amplitude) | net slip per cycle | ratio to 30° | surface net displacement per cycle |
|---|---|---|---|---|---|
| 30° | −152° | 7.5 × 10⁻³ | −1.12 × 10⁻³ | 1 | 3.0 × 10⁻⁴ |
| 45° | −108° | 3.2 × 10⁻³ | −4.4 × 10⁻⁴ | 0.39 | 1.0 × 10⁻⁴ |
| 60° | −82° (near quadrature) | ≈ 1.4 × 10⁻³, changing sign | −5.2 × 10⁻⁵ | 0.05 | 2.6 × 10⁻⁵ |
The walk follows the part of the clamping in phase (here anti-phase) with the shear, the component that makes one half-cycle stronger than the other: the far-field estimate gives 0.43 at 45° against 0.39 measured. Near quadrature (60°) the slip still reverses twice a cycle at similar peak rates; the clamping shifts when the fault slides, not how far, and the walk almost vanishes. This is the box form of the shell's site sweep. (The splitter labels the fault's sides by a coordinate-order rule that swaps as the fault rotates, between 30° and 45° on this geometry, so the raw jump changes sense with the angle; the driver now orients it from the geometry.)
