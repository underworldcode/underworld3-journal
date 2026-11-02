---
title: "seams='conform' cannot place a fault that reaches the domain wall in 2-D (the network mesher's cavity reaches the wall), and the ladder takes only gather: dividing the FAC patch across ranks is blocked for every surface-reaching fault until one of the two changes"
date: 2026-11-02
authors: ["science hub session_013CgVT1Gx9WTvaZVqU58HsQ (serial repro on kaiju, 2026-11-01)", "relayed by the wombat notes session_011S876ckjYqqth1aPyojrhh", "recorded by the docs hub"]
options:
  kind: dead-end
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/29cd738/HUB.md
    - https://github.com/lmoresi/uw3-campaigns/blob/bf18312/zg95_lid_regimes/DECISIONS.md
    - https://github.com/underworldcode/underworld3/pull/670
    - entries/2026-11-01-the-patch-is-on-one-rank-by-construction-the-default-gather-placement-not-the-welded-tail.md
    - entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md
---

The placement entry of 2026-11-01 named `seams="conform"` (#670) as the way to divide the
FAC patch into one block per rank, and the 2026-11-02 decision put that division on the
programme as row 2. It cannot run in the trench models as the library stands. The science
hub's serial reproduction on kaiju (`HUB.md` 29cd738, 2026-11-01) placed the annulus
fault with the network mesher, which conform requires, and it failed in under five
seconds: "the ribbon's cavity reached the domain wall". The ladder mesher, which places a
wall-reaching fault, accepts only `seams="gather"`.

## What follows

- Every surface-reaching fault in 2-D (the crust-law faults of the lid-regime campaign,
  the trench of UWTN 2026-022) is placed by the ladder, gathered onto one rank, and its
  patch solved by one serial LU block. There is no option in the drivers that spreads it.
- The dev hub's k-partitions test (a long fault crossing k partitions, the patch one block
  per rank crossed) cannot run in the annulus until either the network mesher can place a
  fault that reaches the wall or the ladder learns conform. Which of the two is the work
  is the dev hub's call.
- UWTN 2026-022 says it in one sentence: "It cannot be used in the trench models as they
  stand: the network mesher cannot place a fault that reaches the domain's wall, and the
  ladder, which can, does not mesh through the boundaries between processes."
- Louis, in the ledger, on conform: "disappointing to discover it is not used and has
  been forgotten." The September design (#670) built it; no driver ever wired it in, even
  as an option, and the ligament seams deadlocked with the network mesher on 18 October
  and were not retried.

## Verdict

Discarded as the next step for the patch's distribution until the library changes; the
issue that names the work is the dev hub's to file. Feeds the fault-multigrid guide's
parallel section and the topic page.
