---
title: "A per-level wall rotation cuts a rotated free-slip custom-FMG solve on an adapted annulus from 18 serial and 197 parallel velocity iterations to 3 and 4"
date: 2026-10-29
authors: [wombat session_01HxWvn5rMK67zasgirdXszQ (Fault Models Code Unification), docs hub]
options:
  kind: measurement
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/tree/feature/fault-split-multigrid
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

Found while reviewing `feature/fault-split-multigrid` (B of the fault-split integration)
after its merge with development, on the laptop, 2026-10-29.

## What was tried

A rotated free-slip Stokes solve on an adapted annulus with custom full multigrid, no
fault, on development and on B, serial and at 4 ranks; same problem, same answer
checked.

## What happened

| | development | B |
|---|---|---|
| velocity iterations, serial | 18 | 3 |
| velocity iterations, np 4 | 197 | 4 |

The difference is B's per-level wall rotation: every coarse level takes the wall's
rotated frame on its own nodes and loses its normal rows, where development's coarse
levels under a rotated finest are Cartesian. The topic page recorded the mechanism on
the faulted annulus on 2026-10-14 (a coarse wall node's normal component reached only
through fine tangential rows weighted by a vanishing sine; zero pivots in the inode
smoother); this is the same effect measured on a plain adapted annulus, with the
parallel count the striking one.

## What we now think

The per-level wall rotation is a change for every rotated free-slip custom-FMG user,
not only for faults, and it is a large improvement where it applies. It is also the
reason B's review flagged `custom_mg`'s split-transfer routing for non-fault solves as
a solver change needing benchmark evidence: this is one piece of that evidence, on one
problem. The annulus and shell cases named in the review still want their own numbers
before B opens or in its PR body.

## Verdict

Kept. Feeds the fault-multigrid and boundary-condition guides once B merges (the
rotated path's coarse levels carry the wall rotation), and B's PR body as the evidence
for a default that reaches non-fault users.
