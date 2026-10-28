---
title: "Fault multigrid: the finest ladder is the constraint; how far the welded base carries it, and what each realisation needs under it"
date: "2026-10-14"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/d94e705a270966e4b96591a7f03f2c6f8daaadc7"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`d94e705a`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/d94e705a270966e4b96591a7f03f2c6f8daaadc7) by Louis Moresi, 2026-10-14: **Fault multigrid: the finest ladder is the constraint; how far the welded base carries it, and what each realisation needs under it**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

**The finest ladder is the constraint; the tail is the choice (2026-10-14).** The ladder exists so that stress, and everything read from it (topography, the stress inside against outside the influence zone), is resolved on elements that lie wholly inside or wholly outside the band: the margins are element boundaries. That is a property of the finest level only; the coarse levels are a preconditioner and never see a stress. So the finest is fixed as the base's finest with the ladder placed into it, the fault entering it by the realisation (spine split for an interface law, TI band for a damage zone, both on the same band), and everything below it is free. The base is never cut: the finest is a separate mesh built from it. The question is then how far the welded base carries a single finest ladder, and what to put under it when it does not:
![iterations against band depth](../figures/fault-mg-ladder_depth.png)
*Velocity iterations as the ladder deepens, on the base with finest cell 1/16 (red) and on a twice-refined base, finest cell 1/32 (blue), with no mid level; the markers at 0.0025 are the tails tried under the 1/16 base. Left, split-node contact; right, the TI band.*
| finest spacing (ratio to base 1/16) | contact, no mid | contact, 1 / 2 / 3 welded mids | contact, 1 / 2 / 3 / 4 split mids | TI, no mid | TI, 1 / 2 / 3 welded mids |
|---|---|---|---|---|---|
| 0.01 (6) | 6 | 7 | 7 | 3 | 2 |
| 0.005 (12) | 9 | 9 | 9 | 6 | 3 |
| 0.0025 (25) | 25 | 21 / 21 / 21 | 21 / 21 / 13 / 13 | 8 | 6 / 5 / 4 |
On the twice-refined base, no mid: contact 8 and 14 at 0.005 and 0.0025 (ratio 6 and 12), TI 5 and 7.
- **A single ladder over the welded base is enough up to a ratio of about 12** for both realisations (contact 9, TI 6). Past that the contact count climbs steeply (25 at ratio 25); the TI count hardly moves (8).
- **For the TI realisation the nested welded mids are a clean, monotone gain** (8, 6, 5, 4 with zero to three mids at ratio 25), and optional.
- **For the split realisation the welded mids do nothing** (21 for one, two or three), which is the B2 result again: a welded coarse space under a split fine operator. One or two split mids near the finest do nothing either (21). The *chain* of split ladders from near the base's spacing (0.02, 0.01, 0.005 under 0.0025; adding 0.04 changes nothing) brings it to 13, which is C on the ladder and is what the split-level machinery is for. A twice-refined base with no mid gives the same count (14): the split chain does the job of base refinement under the band. The chain's levels are fat (57 to 66 nonzeros per row on the mid levels against 27) and cost 40 s against 26 s for the finer base at this size.
- **The count still rises with the band's absolute resolution** on either route (9 at 0.005 to 13 or 14 at 0.0025), unlike C on the cut, which fell with depth. The two have different tails (the cut's levels are 2:1 bisections of the base down to the fault; the ladder's chain starts with a 3:1 welded-to-split jump).
So, under the constraint: keep the band within a ratio of about 12 of the base's finest cell near the fault and the add-on is one level, both realisations, no mids. A base graded toward the fault corridor at construction (`refine_lines`) is the balanced way to get that ratio, since the base is partitioned once for what it holds. Where the base cannot be graded, the TI realisation takes welded nested mids and the split realisation takes the split chain, which needs the ribbon replay.
