---
title: "Box fault: implementation as built (gmsh patch + registered coarse tail, sign, cost)"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/d0e5112028677bbe7e4bfad2a16542efcdb5068a"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`d0e51120`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/d0e5112028677bbe7e4bfad2a16542efcdb5068a) by Louis Moresi, 2026-10-17: **Box fault: implementation as built (gmsh patch + registered coarse tail, sign, cost)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

**Status (2026-10-17, evening): the driver runs in parallel with geometric multigrid; smoke-tested, no science runs yet.** Branch `feature/tidal-shell` (pushed), scripts `scripts/sessions/box_fault_cyclic/box_fault_cyclic.py` (driver) and `box_fault_plot.py` (figures).
- **Mesh and fault.** A gmsh box with the fault as a conforming interior patch (`BoxInternalPatch`), graded from the fault cell size (0.05) to the far field (0.15), the patch top two fault cells below the surface; the patch is split into coincident node pairs (`split_fault`). The box carries no multigrid tail of its own, so two plain boxes at twice and four times the far-field size are registered as the coarse tail (`set_custom_fmg`, non-nested, barycentric transfers) and the rotated solve takes the custom-P geometric multigrid velocity block. Measured on 8 ranks, 16k cells: 32 velocity and 10 pressure iterations per linear solve, zero normal leak on the fault. A GAMG velocity block is refused by the driver, and the library now warns whenever it falls back to GAMG: the fallback is a symptom of a mesh without its tail, not a configuration.
- **The alternative, adapt-on-top, and why it is not the default.** The designed pipeline (box with one refinement level, adapt toward the fault column, sheet placed by carving a cavity, split) carries its tail automatically, but the cavity reaches about two cell diameters above the sheet top, so a blind fault needs a setback of at least five fine cells (0.20 refused, 0.25 passed at cell size 0.05), and in parallel the placement's gathered region under-reached the grown cavity on this geometry (serial passes). The defect is marked in `place_surface.py`; the route stays an option.
- **Damage band.** A low-viscosity region (ratio 0.01 by default) one fault cell wide either side of the trace, from the fault top to the free surface. The shear modulus is not reduced there.
- **Boundary conditions.** The x = 0 face fixed; on x = Lx the traction (N sin(ωt + φ), S sin(ωt), 0) through two uniform P1 fields updated each step, so the residual is compiled once. The natural-condition value in Underworld3 pushes into the domain when positive (measured: a positive normal value compressed the box), so the traction vector enters negated; N > 0 is tension and the loaded end moves outward. The y faces are traction-free (option: u_x = u_z = 0; there is no periodic box yet); the base has u_z = 0; the top is free.
- **Fault laws.** Regularised Coulomb from the no-opening reaction with a constant overburden (`add_coulomb_fault_bc(mu, sigma_n="reaction", V0, background=T_b)`), or a viscous or frictionless interface. The 3-D normal traction is recovered pointwise (see the ported fixes).
- **Diagnostics (all collective).** Signed strike slip at every pair each step (`fault_pair_jumps`, all-gathered), accumulated per cycle and in total; the fault normal traction; the surface velocity on a fixed grid integrated to a net displacement per cycle; `cycle_NNNN.npz` per cycle and `records.json` of step scalars. A pure normal load on the x-parallel fault gives no strike slip, as it must.
- **Library fixes brought in from `feature/mohr-triaxial`** (one commit, all tests passing here): the 3-D fault normal traction recovered pointwise (the P2-triangle load against P1 lumped masses read zero at vertices and 4/3 at midpoints), keyed on facet topology so the surface-mesh edge fault is unchanged; the sheet-cavity closure for three shapes that defeated it on adapted meshes; a single `split_fault` keeps the mesh's multigrid tail. Tests in `test_0848` and the new `test_0867`.
- **Cost.** 95 s per step on 8 ranks at 16k cells (134 s for the first step with compilation), so a 32-step cycle is about 50 minutes. Where the time goes is the next thing to measure before production runs; the Schur loop applies the velocity multigrid at every pressure iteration.
