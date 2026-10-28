---
title: "Fault multigrid: the two embeddings (cut and ladder), the larger-case scaling and where the imbalance comes from"
date: "2026-10-13"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/1f9b8271e428c638aa4ac9b44a13094f33a657a9"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`1f9b8271`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/1f9b8271e428c638aa4ac9b44a13094f33a657a9) by Louis Moresi, 2026-10-13: **Fault multigrid: the two embeddings (cut and ladder), the larger-case scaling and where the imbalance comes from**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

## Two embeddings: the cut and the ladder band
A fault reaches the mesh by one of two routes, and C was built on the first.
![the two embeddings](../figures/fault-mg-embedding_routes.png)
*Left: the cut. Middle: the placed ladder band, as the fault-network work builds it. Right: where the two meet, not yet built.*
- **The cut** (`FaultNetwork.build(width=None)`, `mesh.add_fault` with `cut=True`): adapt grades the mesh toward the trace, the trace's control points are pulled onto vertices, every edge the trace crosses is split at the crossing, and the chain is split. The fault's resolution is whatever adapt gave the band. This is the route the whole page above describes, and the level replay is literally the same cut on each add-on level.
- **The ladder band** (`FaultNetwork.build(width=w)`, `place_fault_ribbon_2d`, `mesher="ladder"` or `"network"`): a structured band of width $w$ (rails plus the exact spine, transfinite) is placed into the mesh by carve-and-fill, the fault is the band's spine, and the split consumes the spine's own vertices (`cut=False`, nothing snaps). The band is a modelling object (a damage zone, a yielding or TI layer, a permeable zone) or, for a split-node model, pure resolution. Its multigrid is the fault-patch design (#629): the welded base levels as the tail, and the finest level's smoother gains an ASM patch of LU blocks keyed on the band's cell label. Measured there: 10 velocity iterations against 44 with no patch and 60 with a replacing patch, on the fine S-fault rig at a TI contrast of $10^{-3}$.
**Where they meet.** The ladder design foresaw band-resolved intermediate levels (a 2:1 sub-sampled ladder shares every spine vertex with the finer one, which is why `mesher="ladder"` exists), and then measured that an intermediate level is not worth building: "the no-mid economics", tail $[L_0, L_1]$ plus finest. Those mid levels were welded or band-rheology levels, and that is the same result as B2 here: a coarse level without the discontinuity does not help the split fine operator. What was not measured is a mid level that carries the *split* spine, which is C. On the ladder route C would be: place the sub-sampled band on each add-on level and split its spine, so the slits nest exactly (the clamp becomes unnecessary) and the band cells are structured on every level; the FAC patch can stay on the finest. The replay, the pairing-as-labels, the co-location and the per-level frames carry over unchanged; the placement replay is the missing piece (a `("ribbon", traces, width, size)` recipe beside `("line", ...)` and `("sheet", ...)`). Today a `cut=False` fault keeps its welded tail and patch, and C does not touch it.
**Iterations and times.** C converges at every rank count tried: $k = 3$ takes 5, 6, 6, 8 iterations at 1, 2, 4, 8 ranks and $k = 4$ 4, 5, 5, 7. The count creeps up with ranks for two reasons: `adapt` keeps one intermediate level fewer at 8 ranks than in serial (its level subsampling is partition-dependent, a known difference; 4 levels against 5), and the smoother is block-Jacobi across ranks. On the 2000- to 3000-cell box the times say nothing about scaling (the solve is 4 to 9 s and dominated by set-up). A larger case says something:
![larger case](../figures/fault-mg-parallel_behaviour_large.png)
*The same box with a base cell of 0.025 and three add-on levels (26230 cells on the finest) at 1, 4, 8 and 16 ranks: imbalance per level, transfer misses, and stage times.*
| ranks | velocity its | finest max/mean cells | adapt | cut + split all levels | transfers | solve |
|---|---|---|---|---|---|---|
| 1 | 11 | 1.0 | 16.0 s | 21.7 s | 6.8 s | 314 s |
| 4 | 9 | 1.7 | 4.8 s | 7.7 s | 2.4 s | 92 s |
| 8 | 8 | 3.1 | 3.9 s | 5.9 s | 1.8 s | 64 s |
| 16 | 8 | 5.2 | 3.3 s | 5.5 s | 1.5 s | 67 s |
The iteration count holds, the set-up stages scale with the ranks that do not own the fault, and the solve stops scaling at 8 ranks: the rank that owns the fault carries three times the mean cells there and five times at 16, and every smoother sweep and residual waits for it. Most of that is adapt's own imbalance, not the star: at 16 ranks the unsplit child already puts 6822 of 26230 cells on one rank (4.2 times the mean), and the gathered star adds 1624 to it (8458, 5.2 times). The transfer misses are 1 to 4 % throughout. This is the compromise in numbers: refining in place without rebalancing, and then gathering the star onto the rank that already holds the band, caps the speed-up at roughly (mesh / band) ranks. In a plate-scale model the band is a small fraction and the cap is correspondingly higher, but it is a cap. The way past it is rebalancing after adapt (item 1) with a partition that weights the star's cells so the fault's rank gets correspondingly less of the rest.
- Rebalancing after `adapt` (the inheritance above, and the larger part of the measured imbalance), with the star's cells weighted; it would also change where the stars land.
- C on the ladder band: replay the sub-sampled ribbon placement and spine split on each add-on level (nested slits), with the FAC patch kept on the finest; the no-mid economics were measured with welded mid levels only.
