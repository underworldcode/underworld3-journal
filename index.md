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

- [Fault multigrid](topics/fault-multigrid.md) · 30 live
- [Particle-to-field projection](topics/particle-to-field-projection.md) · 5 live
- [Shear-band length scales](topics/shear-band-length-scales.md) · 25 live
- [Solvers and multigrid](topics/solvers-and-multigrid.md) · 27 live
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

- 2026-11-02 · [The add-on is the line to invest in for split faults: the fault carries its own resolution as a divided line, and split coarse levels are not developed further (Louis, 2026-11-02)](entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md) · decision
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
- 2026-10-29 · [Under continuation a datum-only cold start skips its Picard phase and still converges in 10 Newton iterations: not a must-fix](entries/2026-10-29-datum-only-continuation-skips-picard-and-still-converges.md) · measurement
- 2026-10-29 · [A datum-only cold start on the rotated path sets its convergence reference from the lifted iterate and takes one increment more than it needs](entries/2026-10-29-datum-only-cold-start-reference-on-the-rotated-path-costs-one-increment.md) · finding
- 2026-10-28 · [Which fault-mesh construction is used in practice: the placed ladder with a hand-built split chain; adapt-and-cut is the automated route the hierarchy was measured on](entries/2026-10-28-which-fault-mesh-construction-is-used-in-practice.md) · finding
- 2026-10-28 · [The fault-split integration head reproduces UWTN 2026-022's numbers; the suites pass but for two failures that predate it](entries/2026-10-28-fault-split-integration-head-reproduces-uwtn-2026-022.md) · measurement
- 2026-10-28 · [Coarse solve on the rotated path: handle the null space, leave the coarse level to PETSc's defaults; MUMPS is not the default](entries/2026-10-28-coarse-solve-null-space-first-petsc-defaults-not-mumps.md) · decision
- 2026-10-18 · [Viscoelastic stretch at large steps: corrections from the adversarial review (Pakdel-McKinley inside the layer, time-scheme cost, tangent at 1/120, SPD scope, conformation-check scope, the refusals, merge order after #800)](entries/2026-10-18-viscoelastic-stretch-at-large-steps-corrections-from-the.md) · measurement
- 2026-10-18 · [Box fault: walk scaling with the Wallace number and the clamping-phase result](entries/2026-10-18-box-fault-walk-scaling-with-the-wallace-number-and-the-clamping.md) · measurement

[All entries](entries.md)
