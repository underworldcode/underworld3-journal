---
title: "The np 16 annulus, corrected by kaiju's budget: the welded arm carried a 3584-row patch on one rank and the chain none; the velocity work is equal (8.65 against 8.74 F-cycles per solve) and the times are a wash; the serial patch LU costs 5 to 6 % of the solve, not little"
date: 2026-11-01
authors: [kaiju session (science hub), reported by Louis Moresi on underworld3 #892; recorded by the docs hub]
options:
  kind: measurement
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892#issuecomment-6552218825
    - https://github.com/underworldcode/underworld3/issues/895
    - entries/2026-11-01-np-16-annulus-confirms-the-welded-tail-by-a-small-margin-and-the-patch-is-serial-on-one-rank.md
---

Kaiju measured where the time goes in the np 16 annulus pair of this morning (jobs 2480
to 2488, steps 41 to 43 from TAf checkpoint 40, `development` 25d62812, one node per
arm), and the budget corrects two statements of the earlier entry, which this one
supersedes. The arms did not carry the same patch, and the velocity work is equal.
What stands: the welded tail is no worse than the chain on the production annulus, the
answers agree, and the patch's LU solve is serial on one rank at a cost that is now
measured.

## What was wrong

- **The patches differ.** Both arms solved on the same rebuilt mesh. In the multigrid
  the Stokes solve applies, chain 0 (the welded base) has a finest-level patch of 3584
  rows, all on one rank, and chain 2 (the lean chain) has no patch at all. The 465-row
  patch of the earlier entry belongs to a second multigrid that each solve also
  configures under the solver's own prefix, applied 50 times in 3 steps. So the pair
  compares patch against no patch, as the box table does, and the earlier reading that
  "the difference comes from the coarse levels alone" is wrong.
- **The velocity work is equal.** The 5.9 against 7.7 velocity iterations per Newton
  increment counted only the last velocity solve of each increment. Over every velocity
  solve, chain 0 takes 8.65 F-cycles per solve and chain 2 takes 8.74.
- **"Costs little" was wrong.** Chain 0's patch solve runs on the rank that holds the
  fault while the other 15 wait (max/min time ratio 165 to 178): 21 to 28 s a step,
  5 to 6 % of the solve at np 16.

## What happened

Per step, the mean over steps 41 to 43:

| | chain 0, welded | chain 2, lean chain |
|---|---|---|
| Stokes solve | 441 s | 410 s |
| F-cycles | 2489 | 2527 |
| FAC patch LU, on one rank | 21 to 28 s | none |

With the earlier pair (448 s against 467 s) the two tails take the same time to within
the ±10 % spread between repeated runs. Both arms reach the same answer with the same
Newton counts, from rest, warm or after a rebuild, and neither needed a cold retry.

## What we now think

- The ruling's condition is met in the sense that matters: on the production annulus
  at np 16 on `development` the welded tail is no worse than the chain in work or time
  and gives the same answers, with one hierarchy fewer to build. The drivers' `uw_chain`
  default moves to 0 as the campaign builds move to `development` (science hub).
- The gain the fixtures show (4 to 11 times fewer velocity iterations per Newton
  increment on the box) does not appear on the annulus, and the pair is patch against
  no patch there too. Why is open; the science hub has been asked for the annulus band
  ratio, the first suspect.
- The serial patch is the gathered-star trade of ruling 1 and it is not free: 5 to 6 %
  of the solve at np 16, growing with the rank count or with several faults in one
  partition (#895). The structural patch is one block per rank with no row cap; the
  2000-row cap (`fac_block_rows`, `UW_FAC_BLOCK_ROWS`) cuts only the blocks built from
  `fac_zone` masks. One block is the measured 2-D choice (one block beat the slip coarse
  space); its cost in 3-D is #895.
- Two wordings now retired: the earlier entry's "the welded tail's own gain is a quarter
  of the iterations" (it was patch against no patch, and the work is equal), and any
  "3 to 16 times faster" read as a statement about the tail rather than the patch. UWTN
  2026-022 names its table rows by smoother and concludes "the welded base is enough
  when the patch is solved exactly", which is the statement the evidence supports.

## Verdict

Kept; supersedes the np 16 entry of this morning. Feeds the fault-multigrid guide's
production paragraph and parallel section, the faults-in-convection guide's hierarchy
section, and the topic page. The annulus band ratio, when it comes, is a follow-up
entry.
