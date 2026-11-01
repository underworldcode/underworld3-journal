---
title: "The np 16 annulus pair ran at a band ratio of 3.9, below the smallest ratio in UWTN 2026-022's sweep table (6.06 to 24.8), which is why the welded tail's patch bought nothing measurable there; the runs used the library's default tolerances, and a pressure rtol of 1e-2 halves the solve with the same answer"
date: 2026-11-01
authors: ["kaiju session (science hub, chain page v4)", "relayed by the wombat notes session_011S876ckjYqqth1aPyojrhh", "recorded by the docs hub"]
options:
  kind: finding
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892#issuecomment-6552218825
    - https://github.com/lmoresi/uw3-campaigns/blob/main/HUB.md
    - entries/2026-11-01-np-16-annulus-corrected-the-arms-had-different-patches-the-velocity-work-is-equal-and-the-serial-patch-costs-5-to-6-percent.md
---

The corrected np 16 entry left one thing open: why the production annulus shows none of
the gain the box fixtures show from the LU patch. Kaiju's chain page answers it with
the band ratio. On the annulus's rebuilt mesh f8 the base's finest cell is
$h_b = 0.5/2^5 = 0.0156$ and the rung spacing $S = 0.004$, so $h_b/S = 3.9$. Every
row of UWTN 2026-022's sweep table sits between 6.06 and 24.8, and the box's gain from
the patch appears only at those larger ratios. At 3.9 the welded coarse space already
carries the band well enough, and a chain with no patch matches the welded base with
one.

## The hierarchies, as applied

Cells coarsest first, both on the same rebuilt mesh:

| arm | levels |
|---|---|
| chain 0, welded | 124 / 496 / 1984 / 7936 / 31744 / 126976 (welded base) / 127705 (the $S$ child, with the patch) |
| chain 2, lean chain | 124 / 496 / 1984 / 7936 (welded base) / 31914 ($4S$ on base level 4) / 127277 ($2S$ on base level 5) / 127705 (the $S$ child, no patch) |

## What it settles

- The annulus result and the box table are consistent: the patch's gain is a function
  of the band ratio, nil at 3.9 and 4 to 11 times per Newton increment from about 8
  upward. UWTN 2026-022's conclusion, "the welded base is enough when the patch is
  solved exactly", holds on the annulus as well; what the annulus does not show is a
  gain from the patch, and the ratio explains that.
- The ruling stands as written, and the guides can give the ratio where they said the
  reason was open.

## Also recorded, from kaiju's logs

The trench runs, the restart runs and the annulus pair all used the library's default
tolerances: 1e-3 on the Stokes residual, 1e-4 on the pressure, 3.3e-5 on the velocity
(the velocity sub-solve's rtol is 0.033 of the solver tolerance). UWTN 2026-022 now
says so for each set. Louis has approved `-uw_pres_rtol 1e-2` as the campaign default;
in the annulus pair it took the Stokes solve from 441/410 s to 183/174 s with the same
answer. Whether the library's own default follows is the dev hub's question.

## Verdict

Kept; closes the open line of the corrected np 16 entry. Feeds the fault-multigrid and
faults-in-convection guides (the ratio replaces "reason open") and the topic page.
