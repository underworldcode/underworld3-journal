---
title: "The tail ruling is provisional above a band ratio of about 8: a sweep of three hierarchies on the production ladder is commissioned before any result is published"
date: 2026-10-30
authors: [Louis Moresi, wombat notes session_011S876ckjYqqth1aPyojrhh, docs hub]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

Louis, 2026-10-30, on the UWTN 2026-022 multigrid numbers: "I am very unsure at this
point that we recorded the best cases. This should be resolved before we publish any
results."

## What is in question

The ruling of 2026-10-29 (the lean split chain in production, at any band ratio) rests
on one measurement at a ratio of about 8 (the box-fault hard state in the
faults-in-convection guide). The lean chain keeps the welded-to-split step inside the
band at the full band ratio (a welded level at $4h_b$ under a $4S$ band), and that step
has not been measured at a higher ratio. The rig's 13-iteration chain at ratio 25 was
the graded kind, every level in a copy of the finest, and its cells were $S \times 0.03$
rather than square (entry 2026-10-30 on the rig's confound). So the ruling is
unverified above a ratio of about 8.

## The sweep, commissioned on Louis's word

Three hierarchies, all on the production ladder (band $2kS$, square cells):

- H0: the welded base, no chain.
- H1: production's lean chain ($2S$ in $h_b$, $4S$ in $2h_b$).
- H2: a graded chain, every level in a copy of the base's finest, down to within a
  factor of 4 of $h_b$ (the rig's chain at production cell shape).

Band ratios 6, 12 and 25. Problem A: the note's linear fixture (unit box, $h_b = 1/32$,
np 1 and 4). Problem B: the yielding-lid box at `uw_spacing` 0.004, 0.002 and 0.00125 on
the guide's hard state. Run by the laptop integration session; results to
`~/+Simulations/uwtn_2026_022_tail_sweep/` on wombat.

## Standing until it reports

- **Preferred** (provisional): the lean chain, as measured at ratio about 8.
- **Allowed**: nothing is ruled out above ratio 8; H2 may replace H1 there.
- **Where enforced**: the fault-multigrid topic page's current-understanding bullet
  says "provisional above a ratio of about 8"; the note keeps its existing numbers
  with their scope stated and publishes no tail result until the sweep reports;
  `DOCS-HUB.md` carries the item.

## Verdict

Open until the sweep reports. The entry that closes it names the hierarchy per ratio
and per problem, and the drivers' default follows it.
