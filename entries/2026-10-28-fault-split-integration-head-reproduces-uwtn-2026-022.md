---
title: "The fault-split integration head reproduces UWTN 2026-022's numbers; the suites pass but for two failures that predate it"
date: 2026-10-28
authors: [wombat session_01HxWvn5rMK67zasgirdXszQ (Fault Models Code Unification), docs hub]
options:
  kind: measurement
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/tree/feature/fault-split-integration
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
    - https://github.com/Underworld-Technical-Notes/underworldcode.org/tree/note/faults-on-an-add-on-mesh/articles/faults-on-an-add-on-mesh/figures/src
---

The candidate head `feature/fault-split-integration` (d81a2588: development 7222caf3 with
the split-multigrid root, the parallel add-on lineage, the box-faults deltas, the
warm-start switch, kaiju's diagnostics and the leak fix) was built on the laptop in its
own worktree (amr-dev, PETSc 3.25, macOS) and run against the suites and against the
note's own fixture.

## What was tried

Tier A level 1 serial; `tests/parallel` at 2 and 4 ranks; the fault and multigrid tests
by name; the note's `library_c.py` fixture at k = 2, 3, 4 and the moving fault, serial
and at 4 ranks; the note's "Using it" recipe as written, with the box's fault points,
unit viscosity and simple shear on every wall filled in.

## What happened

| | result |
|---|---|
| tier A serial | 1515 passed, 44 skipped, 0 failed |
| parallel np 2 | 156 passed, 16 skipped, 2 failed |
| parallel np 4 | 187 passed, 2 failed, no hangs |
| by name (1086, 1089, 1095 to 1099, 0077, 1018, 1058) | all pass |

The two failures are the same at both rank counts and neither is the head's:
`test_0078` reads `/proc/self/statm`, which does not exist on macOS (made portable on
the leak branch, with the RSS assertion kept Linux-only, because on macOS the resident
set rises 14 to 26 MB per rebuild while PETSc's object table is unchanged after 4 and 8
rebuilds); `test_1063_constrained_freeslip_parallel[ti]` gives topography 37.7525
against a recorded 37.0780 at rtol 0.01, and fails identically on development 7222caf3
with only the leak fix applied.

Against the note's figures: split C takes 5, 5, 4 velocity iterations at k = 2, 3, 4
where welded A takes 8, 13, 18; the viscous fault at k = 3 takes 5 against 12; cells
1470, 2006, 3034; peak slip equal to ten digits at every k (one difference of 1e-10).
The moving fault at k = 4: 4, 4, 5 iterations, slip 0.153319, 0.159264, 0.153278. At
4 ranks C takes 6, 5, 5 and the moving fault 5, 5, 6 (the note's 8-rank column says
7, 7, 7), with slip within 2.4e-6 relative of serial at a solve tolerance of 1e-6.

The recipe as written: 7 velocity and 15 pressure iterations, peak slip 0.15916181,
1622 cells, 4 levels (1 split) in serial; 5 and 17, slip 0.15916189, 5 levels (2
split) at 4 ranks. The level count differs with the rank count because
`base.adapt`'s intermediate levels depend on the partition when the metric's far size
(0.1) sits above the base's finest cell (0.05): child levels of 242, 968, 1144, 1436
cells in serial against 242, 968, 1040, 1230, 1436 at 4 ranks, the finest identical.
Development 7222caf3 does exactly the same, so it predates the head; the note's own
fixture (`h_far` 0.05) is partition-independent.

## What we now think

The method the note describes operates on the integration head and gives the note's
numbers. The head is not yet mergeable: development moved 38 commits (#846, #850 to
#853) and the root, the parallel lineage and the box-faults deltas now conflict with
it in `systems/solvers.py`, `systems/ddt.py` and `constitutive_models.py`; the leak fix,
the warm-start switch and the diagnostics still merge clean. Two things for the note:
the recipe's level count varies with the rank count for the reason above, so either a
sentence says so or the recipe uses the fixture's metric; and the 8-rank moving-fault
counts in the figure README (7, 7, 7) were not re-measured here.

## Verdict

Kept: feeds the integration plan (PRs B and C each take a development merge before they
open) and the note's "Using it" section. `test_1063` and the partition-dependent
intermediate levels are issues on development, filed from the hub.
