---
title: "Cylinder campaign, September–October 2026"
options:
  kind: "campaign"
  migrated_from: "https://github.com/underworldcode/underworld3/wiki/Cylinder-campaign-2026"
  wiki_created: "2026-10-05"
  wiki_last_edited: "2026-10-16"
---

```{note}
Migrated from the wiki page [Cylinder-campaign-2026](https://github.com/underworldcode/underworld3/wiki/Cylinder-campaign-2026) on 2026-10-27 as this campaign page's starting text (written 2026-10-05 to 2026-10-16). The dated entries at the foot are the record; this text is trimmed as its content moves into guides, subsystem pages and entries.
```


A confined cylinder (DFG 2D-2 geometry, channel 2.2 × 0.41, cylinder diameter 0.1) at Re 200 and Re 100, β 0.5, Wi 0.5 to 2, three resolutions, every stress history and both reconstructions, Oldroyd-B and FENE-P. Driver and scripts: the `ve_cylinder_demo` campaign (to be moved into a repository; roadmap item). What the campaign taught us is recorded on the topic pages; this page says what we ran and what came out.

## The meshes

![res 20 and res 40 meshes](../figures/cylinder-meshes.png)

*The gmsh base is built two refinement levels coarser and refined back with the new vertices snapped to the circle, so the velocity block has a multigrid hierarchy. Res 20 puts two cells across a diameter in the wake; res 40 four. dt is set by Courant one at the cylinder, so the wake runs at Courant 0.25 (res 20) or 0.5 (res 40).*

## What it looks like

Each movie has two panels: the stress-history magnitude (asinh scale) with streamlines above, vorticity (−40 to 40) with tracers from two off-centre smoke sources below. Frames near t 7.5, Re 200, Wi 0.5, res 20, all with the stress by global projection unless marked.

![Newtonian](../figures/frame_newtonian.jpg)
*Newtonian: the Kármán street at Re 200.*

![Eulerian](../figures/frame_grid.jpg)
*Eulerian momentum and stress (SUPG + DEVSS): the "nicest" vortices at this resolution, which the resolution study says is an artefact.*

![forward nodes, global projection](../figures/frame_nodal_forward_global.jpg)
*Forward-nodes momentum and stress, global projection: coherent street, St 0.26.*

![SUPG momentum, forward global stress](../figures/frame_supg_fwn_global.jpg)
*SUPG momentum with the forward global stress: St 0.30 follows the velocity history.*

![free-slip cylinder](../figures/frame_grid_freeslip.jpg)
*Free-slip cylinder: no shedding, one steady birefringent strand.*

![Re 100 Wi 0.5 res 40 forces](../figures/re100_wi05_r40_forces.png)
*Re 100, Wi 0.5, res 40: lift and drag for every stress scheme (see [Confined cylinder benchmark](../benchmarks/confined-cylinder-benchmark.md)).*

![FENE-P Wi sweep at res 20](../figures/re100_fene_r20_lift.png)
*FENE-P at res 20 on the log(f c) record: Wi 0.5 and 1 shed weakly; Wi 2 is not resolved on this mesh.*

## Results that stand

Re 100, Wi 0.5, res 40, settled window t 6 to 8, cd and lift amplitude:

| stress history | cd | cl amp |
|---|---|---|
| Newtonian (DFG reference cd 3.22–3.24, cl 0.99–1.01) | 3.14 | 1.01 |
| FENE-P, forward, global projection | 3.25 | 0.07 |
| Oldroyd-B, forward, global projection | 3.68 | 0.001 |
| SUPG momentum, forward global stress | 3.50 | 0.07 |
| Oldroyd-B, forward, cell fit | 4.22 | 0.24 (growing) |
| Eulerian stress (SUPG + DEVSS) | 4.33 | 0.52 |

The global projection suppresses the shedding; the cell fit and the Eulerian stress keep it. Which is right is the open question ([Particle-to-field projection](../topics/particle-to-field-projection.md), [Transport histories](../topics/transport-histories.md)).

Re 200: lift collapses with resolution in every scheme (Eulerian 3.7, 2.9, 0.7 at res 20, 40, 80; forward 1.7, 0.3). The forward family converges on itself at res 40.

FENE-P at res 20: Wi 0.5 cd 3.44, cl 0.29; Wi 1 cd 3.23, cl 0.25; Wi 2 unresolved (ran to t 7.1 then blew up). Oldroyd-B Wi 2 fails at every resolution.

Free-slip cylinder: steady, no shedding, one birefringent strand.

## Results to discount

Runs between 2026-10-04 16:30 and 2026-10-05 23:08 with a global-projection stress carry the first deficit fill's bias (nodal_forward_global3, r40_fwd_Wi1, r40_fwd_Wi2, r20_fwd_Wi2). FENE-P runs before 2026-10-05 13:00 used the log-c record and hung.

## Lessons recorded elsewhere

The FENE-P record ([Constitutive models](https://github.com/underworldcode/underworld3/wiki/Constitutive-models)); the deficit fill and the limiter ([Particle-to-field projection](../topics/particle-to-field-projection.md)); St follows the velocity history, and lift collapses with resolution ([Transport histories](../topics/transport-histories.md)); the stall that looked like a hang ([Solvers and multigrid](../topics/solvers-and-multigrid.md)); the benchmarks and the next target ([Benchmarks](../benchmarks/benchmarks.md)); why the implicit stretch stalls at Courant 8 on the wall cell and how runs now get through it ([Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md)).

## Next

The res-80 pair at Re 100 Wi 0.5 (Eulerian stress against forward global). Wi 2 at res 40. Then the creeping confined-cylinder benchmark.

## History

- 2026-10-05 — created at the end of the overnight queue and the FENE-P fix; meshes, frames and force traces added.
- 2026-10-16 — the large-step runs at resolution 40 with wall cells 1/8 (implicit, tangent, linear, lagged, switching; Jacobian dumps) recorded on [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md).

<!-- BEGIN ENTRIES (generated by scripts/build_index.py; do not edit) -->

## Entries

- 2026-10-05 · [Working notes: topic pages (constitutive models, transport histories, projection, solvers, benchmarks), the cylinder campaign, how we plan](../entries/2026-10-05-working-notes-topic-pages-constitutive-models-transport.md) · finding
- 2026-10-05 · [Equations for each VE model and the step; figures: meshes, frames, force traces, validation, convergence](../entries/2026-10-05-equations-for-each-ve-model-and-the-step-figures-meshes-frames.md) · finding

<!-- END ENTRIES -->
