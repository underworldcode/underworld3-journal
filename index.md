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

- [Fault multigrid](topics/fault-multigrid.md) · 25 live
- [Particle-to-field projection](topics/particle-to-field-projection.md) · 5 live
- [Shear-band length scales](topics/shear-band-length-scales.md) · 25 live
- [Solvers and multigrid](topics/solvers-and-multigrid.md) · 22 live
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
- 2026-10-18 · [Box fault: orientation series (30, 45, 60 degrees) against the in-phase clamping](entries/2026-10-18-box-fault-orientation-series-30-45-60-degrees-against-the-in.md) · finding
- 2026-10-18 · [Box fault: De 0.3 steady walk](entries/2026-10-18-box-fault-de-0-3-steady-walk.md) · finding
- 2026-10-18 · [Box fault: 60 degree walk is left-lateral (slip sense corrected)](entries/2026-10-18-box-fault-60-degree-walk-is-left-lateral-slip-sense-corrected.md) · finding
- 2026-10-17 · [Viscoelastic stretch at large steps: the wall layer measured (extension at the stagnation point, tension on the shoulders, unresolved), FENE-P capped at the same place and step, the consequences for yielding](entries/2026-10-17-viscoelastic-stretch-at-large-steps-the-wall-layer-measured.md) · measurement
- 2026-10-17 · [Tidal faulted shell: mesh figure and resolution notes](entries/2026-10-17-tidal-faulted-shell-mesh-figure-and-resolution-notes.md) · measurement
- 2026-10-17 · [Box fault: the parallel multigrid defect and its fix](entries/2026-10-17-box-fault-the-parallel-multigrid-defect-and-its-fix.md) · finding
- 2026-10-17 · [Box fault: side walls traction-free, blind fault under a damage band](entries/2026-10-17-box-fault-side-walls-traction-free-blind-fault-under-a-damage.md) · finding
- 2026-10-17 · [Box fault: post-fix step cost; first run in progress](entries/2026-10-17-box-fault-post-fix-step-cost-first-run-in-progress.md) · measurement

[All entries](entries.md)
