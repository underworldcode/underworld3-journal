---
title: "Under continuation a datum-only cold start skips its Picard phase and still converges in 10 Newton iterations: not a must-fix"
date: 2026-10-29
authors: [wombat session_01HxWvn5rMK67zasgirdXszQ (Fault Models Code Unification), docs hub]
options:
  kind: measurement
  status: live
  topics: [solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/883
    - https://github.com/underworldcode/underworld3/issues/876
    - https://github.com/underworldcode/underworld3/tree/feature/fault-split-integration
---

Follows `2026-10-29-datum-only-cold-start-reference-on-the-rotated-path-costs-one-increment`,
which left the continuation case open.

## What was tried

C at 4698938f: a ThinSheet on a spherical manifold (cell size 0.25), viscoplastic
(unit viscosity, yield stress 0.05), a prescribed normal velocity $0.1 z^2$ as the only
forcing, tolerance $10^{-6}$, `consistent_jacobian="continuation"`.

## What happened

The switch is evaluated at iteration 0 with a zero reference, so the Picard phase is
skipped, and the solve converges in 10 iterations with exactly the default Newton
tangent's residual history ($1.13\times10^{-2}$ down to $1.46\times10^{-9}$). No
failure, no stall.

## What we now think

By the criterion set the day before (a must-fix only if a datum-only nonlinear solve
stalls or fails), the hand-resolved hunk stays as it is in C. The cost on the linear
case and the skipped Picard phase here are the same root cause, the reference taken
from the lifted iterate, and go to the follow-up #883 (reference from the lift's
right-hand side) as a small PR after C. Separately, `ThinSheet.solve(picard=N)` is a
TypeError (#876), so a sheet cannot ask for Picard steps by that route either.

## Verdict

Kept. Closes the open question of the previous entry; #883 carries the fix.
