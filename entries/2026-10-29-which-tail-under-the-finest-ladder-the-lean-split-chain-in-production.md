---
title: "Which multigrid tail goes under the finest ladder: the lean split chain in production; a single ladder over the welded base only on a linear rig up to a band ratio of about 12"
date: 2026-10-29
authors: [docs hub session_01HxWvn87HYCEJodpgCdaBro, for Louis Moresi and the UWTN 2026-022 draft]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/docs/developer/guides/faults-in-convection.md
    - https://github.com/lmoresi/uw3-campaigns/blob/main/zg95_lid_regimes/drivers/box_fault.py
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/scripts/sessions/fault_mg/ladder_depth.py
---

Two statements sat side by side and read as a contradiction. The ladder-depth
measurement of 2026-10-14 says a single finest ladder over the welded base is enough
up to a band ratio of about 12 (velocity iterations 6, 9, 25 at ratios 6, 12, 25,
frictionless contact, linear). The production drivers run at a ratio of about 8 and
still build two split chain levels under the finest (`uw_chain = 2`).

## What settles it

The two were measured on different problems. The ratio-12 result is a linear,
frictionless contact solve on the test rig. The production case is a time-dependent
viscoplastic convection model with a mobilising lid, and there the welded tail fails
for a different reason than depth: once Newton starts on the yielding lid, the velocity
sub-solve under the welded hierarchy caps at its 200 iterations. The
faults-in-convection guide measured it on the box-fault model: welded A, 39 Newton
increments, 1849 velocity iterations in total, 71 to 200 per increment, two caps; the
lean split chain, 42 increments, 695 iterations, 29 to 38 per increment, no caps; the
band patch smoother did not rescue the welded tail (114 to 150 per increment). A chain
placed entirely on the finest level converges the same but costs about twice the work
per cycle, so the lean chain, each ladder on the base level one step coarser, is the
cheapest form.

**Definitions the note uses.** Band ratio: the base's finest cell size over the finest
ladder's rung spacing, $h_b / S$; on the rig $h_b = 1/16$, so $S$ = 0.01, 0.005, 0.0025
give 6, 12, 25; in the production annulus and box runs $h_b \approx 0.031$ and
$S = 0.004$, about 8. Velocity iterations: the iteration count of the velocity block's
Krylov solve, the fieldsplit sub-KSP (`fieldsplit_vel`), FGMRES with relative tolerance
0.033 times the solver tolerance (the ladder-depth runs set `tolerance = 1e-5`, so
3.3e-7) and a cap of 200, preconditioned by PCMG of type FULL built from the custom
prolongations, redundant coarse solve, the robust smoother. One iteration is one
F-cycle. The outer saddle-point KSP is FGMRES at the solver tolerance; the pressure
sub-KSP FGMRES with a cap of 200.

## The ruling

- **Preferred**: in production, the lean split chain, `uw_chain = 2`: the same ladder
  at $2S$ and $4S$ placed into the base levels one and two steps below the finest, each
  split along its own rungs, the base's remaining levels welded beneath. Whatever the
  band ratio.
- **Allowed**: a single finest ladder over the welded base, for a linear or
  frictionless solve on a rig at a band ratio of 12 or less, where it costs 6 to 9
  iterations and nothing more; and the TI realisation, which gains from welded mid
  levels and needs no split chain.
- **Where enforced**: the drivers' default (`uw_chain = 2` in `box_fault.py`,
  `annulus_fault.py`, `annulus_faults.py`); the faults-in-convection guide's hierarchy
  section with its table; the fault-multigrid guide's "what production runs do today"
  paragraph (to gain the reason: not depth, the yielding lid); UWTN 2026-022's text,
  which states both measurements and which applies when. The ribbon replay in the
  library, when it lands, makes the chain the one-call default rather than driver code.

## Verdict

Kept. The note carries one statement: the welded tail is adequate for a linear rig at
a modest ratio, and production uses the split chain because a yielding lid caps the
welded velocity solve, measured.
