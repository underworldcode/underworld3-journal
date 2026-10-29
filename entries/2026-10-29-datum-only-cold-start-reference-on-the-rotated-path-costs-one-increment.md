---
title: "A datum-only cold start on the rotated path sets its convergence reference from the lifted iterate and takes one increment more than it needs"
date: 2026-10-29
authors: [wombat session_01HxWvn5rMK67zasgirdXszQ (Fault Models Code Unification), docs hub]
options:
  kind: finding
  status: superseded
  superseded_by: 2026-10-29-datum-only-continuation-skips-picard-and-still-converges.md
  topics: [solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/tree/feature/fault-split-integration
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

The fault-split integration head carries one hand-resolved hunk in `rotated_bc.py`:
hyperion's widened cold-start condition (`r0 is None or (lift_datum and iters == 1 and
r0 == 0.0)`, for a sheet whose only forcing is a prescribed datum and whose residual
at `u = 0` is therefore zero before the lift) kept, with the laptop's residual-history
append before it. The laptop measured what the widened condition does.

## What was tried

`test_1092`'s breathing sphere, a linear datum-only solve, on the integration head.

## What happened

`rnorm_history` is `[0, 1.87e-8, 8.7e-15]` and the reference is `1.87e-8`: the
reference is set from the lifted iterate's residual, so the solve takes two increments
where one suffices. The answer is right. Under continuation the Picard-to-Newton
switch is evaluated at iteration 0 with a reference of 0, so a datum-only solve would
skip its Picard phase; not measured.

## What we now think

The behaviour comes from hyperion's lineage, not from the merge resolution, and it is
a cost, not an error, on the linear case. The suggested fix is to take the reference
from the lift's right-hand side. The continuation case is the one that matters: if a
datum-only nonlinear solve skips Picard, that is a convergence risk for the tidal
shell, and it should be measured before the fix is designed.

## Verdict

Inconclusive on the continuation case. Filed by the laptop with the suggested fix;
the hub's advice is a separate small PR with the measurement and its test after C,
not a change folded into C's merge resolution.
