---
title: "Fault multigrid: the ladder measured (split, welded and no mid; TI); orphan injection retired"
date: "2026-10-13"
authors:
  - "Louis Moresi"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/30545203ce1bc4f483e3ece01bb3f1250887acfd"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`30545203`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/30545203ce1bc4f483e3ece01bb3f1250887acfd) by Louis Moresi, 2026-10-13: **Fault multigrid: the ladder measured (split, welded and no mid; TI); orphan injection retired**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

**Measured on the ladder (2026-10-13, the `test_1022` rig: base $h = 1/8$ with one refinement, a transfinite ribbon of width 0.06 at spacing 0.04, 0.02, 0.01, 0.005, the spine cut at the ribbon's own vertices and split; the mids are the same ribbon at 2:1 and 4:1, welded or split on the same spine vertices).** Velocity iterations per solve:
| finest spacing | no mid | welded mid(s) | split mid(s) |
|---|---|---|---|
| 0.01 (one mid, 0.02) | 6 | 7 | 7 |
| 0.005 (two mids, 0.02 and 0.01) | 9 | 9 | 9 |
The slip is identical in every arm (0.2182 and 0.2177). The contact count does not depend on the mids at all here: the finest's FAC patch already carries the discontinuity, and the ribbon is only 6 to 12 times finer than the base's finest level, so the no-mid tail is a short, healthy chain. The split mids cost a fatter level (45 nnz per row against 33 welded, the cell-located transfer against the nested one). The TI realisation on the same ladders: 3 and 6 iterations with no mid at the two depths, 2 and 3 with the nested welded mids, so for TI the mids are worth having at depth. Both welded two-mid arms returned NaN on the first run: the welded-to-finest transfer left four orphan coarse unknowns and the nearest-node injection "repaired" them into duplicate columns (a singular coarse operator), the same mechanism as the parallel failure of the welded tail. Dropping orphans is now the rule on every hierarchy and both arms converge.
- **Nearest-node injection for orphan columns.** Not correct in serial either: on the ladder's two-mid chain four orphans injected onto fine rows that already carried a weight-1 entry gave duplicate columns, a singular coarse operator and NaN, split and unsplit finest alike; in parallel 512 of 618 orphans duplicated. Dropping the unknowns is the rule on every hierarchy now; the repair is gone.
