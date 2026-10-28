---
title: "Fault multigrid: the base is never rebalanced; partition the add-on child; one ladder hierarchy for split and TI"
date: "2026-10-13"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/029c3659019cf81b963ebe9c3c2c771d6ea5f1cd"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`029c3659`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/029c3659019cf81b963ebe9c3c2c771d6ea5f1cd) by Louis Moresi, 2026-10-13: **Fault multigrid: the base is never rebalanced; partition the add-on child; one ladder hierarchy for split and TI**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

1. **The add-on child is imbalanced before any fault exists.** Adapt-on-top refines in place, co-partitioned with the base, and the child keeps the base's partition: the refined band lands on whichever ranks held the region. On this box the unsplit child holds 240, 601, 243, 680 cells on 4 ranks and 132 to 625 on 8. The base is never rebalanced (it is the persistent object that holds the fields; the ruling in `fault-parallel-placement-2026-09.md`); the child is ephemeral and does not have to inherit the base's partition, since every transfer to it is partition-agnostic. Redistributing the child and its levels, with the fault star's cells weighted, is the fix, and it touches nothing in the base. The toy exaggerates the effect (the band is most of the mesh here; in a plate-scale model it is a small fraction).
The iteration count holds, the set-up stages scale with the ranks that do not own the fault, and the solve stops scaling at 8 ranks: the rank that owns the fault carries three times the mean cells there and five times at 16, and every smoother sweep and residual waits for it. Most of that is adapt's own imbalance, not the star: at 16 ranks the unsplit child already puts 6822 of 26230 cells on one rank (4.2 times the mean), and the gathered star adds 1624 to it (8458, 5.2 times). The transfer misses are 1 to 4 % throughout. This is the compromise in numbers: a child that keeps the base's partition, and then gathers the star onto the rank that already holds the band, caps the speed-up at roughly (mesh / band) ranks. In a plate-scale model the band is a small fraction and the cap is correspondingly higher, but it is a cap. The way past it is to partition the child and its add-on levels for themselves (the base untouched), with the star's cells weighted so the fault's rank gets correspondingly less of the rest.
- Partitioning the add-on child and its levels for themselves, star-weighted, the base untouched (the larger part of the measured imbalance).
- **One hierarchy for both fault representations.** The ladder band sub-sampled 2:1 is the add-on hierarchy: nested levels, each carrying the fault as the model has it, a split spine on every level (C) or a TI band at every level's own resolution (the TI realisation, where a smeared coarse level is the right coarse space because the fine operator is smeared too; B2 failed only because its fine operator was split). The background stays welded and untouched either way. Not the cut on some meshes and a placement on others: one placed, nested ladder, two realisations. The ribbon replay recipe is the missing piece; the no-mid economics were measured with welded mid levels only.
