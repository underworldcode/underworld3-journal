---
title: "The production chain puts the 2S ladder on the base's finest level, beside the S ladder, and the 4S ladder one level down; the rig's band-ratio table is confounded with cell aspect"
date: 2026-10-30
authors: [wombat notes session_011S876ckjYqqth1aPyojrhh, docs hub]
options:
  kind: finding
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/b99c323/zg95_lid_regimes/drivers/annulus_fault.py
    - https://github.com/lmoresi/uw3-campaigns/blob/main/zg95_lid_regimes/drivers/box_fault.py
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/docs/developer/guides/faults-in-convection.md
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/scripts/sessions/fault_mg/ladder_depth.py
---

Two corrections to `2026-10-28-which-fault-mesh-construction-is-used-in-practice` and
`2026-10-29-which-tail-under-the-finest-ladder-the-lean-split-chain-in-production`,
found by the notes session while starting the ladder rewrite of UWTN 2026-022 and
confirmed by the hub against the drivers and the guide's own cell counts.

## 1. The hosts, off by one

The drivers define `levels = base._coarse_level_meshes()[:-1] + [base]`, so the last
entry is the base's finest level, and place the chain with
`host = levels[len(levels) - k]` for `k = chain, ..., 1`: `k = 1` is the finest level
itself, hosting the ladder at $2S$; `k = 2` is one level down, hosting $4S$. The
faults-in-convection guide's own measurement confirms it: welded A is 642, 2568, 10272,
11604 cells; the lean chain is 642, 2924, 10950, 11612, that is L0 welded, $4S$ on L1
(+356 cells), $2S$ on L2 (+678), $S$ on L2. The $S$ and $2S$ ladders share the finest
base level as host; the chain replaces the base's top two levels, and the hierarchy
has as many levels as the welded one. The host-to-ladder ratio in production is about
8, 4, 4.

The two earlier entries, the guide's prose ("placed on the base levels one and two
steps below the finest"), the drivers' comments ("the base level k steps below the
finest") and panel (c) of the ladder construction figure all say otherwise. The code
and the counts are the authority; the words follow.

## 2. The rig's band-ratio table measures cell aspect as well

`ladder_depth.py` and `ladder_c.py` build the rig's band with
`place_thin_volume(..., width=0.06, size=S, mesher="ladder")`, which meshes three
nodes across (rails at $\pm 0.03$ and the spine), so the band cells are $S$ along by
$0.03$ across: aspect ratios 3, 6 and 12 at $S$ = 0.01, 0.005, 0.0025. Production's
band is $2S$ wide, giving square $S \times S$ cells. The rise of the iteration count
with "band ratio" on the rig (6, 9, 25) is therefore confounded with cell aspect, and
the table does not establish a ratio-12 limit for the production ladder.

## What we now think

The ruling of 2026-10-29 stands in its preferred clause (the lean split chain in
production, because a yielding lid caps the welded velocity solve, measured on the
box-fault model with the production construction) and loses its numerical "allowed"
clause: the welded tail's adequacy "up to a ratio of about 12" is a rig number with
the rig's geometry, not a production limit. A clean sweep on the production ladder
(width $2S$, $S = h_b/6, /12, /25$, chain 0 and 2) would settle it; that is new compute
and Louis's call.

## Verdict

Kept. Panel (c) of the figure is redrawn as $S$ on $h_b$, $2S$ on $h_b$, $4S$ on
$2h_b$; the fault-multigrid guide's production paragraph and the faults-in-convection
guide's prose are corrected (the first on PR #862 now, the second on B or C); the two
earlier entries stay live with this one beside them. One API point for the integration
plan: the recipe needs the base's levels and today gets them from the private
`Mesh._coarse_level_meshes()`; a published note cannot name a private method, so a
public accessor is needed.
