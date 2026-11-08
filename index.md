---
title: Underworld journal
---

The lab journal of the Underworld project: what was tried, what happened, and
what we now think, one dated entry at a time. Entries are never edited; a topic
page says what currently stands, and the weekly digest says what moved.

## This week

[Week 44: 20 to 27 October 2026](digests/2026-W44.md)

## Topics

**Topics**

- [Fault multigrid](topics/fault-multigrid.md) · 35 live
- [Particle-to-field projection](topics/particle-to-field-projection.md) · 5 live
- [Shear-band length scales](topics/shear-band-length-scales.md) · 25 live
- [Solvers and multigrid](topics/solvers-and-multigrid.md) · 33 live
- [Transport histories](topics/transport-histories.md) · 5 live
- [Constitutive models](topics/viscoelastic-constitutive-models.md) · 8 live
- [Viscoelastic stretch at large steps](topics/viscoelastic-stretch-at-large-steps.md) · 6 live

**Benchmarks**

- [Benchmarks](benchmarks/benchmarks.md) · 5 live
- [Confined cylinder benchmark](benchmarks/confined-cylinder-benchmark.md) · 0 live
- [Creeping confined cylinder benchmark](benchmarks/creeping-confined-cylinder-benchmark.md) · 0 live
- [Cross-slot benchmark](benchmarks/cross-slot-benchmark.md) · 0 live
- [Spiegelman notch benchmark](benchmarks/spiegelman-notch-benchmark.md) · 0 live
- [Viscoelastic steady shear benchmark](benchmarks/viscoelastic-steady-shear-benchmark.md) · 0 live
- [Waters King start-up benchmark](benchmarks/waters-king-start-up-benchmark.md) · 0 live

**Campaigns**

- [A strike-slip fault under cyclic loading: the box toy model](campaigns/box-fault-cyclic-loading.md) · 13 live
- [Cylinder campaign, September–October 2026](campaigns/cylinder-campaign-2026.md) · 2 live
- [Spiegelman notch campaign, July–October 2026](campaigns/spiegelman-notch-campaign-2026.md) · 1 live
- [Tidal response of a faulted thin shell](campaigns/tidal-faulted-shell.md) · 6 live

## Recent entries

- 2026-11-08 · [Measure the two-level FAC patch against #934's one block in parallel, by wall time and memory, before any 3-D work: the serial iteration comparison that held it could not show its case (Louis, 2026-11-08)](entries/2026-11-08-measure-the-two-level-fac-patch-against-one-block-in-parallel-before-3d.md) · decision
- 2026-11-05 · [The multigrid coarse solve has one rule on every route: redundant LU with a nonzero factor shift, the null space fixed on the fine level, and no SVD path (Louis, 2026-11-05)](entries/2026-11-05-the-coarse-solve-has-one-rule-on-every-route-redundant-lu-with-a-zero-pivot-shift-and-no-svd-path.md) · decision
- 2026-11-05 · [No example needs an SVD coarse solve: 44 examples and tutorials lose the line, measured on hyperion where they run, and the one coarse-solve rule is in code and docs on A-prime (closes the 2026-11-05 decision)](entries/2026-11-05-no-example-needs-an-svd-coarse-solve-44-files-measured-on-hyperion-the-one-rule-is-in-code-and-docs.md) · measurement
- 2026-11-03 · [The ladder is equant: its half-width is one cell and its rungs are about one cell apart, so recipe v2 stands, and the fault-division design goes to a plate-boundaries module (Louis, 2026-11-03)](entries/2026-11-03-the-ladder-is-equant-half-width-one-cell-and-rungs-at-about-one-cell-recipe-v2-stands-and-the-division-design-goes-to-a-plate-boundaries-module.md) · decision
- 2026-11-03 · [The fault's division and the band's width are not knobs: the ladder is built from the fault's own points, and the band is as wide as the local mesh size (Louis, 2026-11-03, clarifying decision 1b)](entries/2026-11-03-the-faults-division-and-the-bands-width-are-not-knobs-the-ladder-is-built-from-the-faults-own-points-and-the-width-is-the-local-mesh-size.md) · decision
- 2026-11-02 · [The campaign drivers default to uw_chain 0 (b440b88), accepted on kaiju at np 16 on development 25d62812: the last 'where enforced' line of the 2026-11-01 tail decision is done, and the drivers' decisions ledger is citable](entries/2026-11-02-the-drivers-default-to-uw-chain-0-the-last-where-enforced-line-of-the-tail-decision-is-done.md) · measurement
- 2026-11-02 · [The add-on is the line to invest in for split faults: the fault carries its own resolution as a divided line, and split coarse levels are not developed further (Louis, 2026-11-02)](entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md) · decision
- 2026-11-02 · [seams='conform' cannot place a fault that reaches the domain wall in 2-D (the network mesher's cavity reaches the wall), and the ladder takes only gather: dividing the FAC patch across ranks is blocked for every surface-reaching fault until one of the two changes](entries/2026-11-02-conform-seams-cannot-place-a-wall-reaching-fault-in-2d-so-the-patch-cannot-be-divided-across-ranks-in-the-trench-models.md) · dead-end
- 2026-11-01 · [The production multigrid tail for a split fault is the welded base with the split S level on top and the FAC LU patch on that finest level; the chain of split ladders is the measured alternative, not the production tail (Louis, 2026-11-01)](entries/2026-11-01-the-production-tail-for-split-faults-is-the-welded-base-with-the-fac-lu-patch-on-the-split-finest-level.md) · decision
- 2026-11-01 · [The FAC patch is on one rank by construction: the default placement, seams='gather', runs partition_addon first and gives the band's region to one rank at any rank count; the serial patch solve measured at np 16 comes from the placement, not from the welded tail](entries/2026-11-01-the-patch-is-on-one-rank-by-construction-the-default-gather-placement-not-the-welded-tail.md) · finding
- 2026-11-01 · [The np 16 annulus pair ran at a band ratio of 3.9, below the smallest ratio in UWTN 2026-022's sweep table (6.06 to 24.8), which is why the welded tail's patch bought nothing measurable there; the runs used the library's default tolerances, and a pressure rtol of 1e-2 halves the solve with the same answer](entries/2026-11-01-the-annulus-pair-ran-at-band-ratio-3-9-below-the-sweep-table-which-is-why-the-patch-bought-nothing-there.md) · finding
- 2026-11-01 · [The np 16 annulus, corrected by kaiju's budget: the welded arm carried a 3584-row patch on one rank and the chain none; the velocity work is equal (8.65 against 8.74 F-cycles per solve) and the times are a wash; the serial patch LU costs 5 to 6 % of the solve, not little](entries/2026-11-01-np-16-annulus-corrected-the-arms-had-different-patches-the-velocity-work-is-equal-and-the-serial-patch-costs-5-to-6-percent.md) · measurement
- 2026-11-01 · [The production annulus at np 16 confirms the welded tail by a small margin (5.9 against 7.7 velocity iterations per Newton increment, the same answers), because both arms carry the same finest patch; that patch, 465 rows and 105 split pairs, sits on one rank, so its LU solve is serial](entries/2026-11-01-np-16-annulus-confirms-the-welded-tail-by-a-small-margin-and-the-patch-is-serial-on-one-rank.md) · measurement
- 2026-11-01 · [FAC patch blocks are LU and ILU there is a regression: the LU block solve of #670 was measured, made the default and never ran on the rotated path, because the composite's ASM child read the options after the rotated path had deleted them (#892, fixed by #912)](entries/2026-11-01-fac-patch-blocks-are-lu-the-design-was-adopted-and-never-ran-on-the-rotated-path.md) · finding
- 2026-10-31 · [Band-ratio sweep: a welded base with the FAC patch solved by LU takes 3 velocity iterations at every ratio from 6 to 25 and beats every split chain; the chains never get the patch, and the rotated path runs the patch as ILU(0) (#892)](entries/2026-10-31-band-ratio-sweep-welded-base-with-a-fac-lu-patch-beats-every-chain-once-892-is-fixed.md) · measurement
- 2026-10-30 · [The tail ruling is provisional above a band ratio of about 8: a sweep of three hierarchies on the production ladder is commissioned before any result is published](entries/2026-10-30-the-tail-ruling-is-provisional-above-a-band-ratio-of-about-8-pending-a-sweep.md) · decision
- 2026-10-30 · [The production chain puts the 2S ladder on the base's finest level, beside the S ladder, and the 4S ladder one level down; the rig's band-ratio table is confounded with cell aspect](entries/2026-10-30-the-production-chain-puts-2s-on-the-finest-base-level-and-4s-one-level-down.md) · finding
- 2026-10-30 · [Ladder levels nest along the spine, not by vertices, when the band widens with the level as production does](entries/2026-10-30-ladder-levels-nest-along-the-spine-not-by-vertices-when-the-band-widens.md) · finding
- 2026-10-29 · [Which multigrid tail goes under the finest ladder: the lean split chain in production; a single ladder over the welded base only on a linear rig up to a band ratio of about 12](entries/2026-10-29-which-tail-under-the-finest-ladder-the-lean-split-chain-in-production.md) · decision
- 2026-10-29 · [A per-level wall rotation cuts a rotated free-slip custom-FMG solve on an adapted annulus from 18 serial and 197 parallel velocity iterations to 3 and 4](entries/2026-10-29-per-level-wall-rotation-cuts-rotated-freeslip-fmg-iterations-on-an-adapted-annulus.md) · measurement

[All entries](entries.md)
