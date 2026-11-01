---
title: "The production annulus at np 16 confirms the welded tail by a small margin (5.9 against 7.7 velocity iterations per Newton increment, the same answers), because both arms carry the same finest patch; that patch, 465 rows and 105 split pairs, sits on one rank, so its LU solve is serial"
date: 2026-11-01
authors: [kaiju session (science hub), reported by Louis Moresi on underworld3 #892; recorded by the docs hub]
options:
  kind: measurement
  status: superseded
  superseded_by: entries/2026-11-01-np-16-annulus-corrected-the-arms-had-different-patches-the-velocity-work-is-equal-and-the-serial-patch-costs-5-to-6-percent.md
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892#issuecomment-6550915680
    - https://github.com/underworldcode/underworld3/issues/895
    - https://github.com/lmoresi/uw3-campaigns/blob/main/HUB.md
---

The tail ruling of 2026-11-01 made the drivers' default conditional on one run: the
production faulted annulus at np 16 on `development`, welded base against lean chain.
Kaiju ran it the same day. The welded base wins, by less than on UWTN 2026-022's
fixtures, and for a reason the run makes plain: both arms carry the same finest-level
patch, so only the coarse levels differ. The run also shows where the patch lives in
parallel: all of it on one rank.

## What was tried

`development` 25d62812 (with #912 and #914), the production faulted annulus from TAf
checkpoint 40, four steps, one node per arm, the same checkpoint for both:
`-uw_chain 0` (the welded base) against `-uw_chain 2` (the lean chain).

## What happened

| | chain 0, welded | chain 2, lean chain |
|---|---|---|
| velocity iterations per Newton increment, mean (worst) | 5.9 (8) | 7.7 (10) |
| Stokes time per step, mean | 448 s | 467 s |
| Newton iterations per step | 6 to 7 | 6 to 7 |

vrms agrees to 2e-6 relative and the peak slip to 0.01 in about 6000. No solve reached
the cap and no preconditioner fell back. Both arms carried the same finest-level patch,
465 owned rows on the solving mesh. The whole patch and all 105 split node pairs are on
one of the 16 ranks, because the fault lies inside one partition, so the patch's LU
solve is serial on that rank. The science hub reports chain 0 about 1.5 times slower
than chain 2 on the older overlay build without #912, which is the ILU-block story of
the finding entry of today seen once more.

## What we now think

- The ruling's condition is met and the drivers' `uw_chain` default moves to 0 when
  the campaign's builds move to `development`. With that, every line of the decision
  entry's "where enforced" has an owner and a date.
- The annulus margin (a quarter fewer velocity iterations, four per cent of Stokes
  time) is not the fixtures' factor of 3 to 16. On the fixtures the chain had no patch
  and the welded tail had an LU one; here both arms have the same LU patch on the
  finest level, and the difference is the coarse levels alone. The dramatic numbers
  measured the patch; the annulus measures the tail, and the tail's gain is modest and
  real. A claim that the welded tail is "3 to 16 times faster" is a claim about the
  patch and should be worded so.
- The serial patch is the gathered-star trade of ruling 1 (the fault's cell star on one
  rank, no communication inside the contact solve). At 465 rows it costs little; at
  higher rank counts, or with several faults in one partition, it is a load-imbalance
  term, and the LU block grows with the band's rows. #895 tracks it. UWTN 2026-022's
  multigrid section carries a paragraph on it.

## Verdict

Kept. Closes the last line of the decision entry of 2026-11-01 (the drivers' default),
pending the driver commit, which the science hub owns. Feeds the fault-multigrid and
faults-in-convection guides (both cite it beside the fixtures) and the parallel section
of the fault-multigrid guide.
