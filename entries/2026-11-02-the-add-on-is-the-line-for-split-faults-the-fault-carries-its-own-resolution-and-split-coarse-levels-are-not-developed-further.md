---
title: "The add-on is the line to invest in for split faults: the fault carries its own resolution as a divided line, and split coarse levels are not developed further (Louis, 2026-11-02)"
date: 2026-11-02
authors: ["Louis Moresi", "notes session session_011S876ckjYqqth1aPyojrhh on wombat", "dev hub session_01HxWvn6vA38fdYLUxnxDk4g", "docs hub session_01HxWvn87HYCEJodpgCdaBro", "measurements by the integration session on wombat and kaiju"]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/e6832e0/DEV-HUB.md
    - https://github.com/underworldcode/underworld3/issues/918
    - https://github.com/underworldcode/underworld3/issues/921
    - https://github.com/underworldcode/underworld3/issues/892
    - https://github.com/underworldcode/underworld3/issues/895
    - https://github.com/underworldcode/underworld3/pull/862
    - entries/2026-11-01-the-production-tail-for-split-faults-is-the-welded-base-with-the-fac-lu-patch-on-the-split-finest-level.md
---

Louis decided on 2026-11-02, after the integration session's comparison of the two
hierarchies, that the add-on is the line to invest in. His words:

> OK - let's go with the working-hypothesis that the add-on is the most promising and
> the one worth investing in.
> 1) Add minimal additional nodes to implement the fault slip
>   1a) Any refinement around the fault can be separated out from (1)
>   1b) We original said the fault would carry its own resolution (it comes
>   triangulated / as a divided line) and this is how we create the ladder. No S
>   parameter defines the along-strike resolution.
> 2) We will try all the math tricks to make the SOLVE efficient in 2D and 3D
> 3) We can consider the parallel decomposition of this problem to make it efficient.

The add-on is the welded base's own levels, one split level into which the fault is
placed, and the FAC patch on that level solved by LU: the production tail of the
2026-11-01 decision.

## What was decided

- The add-on is developed. Split coarse levels (the chain, `custom_mg.py:1556`) are not
  developed further, and stay in the library as they are until Louis says otherwise.
- The fault's own division is the ladder's spine (1b). No parameter $S$ sets the
  resolution along the fault. This replaces the form "S = h_b or h_b/2" that the dev hub
  drew on 2026-11-01 from Louis's "the ladder and the base mesh have similar resolution";
  that form was never a journal entry. $S$ survives in the drivers (the trace resampled
  at `uw_spacing`, the band width $2S$) and is to go.
- What the ladder is for, in Louis's words the same day: "The idea of cutting the mesh to
  make the fault is that we probably don't need a lot of refinement - it's a
  discontinuity so we need to represent it efficiently. The ladder is to allow us to
  compute stresses and slip-rates accurately. Some refinement will be needed to compute
  near-fault stress lobes, but that is a different question. Let's try to avoid opening
  up too many new directions." Refinement around the fault (1a) is a separate question.
  Resolving the slip by refining the base under the fault's corridor was the dev hub's
  inference, not Louis's, and row 7's corridor arms were dropped.

## What it rests on

The evidence Louis saw, all 2-D, in velocity iterations (`DEV-HUB.md` at e6832e0):

| | add-on (H0), patch allowed | split levels (H1) |
|---|---|---|
| the 022 linear fixture at band ratios 24, 48, 97 | 66–67 | 166, 302, 725 |
| a pair of faults | 68 | 231–287 |
| a TI band | 66–94 | 230–342 |
| a junction | 77–90 | the $4S$ ladder cannot be placed at an $8S$ gap |
| the viscous box, np 4 | 125 | 388 |

H1's limit is structural: every coarse level must hold a coarser copy of the fault, which
in 3-D means surgery on every level. H0's failures were defaults: the cover gate
declining a large patch silently (#918), the structural rows left out of a TI band's
patch (#921), and ILU in place of LU on the rotated path (#892, fixed by #912).

On the mesh alone, on the 022 base at $h_b = 1/32$: with the fault divided at about $h_b$
(13 segments), the ladder adds 14 vertices, the split's duplicates and two more, and a
bare cut (`add_fault`) adds 16. At 26 and 53 segments the ladder adds 143 and 344 and the
cut still 14: the cut pulls base vertices onto the line, so it resolves the slip at $h_b$
whatever division the fault gives, which fails 1b. The placement already takes the
trace's own points as rungs.

## What it does not say

- It is a 2-D statement. The cost of one LU block on a layer of cells in 3-D is not
  measured (the dev hub's matrix row 1, #895).
- The add-on's weakness is the gathered patch. On the annulus at np 16 (kaiju, jobs
  2480–2488) the 3584-row LU block is on one rank, 21–28 s of a 410–441 s Stokes solve
  while 15 ranks wait, because the default placement (`seams="gather"`) puts the band on
  one rank (entry 2026-11-01 on the placement). In serial at band ratio 24, against LU's
  67: ILU(1) blocks at rtol $10^{-2}$, 71; 2000-row pieces with a slip coarse space,
  79–85; one-rung strips with the coarse space, 135. Points (2) and (3) are the
  iterative-patch experiments, then row 1, then row 2 (the patch divided across ranks,
  `seams="conform"`).
- How far below the surface the split stops ("one element, in mesh units") awaits
  Louis's confirmation and is not part of this decision.
- The trench demonstrations in UWTN 2026-022 ran with the chain (`uw_chain 2`); whether
  they are rerun on the add-on is Louis's open choice.

## Closure

- **Preferred**: the add-on: the base's own levels, welded, one split level into which
  the fault is placed at its own division, its points the ladder's rungs, and the FAC
  patch on that level by LU. The call: `place_fault_ribbon_2d(base, [(name, points)],
  width, split=True, mesher="ladder")` with the trace's own points, then
  `set_custom_fmg(stokes, base.multigrid_levels, field_id=0)`.
- **Allowed**: split coarse levels (the chain: `uw_chain` in the drivers,
  `custom_mg.py:1556` in the library), kept as they are for comparison with the
  measurements already made. No new work builds on them.
- **Where enforced**:
  - the fault-multigrid guide's rulings section and the faults-in-convection guide
    (PR #862, docs hub; done with this entry);
  - the chain's code path names itself the alternative and names the add-on
    (`custom_mg.py:1556`; library, dev hub; not yet done);
  - the drivers: `uw_chain` defaults to 0, and the trace is placed at its own division
    with no `uw_spacing` (science hub; not yet done);
  - UWTN 2026-022, whose ladder step says the fault is given as a divided line whose
    points are the spine, and which describes the chain as the alternative (notes
    session; on the workbench, not yet pushed);
  - the topic page's current understanding (docs hub; done with this entry).

Supersedes no entry. It settles the 2026-11-01 decision's open item, "whether split
coarse levels stay available as an option is not decided", and narrows that entry's
"Allowed" line, which kept the chain as the object of that question.

## Verdict

Kept. Feeds the fault-multigrid and faults-in-convection guides, UWTN 2026-022, the
drivers' defaults and the topic page.
