---
title: "Box fault: post-fix step cost; first run in progress"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/a1bbe5e4a402444e17120451ab1e77f410f48751"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`a1bbe5e4`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/a1bbe5e4a402444e17120451ab1e77f410f48751) by Louis Moresi, 2026-10-17: **Box fault: post-fix step cost; first run in progress**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

- **Parallel multigrid defect, found and fixed here.** The velocity multigrid on the split mesh needed 4 iterations in serial but 22, 37 and 55 on 2, 4 and 8 ranks, while a plain or free-slip box held at 3 to 4 on any rank count. The split moves the fault's cell star onto one rank, so the finest partition is no longer the coarse one, and the custom-P transfer into the finest level went wrong in two ways: the cross-partition builder ran a serial orphan repair on each rank's slice of the all-gathered coarse cloud and overwrote thousands of fine rows with injections onto far-away coarse nodes (20,272 of 27,785 rows wrong on 8 ranks), and the co-partitioned builder snapped nodes outside the rank's local coarse hull to the nearest local node, with the automatic choice between the two made on empty columns alone, which preferred the broken one. The parallel builders no longer repair orphans (genuine ones are dropped at install) and a level is rebuilt across partitions whenever a fine node falls outside its local hull. The finest transfer now reproduces the coordinate field to 1e-14 on 2 and 8 ranks; `tests/parallel/test_1095` holds the check. After the fix the velocity solve takes 5, 5 and 6 iterations on 2, 4 and 8 ranks against 4 in serial, and the wall time scales (70, 39, 29 s for the probe's single solve). On the box itself (29k cells, Coulomb, 8 ranks) a Newton iteration now costs about 90 s with 11 to 12 velocity and 20 to 25 pressure iterations; what remains is the per-iteration assembly and the rotated and Galerkin matrix products on P2 tetrahedra, and the Coulomb step takes two to five Newton iterations.
*First run in progress (2026-10-17 night): elastic limit (De = 100), Coulomb μ = 0.4 with overburden 0.01, S = N = 0.01, φ = 80°, 8.5k cells on 16 ranks, four cycles of 16 steps.*
