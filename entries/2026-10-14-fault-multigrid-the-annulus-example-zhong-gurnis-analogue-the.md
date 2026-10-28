---
title: "Fault multigrid: the annulus example (Zhong & Gurnis analogue), the outcropping ladder, the coarse-level wall rotation, meshing against solve"
date: "2026-10-14"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/50400a8d226df46eeeabdc780f95766b2b4db7d5"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`50400a8d`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/50400a8d226df46eeeabdc780f95766b2b4db7d5) by Louis Moresi, 2026-10-14: **Fault multigrid: the annulus example (Zhong & Gurnis analogue), the outcropping ladder, the coarse-level wall rotation, meshing against solve**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

## An annulus example: the Zhong & Gurnis (1995) analogue
The target model is mantle convection with a plate and a mobile, faulted margin (Zhong & Gurnis, Science 267, 838, 1995): a temperature-dependent lid, a dipping fault at the trench that moves with the overriding plate, surface velocity and dynamic topography read from the solution. The driver is `scripts/sessions/fault_mg/zg95_annulus.py` (branch `feature/fault-split-multigrid`), the probe `zg95_probe.py`, the profile `zg95_profile.py`.
**The construction.** The base annulus ($r_i = 0.55$, coarsest cell 0.16 halved three times to 0.02) carries the temperature and the semi-Lagrangian advection-diffusion, and is never cut or rebalanced. The add-on finest is a copy of the base's finest with the trench placed as the structured ladder: spacing 0.005, one element either side of the spine, dipping 45 degrees from above the surface through the lid to a depth of 0.15, outcropping through the ladder's cap. The spine is split on its rung vertices from three spacings below the surface down (no pair node ever sits on the wall, so the wall and pair frames never cross); the cap and the last rungs are painted transversely isotropic (contrast $10^{-3}$) to bridge the split to the surface. Stokes on the add-on: viscosity $\eta = \exp(\ln 10^{3}\,(1 - T))$, $Ra = 10^{6}$, rotated free-slip on both walls with the exact radial normal, frictionless contact on the spine, custom FMG on the base's own four levels. The velocity goes back to the base by evaluation for the advection step, and the trench is advected with the surface velocity just on the overriding side; the add-on is rebuilt when it has moved by a rung.
![the trench on the annulus](../figures/fault-mg-zg95_probe_mesh.png)
*The add-on finest at the trench: regular rungs with one element either side are the ladder, the orange cells at the surface the cap; the split spine (red Plus, blue Minus) stops three spacings below the surface and the bridge carries it to the outcrop. Velocity magnitude under the mesh.*
![the first step](../figures/fault-mg-zg95_first_step.png)
*The driver's first fault step: temperature on the base with the trench, the surface velocity with its step at the fault, the topography with the trench's low and high on top of the convective pattern.*
**What it cost to get there**, each a defect in machinery that had only ever run on boxes:
| defect | symptom | fix |
|---|---|---|
| the placer's domain tool took the annulus loops in whatever winding the walk returned | at cell sizes 0.04 and 0.08 the hole was added as area and the band met nothing | every loop counter-clockwise |
| the 2-D outcrop frame read each chord of the faceted wall as its own wall | a dipping band's clearance cavity refused as contact away from the outcrop; once allowed, the splice chorded across the curve's vertices and lost the sagitta | chords grouped into smooth walls (the 3-D rule); the splice keeps the surviving wall vertices |
| the structured ladder could not outcrop at all | neither realisation could reach the surface; the fallback was an unstructured band with a cut through it | the ladder runs to one rung short of the wall and a clipped cap closes it |
| the orphan rule dropped only exactly unreached coarse unknowns, before the finest's constrained rows were zeroed | wall unknowns with Galerkin diagonals of $10^{-20}$ | relative reach, after the zeroing |
| Cartesian coarse levels under a rotated finest | a coarse wall node's normal component is reached only through fine tangential rows weighted by a vanishing sine; the inode SOR's nodal block inversion hit a zero pivot and the velocity solve failed before its first iteration | every coarse level takes the wall rotation on its own nodes and loses its normal rows |
| the free-slip gauge mode | rejected with facet-averaged normals on an irregular polygon, so the coarse LU met a singular operator | the exact radial normal; and the SVD coarse solve that follows needs a small coarsest level (14k unknowns took over 30 minutes, 900 is instant) |
**Measured.** The probe solve: 10 velocity iterations, slip 1.80; the same case on GAMG 119 iterations. The driver's first fault steps: 14, 12, 14 velocity iterations, slip 3.5, the trench creeping with the overriding plate. One rank against two on the identical two-step case: slip 3.6995 against 3.7005, trench velocity 1.590 against 1.591, topography the same to $10^{-4}$, the solve 60 s against 35 s.
**Meshing against the solve.** Per step on one rank at 15k cells: the base and its levels 2 s once; placement, cap and split 5 s, recurring when the trench has moved a rung (about every twenty steps here); the temperature transfer 1.5 s; the solve 56 to 62 s, of which the hierarchy set-up is the 6 s difference between the first solve and a repeat with the temperature changed. The remaining 50 s is Krylov work, nearly all of it inside the pressure Schur complement, which applies the velocity multigrid at each of its 17 iterations. So the meshing is under a tenth of a rebuilding step and under one percent amortised; the step is the solve, and the solve is the Schur iteration count and the smoother, which is tuning, not meshing.
