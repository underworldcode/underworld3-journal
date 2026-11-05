---
title: "The multigrid coarse solve has one rule on every route: redundant LU with a nonzero factor shift, the null space fixed on the fine level, and no SVD path (Louis, 2026-11-05)"
date: 2026-11-05
authors: ["Louis Moresi", "integration session session_01HxWvn5rMK67zasgirdXszQ on wombat, which measured #901 and relayed the ruling", "docs hub session_01HxWvn87HYCEJodpgCdaBro"]
options:
  kind: decision
  status: live
  topics: [solvers-and-multigrid, fault-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/901
    - https://github.com/underworldcode/underworld3/tree/bugfix/rotated-fmg-coarse-solve
    - https://petsc.org/release/manual/ksp/
    - entries/2026-10-28-coarse-solve-null-space-first-petsc-defaults-not-mumps.md
---

Louis asked the integration session on wombat, on 2026-11-05, to pass the coarse-solve
guidance to the docs hub, "with the goal of making everything simpler, fewer special
cases, no slow-SVD unless a genuine singular pivot is discovered during a solve." Asked
next how a genuinely singular coarse level should be handled, he chose "Keep the shift,
no SVD" over "LU, then SVD on failure" and "Shift, then SVD on failure". Both answers
are in that session's transcript as quoted here.

## What was decided

- Every route, native, custom-P and rotated, factors its multigrid coarse level the
  same way: the shared bundle's redundant LU with a nonzero factor shift. The shift acts
  only on a zero pivot, so a nonsingular level factors as it would without it and a
  singular one factors instead of failing.
- A null space is fixed on the fine operator, by the null space attached there; the
  rotated route admits a rotation only if it is null to round-off against the
  constraint and the operator. The coarse solve sits inside the preconditioner: a
  direction it handles badly costs iterations and cannot change the answer.
- There is no SVD path and no retry logic. The rotated route's special case goes. SVD
  appears in the guidance only as a solver a user may set by hand.
- This replaces Louis's refinement of 2026-10-31 on #901, "SVD is fine if the coarse
  level is coarse enough", and completes the 2026-10-28 decision (handle the null space,
  leave the coarse level to PETSc's defaults), which had no closure lines.

## What it rests on

The measurements of #901 (the integration session; numbers as on the A-prime branch,
77de8d81, and its tests `test_1111` and `test_1113`):

- Every coarse operator measured was near-singular, never singular: lambda_min/lambda_max
  2.0e-5 to 2.4e-8 on the annulus with 40 to 600 bottom cells, and 2.8e-4 on the
  spherical shell. Plain redundant LU gave the SVD's answer and iteration counts on the
  annulus, the shell, `test_1021`, the thin sheet and a faulted annulus at np 1 and 4.
- #306's zero pivot does not reproduce on the current hierarchy. An exact zero pivot
  appeared only on a forced-singular level, the fine mesh used as its own coarse level.
- The SVD is dense and was run on every rank: 64 s at np 1 and 102 s at np 4 to factor
  a 614-cell shell bottom level, against 7 s for the whole Stokes solve with LU at np 4.
- PETSc's manual, "Solving Singular Systems", recommends exactly this for a zero pivot,
  `-pc_factor_shift_type NONZERO` with `-pc_factor_shift_amount` about 1e-10, and does
  not mention SVD.

## What it does not say

- PETSc's manual also says its null-space handling "is only guaranteed to work for left
  preconditioning" and "may not work in some situations with `KSPFGMRES`", which is the
  outer solver here. The answers measured agree, so it works on these problems; it is
  not a guarantee. For the dev hub.
- A GAMG-preconditioned velocity block, used where a mesh has no refinement hierarchy,
  has GAMG's own coarse solve, which the shared bundle does not set. Examples on curved
  or periodic domains that ran with an SVD there are not yet verified without it.
- Why the coarse operators are only near-singular is a hypothesis, not measured: the
  custom transfer reproduces linear fields only for fine nodes inside the coarse hull,
  and a wall node snapped to the true circle or sphere is outside it.

## Closure

- **Preferred**: the shared bundle's redundant LU with a nonzero factor shift on every
  route's coarse level, and the null space attached on the fine operator.
- **Allowed**: `coarse_solve="gamg"` on a custom-P hierarchy when the bottom level is too
  large to gather (Louis, 2026-10-31, on #901), asked for, never automatic; any PETSc
  coarse solver a user sets by hand, an SVD included; taking the shift off to see
  whether a level is genuinely singular.
- **Where enforced**:
  - the library: the A-prime branch (`bugfix/rotated-fmg-coarse-solve`, 77de8d81; no PR
    yet) removes the `"svd"` variant and sets the shift on the rotated route's live
    coarse PC. Not yet done: the shift in the shared bundle's redundant variant, so the
    standard route carries it too (dev hub; `test_1021` reads the bundle);
  - the docs: the advanced multigrid guide and the solvers, rotated free-slip and
    split-level subsystem docs, rewritten to the one rule with the SVD history moved to
    the changelog (`docs/coarse-solve-one-rule`, 42e55655, stacked on A-prime; local,
    awaiting a push); the fault-multigrid guide on #862 (c2ea1565, pushed);
  - the examples: the 16 box and Dirichlet examples and tutorials lose their `svd` line
    (`docs/examples-no-svd-coarse`, b88c9fd9; local, awaiting a push); the 28 curved or
    periodic ones follow after a run on the shifted bundle;
  - the solvers topic page's standing rules (docs hub; done with this entry).

## Verdict

Kept. Feeds the multigrid guides and subsystem docs, the examples, the dev hub's A-prime
PR and the solvers topic page.
