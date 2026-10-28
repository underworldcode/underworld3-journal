---
title: "Box fault: walk scaling with the Wallace number and the clamping-phase result"
date: "2026-10-18"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/198cf04a712710a16b5a2322987635978121e245"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`198cf04a`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/198cf04a712710a16b5a2322987635978121e245) by Louis Moresi, 2026-10-18: **Box fault: walk scaling with the Wallace number and the clamping-phase result**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

*Provisional (2026-10-18): one box, one load, μ = 0.4, overburden 0.01, S = N = 0.01, φ = 80°, 20k cells on 16 ranks, 16 steps per cycle, six cycles per run. The De 0.3, De 3 and 60° runs are still in progress; this section is revised as they land.*
The surface carries the walk's far-field signature: a four-lobed pattern around the fault, as for a left-lateral offset, and a broad drift on the loaded side reaching the edge of the box, 1 to 3 × 10⁻⁴ per cycle, steady from the second cycle on.
**The walk scales with the Wallace number, more weakly than 1/De.** The steady net slip per cycle (from the third cycle on) for the 30° fault:
| De | Wa = 1/De | net slip per cycle | surface net displacement per cycle |
|---|---|---|---|
| 0.3 | 3.3 | −2.8 × 10⁻³ (cycle 2, still settling) | 7.8 × 10⁻⁴ |
| 1 | 1 | −1.12 × 10⁻³ | 3.0 × 10⁻⁴ |
| 3 | 0.33 | −4.7 × 10⁻⁴ | 1.4 × 10⁻⁴ |
| 10 | 0.1 | −1.9 × 10⁻⁴ | 6.2 × 10⁻⁵ |
| 100 | 0.01 | −6.6 × 10⁻⁵ (still falling, about 12 % a cycle) | 3.3 × 10⁻⁵ |
Between De 1 and 10 the walk falls as about De^−0.78, and De 3 sits on that line; the elastic-limit run is decaying toward the floor the same law predicts (about 3 × 10⁻⁵). A truly elastic body cannot sustain a walk: the back-stress of each increment has nowhere to go. The walk needs the Maxwell relaxation to remove it, and the relaxation per cycle sets the rate.
**The walk needs the clamping in phase with the shear.** At 60° the clamping comes mainly from the normal load, which leads the shear by φ = 80°, so it is in quadrature with the driving:
| De 1, cycle 2 | net slip per cycle | fraction of the cycle's slip | surface net displacement |
|---|---|---|---|
| strike 30° (clamping in phase with the shear) | −1.17 × 10⁻³ | 0.25 | 3.4 × 10⁻⁴ |
| strike 60° (clamping in quadrature) | +4.6 × 10⁻⁵ | 0.007 | 2.8 × 10⁻⁵ |
In quadrature the slip still reverses twice a cycle at similar peak rates; the clamping shifts when the fault slides, not how far. This is the box form of the shell's site sweep: in-phase clamping gives a size asymmetry that relaxation accumulates into a walk, quadrature gives a timing asymmetry and almost none.
**Summary so far.** The Berne et al. mechanism needs three things at once: clamping that varies with the load, in phase with the shear; a relaxation time comparable to the period or shorter; and a fault free to slip. Given all three, the asymmetry accumulates into a steady walk and a steady far-field displacement, both scaling as roughly Wa^0.8. Gravity, absent here, would oppose the topography the walk builds and stop it at an amplitude of order the asymmetric driving stress over ρg.
