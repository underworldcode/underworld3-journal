---
title: "Box fault: the parallel multigrid defect and its fix"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/a344376a0b8313237bedff6134c337061846aa72"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`a344376a`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/a344376a0b8313237bedff6134c337061846aa72) by Louis Moresi, 2026-10-17: **Box fault: the parallel multigrid defect and its fix**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

- **Parallel multigrid defect, found and fixed here.** The velocity multigrid on the split mesh needed 4 iterations in serial but 22, 37 and 55 on 2, 4 and 8 ranks, while a plain or free-slip box held at 3 to 4 on any rank count. The split moves the fault's cell star onto one rank, so the finest partition is no longer the coarse one, and the custom-P transfer into the finest level went wrong in two ways: the cross-partition builder ran a serial orphan repair on each rank's slice of the all-gathered coarse cloud and overwrote thousands of fine rows with injections onto far-away coarse nodes (20,272 of 27,785 rows wrong on 8 ranks), and the co-partitioned builder snapped nodes outside the rank's local coarse hull to the nearest local node, with the automatic choice between the two made on empty columns alone, which preferred the broken one. The parallel builders no longer repair orphans (genuine ones are dropped at install) and a level is rebuilt across partitions whenever a fine node falls outside its local hull. The finest transfer now reproduces the coordinate field to 1e-14 on 2 and 8 ranks; `tests/parallel/test_1095` holds the check. The iteration counts and the step cost after the fix are being measured.
- **Cost before the fix.** About 100 s per step on 8 ranks at 16k cells, almost all of it in the Schur loop at those iteration counts; the semi-Lagrangian history added about 45 s, the 100:1 damage band and the solver tolerance were not the drivers.
