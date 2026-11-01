---
title: "The FAC patch is on one rank by construction: the default placement, seams='gather', runs partition_addon first and gives the band's region to one rank at any rank count; the serial patch solve measured at np 16 comes from the placement, not from the welded tail"
date: 2026-11-01
authors: ["Louis Moresi, on underworld3 #892", "kaiju session (science hub)", "relayed by the wombat notes session_011S876ckjYqqth1aPyojrhh", "recorded by the docs hub"]
options:
  kind: finding
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892#issuecomment-6557052460
    - https://github.com/underworldcode/underworld3/issues/895
    - entries/2026-11-01-np-16-annulus-corrected-the-arms-had-different-patches-the-velocity-work-is-equal-and-the-serial-patch-costs-5-to-6-percent.md
---

The np 16 record said the patch was on one rank "because the fault lies inside one
partition". That is not the reason, and the corrected np 16 entry carried the same
reading. The campaign drivers place the fault with
`place_fault_ribbon_2d(..., seams="gather")`, the default. At np > 1 on `development`
that call first runs `addon_partition.partition_addon`, which moves the add-on once,
before any surgery: it gives the band's region to one rank and moves cells far from
the fault to balance the load to within 10 %. The band is then placed and split on
that rank. So the band, the split pairs and the FAC patch are on one rank by
construction, at any rank count.

## What was measured

Kaiju: 105 split pairs at fault depth 0.15 and 231 pairs with a 7010-row patch at
0.45, each time all on one rank of 16. The patch's LU solve, 21 to 28 s a step at
np 16 while the other 15 ranks wait, is therefore a cost of the gather placement and
not of the welded tail.

## The alternative, unmeasured

`seams="conform"` (#670) meshes the band through the partition boundaries with
nothing moved, and would divide the patch into one block per rank. In
`place_fault_ribbon_2d` it needs `mesher="network"`; the ladder takes only
`"gather"`. It has never run in the annulus, and the dev hub's k-partitions test on
kaiju is its first run. Whether the iteration count holds when the patch is divided
among ranks is not measured (#895 for 3-D).

## What it changes

- The fault-multigrid guide's parallel section: the two imbalance terms are now
  stated by route. An adapt-and-cut child inherits the base's partition; the
  placement route repartitions the add-on and puts the band on one rank by choice.
  The 8-rank cap measured on the toy is set by whichever rank holds the band, either
  way.
- The ruling is untouched: the serial patch is a property of the placement, the
  welded tail only exposes it because the chain carries no patch.

## Verdict

Kept. Feeds the fault-multigrid guide (PR #862) and the topic page. The k-partitions
test's result is the follow-up entry.
