---
title: "Box fault: implementation status (mesher, damage band, ported fixes)"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/3387557cae192cf7b2819ad98cb7f381d66fd3e2"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`3387557c`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/3387557cae192cf7b2819ad98cb7f381d66fd3e2) by Louis Moresi, 2026-10-17: **Box fault: implementation status (mesher, damage band, ported fixes)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

**Status (2026-10-17, evening): driver written and in smoke testing; library fixes ported; nothing run to results yet.** Branch `feature/tidal-shell`, scripts `scripts/sessions/box_fault_cyclic/box_fault_cyclic.py` (driver) and `box_fault_plot.py` (figures).
- **Mesh and fault.** The default route is a gmsh box with the fault as a conforming interior patch (`BoxInternalPatch`), graded from the fault cell size (0.05) to the far field (0.15), with the patch top set back two fault cells below the surface. The alternative route, a uniform box with the sheet placed by carving a cavity (`add_conforming_sheet(setback=...)`), needs a setback of three to four cells because any dropped cell touching the top face is refused; that is too thick a lid for a fault half a box deep, so it is kept only as an option. Either way the patch is split into coincident node pairs (`split_fault`). The standing 3-D ruling applies: the fault reaches daylight blind, under a damage region, and is never split through the surface.
- **Damage band.** A low-viscosity region (ratio 0.01 by default) one fault cell wide either side of the trace, from the fault top to the free surface, located by the fault's would-be surface trace. The shear modulus is not reduced there.
- **Rheology.** Maxwell (`ViscoElasticPlasticFlowModel`, ETD integrator, no objective rate), shear modulus 1, viscosity De in periods, so the Wallace number is 1/De. De = 0 gives a viscous block.
- **Boundary conditions.** The x = 0 face fixed; on x = Lx the traction (N sin(ωt + φ), S sin(ωt), 0) through two uniform P1 fields that are updated each step, so the residual is compiled once; the y faces traction-free (option: u_x = u_z = 0; Underworld3 has no periodic box); the base u_z = 0; the top free.
- **Fault laws.** Regularised Coulomb from the no-opening reaction with a constant overburden (`add_coulomb_fault_bc(mu, sigma_n="reaction", V0, background=T_b)`), or a viscous or frictionless interface.
- **Diagnostics (all collective).** Signed strike slip at every pair each step (`fault_pair_jumps`, all-gathered), accumulated per cycle and in total; the fault normal traction; the surface velocity on a fixed grid integrated to a net displacement per cycle; a per-cycle `cycle_NNNN.npz` and a `records.json` of step scalars.
- **Library fixes brought in from `feature/mohr-triaxial`** (one commit): the 3-D fault normal traction recovered pointwise (the P2-triangle load against P1 lumped masses read zero at vertices and 4/3 at midpoints), with the branch keyed on facet topology so the surface-mesh edge fault is unchanged; the sheet-cavity closure for the three shapes that defeated it on adapted meshes; a single `split_fault` now keeps the mesh's multigrid tail. Tests in `test_0848` and the new `test_0867`.
- **Open on the solver side.** No fault multigrid ladder in 3-D yet (GAMG); the serial 3D solves are slow (the Mohr sweep measured 6 to 12 minutes per solve on 21k cells), so production runs go to hyperion in parallel; the natural-traction sign convention is being confirmed by a pure normal load (a positive normal traction on the loaded face must pull it outward).
