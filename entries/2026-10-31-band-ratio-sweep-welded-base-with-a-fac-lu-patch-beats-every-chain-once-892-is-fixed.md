---
title: "Band-ratio sweep: a welded base with the FAC patch solved by LU takes 3 velocity iterations at every ratio from 6 to 25 and beats every split chain; the chains never get the patch, and the rotated path runs the patch as ILU(0) (#892)"
date: 2026-10-31
authors: [wombat session_01HxWvn5rMK67zasgirdXszQ (Fault Models Code Unification), docs hub]
options:
  kind: measurement
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892
    - https://github.com/lmoresi/uw3-campaigns/blob/main/FAULT-SPLIT-INTEGRATION.md
---

The sweep Louis commissioned on 2026-10-30 ("I am very unsure at this point that we
recorded the best cases") is done, on the laptop, on the integration head. Tables,
per-level smoother records and hashes are in `~/+Simulations/uwtn_2026_022_tail_sweep/`
(`README.md`, `summary.md`) on wombat; nothing is pushed.

## What was tried

Hierarchies on the production ladder (band $2kS$, square cells): H0 the welded base with
the split ladder on top; H1 production's lean chain ($2S$ in a copy of the finest, $4S$
in a copy of the level below); H2 a graded chain, every level in a copy of the finest;
H3 as the session added it. Band ratios 6, 12 and 25. Problem A the note's linear
fixture at np 1 and 4; problem B the yielding-lid box at three rung spacings on the
convection guide's hard state. Each level's smoother recorded, which is what found the
two things below.

## What happened

1. **The FAC patch smoother is installed only when the hierarchy's sole split level is
   the finest.** So H0 gets the patch and no chain hierarchy does: H1, H2 and H3 run
   SOR on every level. The comparisons of chains against the welded tail made since
   August have therefore compared a chain without the patch against a welded tail with
   it, or neither with it.
2. **On the rotated path the FAC blocks run ILU(0), not the LU that `custom_mg`
   configures** (#892; the same code on development). The fault-patch record of August
   already said LU is what buys contrast constancy on the near-singular split patch.
3. **With LU restored, H0 takes 3 velocity iterations per linear solve and 7 per Newton
   increment on the yielding-lid box at every band ratio from 6 to 25**, 3 to 16 times
   fewer than every other arm, with Newton counts and slip unchanged.
4. **With today's library, the guide's production setting, H1 at a ratio of about 8,
   is the best arm**; H2 and H3 never pay.

## What we now think

The question the chain answered was the wrong one. The welded tail's failure on a
yielding lid was never a failure of the coarse spaces at depth: it was the finest
level's patch running the wrong sub-solver, and the chain compensated for it. Once
#892 is fixed, the production tail should be the welded base with the FAC patch
solved by LU, the design the fault-patch record settled in August, and the split chain
becomes the measured, more expensive alternative. This reverses the preferred clause of
the 2026-10-29 ruling and vindicates its being marked provisional on 2026-10-30; it
also means the note's multigrid section and panel (c) describe the second-best
construction.

## Verdict

Inconclusive until Louis rules and #892 is fixed. Proposed closure: Preferred, the
welded base with the FAC patch by LU; Allowed, the lean chain where the patch is
unavailable or until #892 lands; Where enforced, the fix to #892 on the rotated path,
the drivers' `uw_chain` default, the convection and fault-multigrid guides, the note's
multigrid section and figure. The entry that closes it carries the fix's commit and the
re-run numbers on the fixed library.
