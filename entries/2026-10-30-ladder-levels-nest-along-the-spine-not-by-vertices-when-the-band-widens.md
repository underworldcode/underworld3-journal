---
title: "Ladder levels nest along the spine, not by vertices, when the band widens with the level as production does"
date: 2026-10-30
authors: [wombat notes session_011S876ckjYqqth1aPyojrhh, docs hub]
options:
  kind: finding
  status: live
  topics: [fault-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/b99c323/zg95_lid_regimes/drivers/annulus_faults.py
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/scripts/sessions/fault_mg/ladder_c.py
---

A correction to the wording in `2026-10-28-which-fault-mesh-construction-is-used-in-practice`
and `2026-10-29-which-tail-under-the-finest-ladder-the-lean-split-chain-in-production`,
which say the chain's ladders "nest by vertices (2:1 rung subsets)". Found by the
notes session while reviewing the ladder construction figure for UWTN 2026-022.

## What was tried

Compared the rig measurement (`ladder_c.py`: the ribbon placed at spacings 0.04, 0.02,
0.01 with the width held at 0.06 throughout) with the production drivers
(`annulus_faults.py`, `box_fault.py`: `uw_band_widen = 1`, so the ladder at `kS` is
`2kS` wide), and with the figure, which follows production.

## What happened

With the width held constant, the coarser ladder's rails and rungs are vertices of the
finer one and the levels nest by vertices. With the width widening with the level, only
the spine points and the inner part of every second rung are shared; the coarser
ladder's rails at $\pm 2S$ sit inside the finer level's unstructured fill and are not
vertices of the finer level, and the fills differ from level to level. In either case
every transfer touching a split level is the cell-located, side-aware one, never
injection, so the solver is the same; only the description of the nesting changes.

## What we now think

The statement for the note and the guides is "the levels nest along the spine". Vertex
nesting is the special case of a constant band width, which is what the rig measured
and not what production builds. The earlier entries' wording is the rig's case stated
as if general.

## Verdict

Kept. Feeds UWTN 2026-022's caption and construction text, and the fault-multigrid
guide's production paragraph ("so the rung sets nest" becomes "so the spine points
nest").
