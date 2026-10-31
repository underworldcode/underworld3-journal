---
title: "The production multigrid tail for a split fault is the welded base with the split S level on top and the FAC LU patch on that finest level; the chain of split ladders is the measured alternative, not the production tail (Louis, 2026-11-01)"
date: 2026-11-01
authors: [Louis Moresi, docs hub session_01HxWvn87HYCEJodpgCdaBro, measurements by the wombat integration session_01HxWvn5rMK67zasgirdXszQ]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892#issuecomment-6550186134
    - https://github.com/underworldcode/underworld3/pull/912
    - https://github.com/underworldcode/underworld3/pull/915
    - https://github.com/underworldcode/underworld3/pull/862
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

Louis ruled on 2026-11-01, on underworld3 #892, that the production multigrid tail for
a split fault is the welded base with the split $S$ level on top and the FAC patch on
that finest level solved by LU. The chain of split ladders, this journal's preferred
route from 2026-10-29 to 2026-10-31, is the measured alternative and not the production
tail. The ruling rests on the tail sweep re-run on #912's build, which restored the LU
blocks on the rotated path.

## What was decided

With the LU blocks running (#912, merged as cc839425), the welded base plus the split
finest level, with the FAC LU patch, is the tail. Louis's table, from UWTN 2026-022's
fixtures as measured in the tail sweep and reproduced on #912's build:

| | band ratio | welded base + LU patch | lean chain |
|---|---|---|---|
| linear fault, np 1, velocity iterations over all applications | 6, 12, 24 | 66, 65, 67 | 83, 118, 166 |
| box with a fault, np 4, velocity iterations per Newton increment | 8, 16, 25 | 7, 7, 7 | 28–40, 45–53, 67–76 |

The chain's levels never carried the patch (a pair touching a split coarse level skips
FAC detection, `custom_mg.py:1556` at 4698938f), so its numbers do not change with the
fix. The Newton path and the peak slip are the same under both tails.

## What it rests on, and what it does not say

- The sweep (entry 2026-10-31) found the two defects: the chains never had the patch,
  and the rotated path ran the patch's blocks as unshifted ILU(0) instead of the
  configured LU with a nonzero shift (#892). The history of that defect is its own
  entry of today.
- Every comparison of the chain against the welded tail made since 2026-09-03 was made
  on ILU blocks: the faults-in-convection guide's table, the 2026-10-29 ruling, the
  drivers' `uw_chain=2`, the kaiju trench demonstrations in UWTN 2026-022. All of them
  compared a chain without the patch against a welded tail with a degraded one.
- It is a 2-D statement. The LU block grows with the band's rows (about 32k summed at
  ratio 25 on the box); the cost in 3-D and at scale is not measured.
- Whether split coarse levels stay available as an option is not decided (the dev hub's
  item: `custom_mg.py:1556`, chain as option or exception).
- The drivers' `uw_chain` default changes once kaiju's np 16 annulus run confirms the
  tail on `development`; #914's parallel fix to the cover gate has not been checked at
  np 16.

## Closure

- **Preferred**: the welded base with the split $S$ level on top and the FAC LU patch
  on that finest level. The call is the convenient one:
  `set_custom_fmg(stokes, base.multigrid_levels, field_id=0)` on the placed mesh, where
  `Mesh.multigrid_levels` (#915, 25d62812) returns the base's levels coarsest first with
  the base last, and the patch is installed from the split's coincident pairs without
  being asked for.
- **Allowed**: the chain of split ladders ($2S$ and $4S$ placed into copies of base
  levels, each split along its rungs), as the measured alternative: where the LU patch
  is unavailable or its block too large (3-D, until the cost is measured), and as the
  object of the open question whether split coarse levels remain an option. It stays
  driver code (`uw_chain`) and is named as the alternative wherever it is described.
- **Where enforced**: the library, where #912 puts the configured LU on the live block
  KSPs from every call site, `test_1090_mg_live_configuration_parallel` reads back every
  level's live smoother, and the docstring at the block configuration says "FAC blocks
  are LU; ILU there is a regression"; the fault-multigrid guide (PR #862, the "what
  production runs" paragraph and the configuration rules) and the faults-in-convection
  guide (same PR, its hierarchy section, table and code), both rewritten today; UWTN
  2026-022, whose multigrid section names the smoother, whose chain paragraph becomes
  the welded tail, whose recipe moves to `Mesh.multigrid_levels` and whose panel (c) is
  redrawn as the welded hierarchy (notes session, in progress, re-pinned to
  `development`); the drivers' `uw_chain` default (science hub, after the np 16 run);
  the topic page's current understanding.

Supersedes the decision entries of 2026-10-29 (the lean chain in production) and
2026-10-30 (provisional above a ratio of about 8), both marked superseded today.

## Verdict

Kept. Feeds the fault-multigrid and faults-in-convection guides, UWTN 2026-022 and the
topic page. The entry that reports the np 16 annulus run and the drivers' new default
closes the last line of "where enforced".
