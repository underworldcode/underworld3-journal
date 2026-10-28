---
title: "Coarse solve on the rotated path: handle the null space, leave the coarse level to PETSc's defaults; MUMPS is not the default"
date: 2026-10-28
authors: [Louis Moresi, docs hub session_01HxWvn87HYCEJodpgCdaBro]
options:
  kind: decision
  status: live
  topics: [solvers-and-multigrid, fault-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/blob/feature/coarse-solve-nullspace/scripts/sessions/coarse-solve/README.md
    - https://github.com/underworldcode/underworld3/blob/feature/coarse-solve-nullspace/scripts/sessions/HANDOVER-2026-10-27.md
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

The free-slip annulus leaves a rotation null mode, so the custom-prolongation multigrid's
coarsest solve on the rotated path is a dense SVD on one rank, and at 612 coarse cells it
took 231 to 364 s per solve at 8 to 32 ranks where a redundant MUMPS factorisation with
null-pivot detection took 4 to 8 s at the same cycle count (hyperion's sweep 3,
2026-10-27). The proposal that came with the measurement was MUMPS as the rotated-path
coarse default with SVD as a recorded fallback.

## The ruling

Louis, 2026-10-28: not MUMPS as the default. It is good on Linux and breaks on the Mac,
and a default should not depend on the platform. The preference is to **deal with the
null space explicitly and let PETSc's defaults handle the coarse mesh.** The cost the
sweep measured is the cost of a coarse level that is not coarse enough; the fix for that
is the hierarchy, which the project has not always built well, not a heavier coarse
solver.

## What this settles

- `feature/coarse-solve-nullspace` stays a measurement branch. Its benchmarks and the
  sweep records remain the evidence; its proposed default does not land.
- The library work is the rotation null space on the rotated operator, attached so that
  PETSc's default coarse solve is well posed on it; the coarsest level is made small
  by construction (the multigrid page's rule), and a large coarsest level is a
  configuration error to report, not a case to solve harder.
- Where MUMPS is available and wanted, it remains a choice the user makes, not one the
  library makes for them.

## Verdict

Kept. It feeds the fault-multigrid guide's coarse-level paragraph and the solvers topic
page; the fault-split integration plan drops the coarse-solve branch from its PR
sequence.
