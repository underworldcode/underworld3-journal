---
title: "The campaign drivers default to uw_chain 0 (b440b88), accepted on kaiju at np 16 on development 25d62812: the last 'where enforced' line of the 2026-11-01 tail decision is done, and the drivers' decisions ledger is citable"
date: 2026-11-02
authors: ["science hub session_013CgVT1Gx9WTvaZVqU58HsQ (kaiju)", "relayed by the wombat notes session_011S876ckjYqqth1aPyojrhh", "recorded by the docs hub"]
options:
  kind: measurement
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/commit/b440b88
    - https://github.com/lmoresi/uw3-campaigns/blob/bf18312/zg95_lid_regimes/DECISIONS.md
    - entries/2026-11-01-the-production-tail-for-split-faults-is-the-welded-base-with-the-fac-lu-patch-on-the-split-finest-level.md
    - entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md
---

The 2026-11-01 tail decision left one line of "where enforced" to the science hub: the
drivers' `uw_chain` default, to change once kaiju confirmed the welded tail on
`development` at np 16. It is done. Commit b440b88 on `lmoresi/uw3-campaigns`
(`zg95-annulus-for-kaiju`) sets `uw_chain=0` in `annulus_faults.py`, `annulus_fault.py`
and `box_fault.py`, with the campaign's build moved to `development` 25d62812 in the same
step, so no run takes the welded tail on a build without #912's LU blocks (on the
leak-fix overlay, chain 0 was about 1.5 times slower).

## Acceptance

Kaiju job 3154, TAf checkpoint 40, np 16, one step on `development` 25d62812, the driver
with `uw_chain 0` and pressure rtol 1e-2: vrms 1358.9188, peak slip 5877.77, mobility
1.2870, Newton 6, walls clean to 1e-12, equal to the chain-0 reference on the same build
to the printed figures. The ledger also records, from the np 16 pairs at TAf 20 and TBf
70 over 10 steps: the same answer, a wash on speed at the production band ratio 3.9, chain
0 20 to 35 % faster at fault depth 0.45, and chain 0 free of the coarse-level ladder
refusals and the silent weld that once put a band along the surface and ran a node out
of memory.

## The ledger

Per Louis's ruling that the drivers' decisions must be findable outside underworld3, the
campaign keeps `zg95_lid_regimes/DECISIONS.md` (bf18312 at the time of writing): one row
per driver option with its value, who ruled it and when, and the evidence. It is the
citation for the pressure rtol (1e-2, ruled 2026-11-01), the chain (0, from 2026-11-02),
the split inset (3 rungs, under review: Louis asks for one element if possible), the
seams and mesher (gather and ladder; conform unusable, the next entry), the wall normal
(analytic today, geometric recommended; a library defect with the dev hub) and the
crust-base locator (envelope).

## What it closes, and what it does not

Every line of the 2026-11-01 decision's "where enforced" now has a commit. Of the
2026-11-02 decision's driver line, `uw_chain 0` is done; the trace placed at its own
division with no `uw_spacing` is not. The campaign's results from here are on a
different library and pressure tolerance than the thermal and Earth sets, a documented
discontinuity in the ledger.

## Verdict

Kept. Closes the drivers' line of the 2026-11-01 decision. Feeds the fault-multigrid and
faults-in-convection guides (the default is now stated as done) and the topic page.
