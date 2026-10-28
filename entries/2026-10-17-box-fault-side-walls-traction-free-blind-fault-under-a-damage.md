---
title: "Box fault: side walls traction-free, blind fault under a damage band"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/52aa8c9f506a59cee7abb3c03c0f9da0d217fdb4"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`52aa8c9f`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/52aa8c9f506a59cee7abb3c03c0f9da0d217fdb4) by Louis Moresi, 2026-10-17: **Box fault: side walls traction-free, blind fault under a damage band**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

*Figure 1. (a) A viscoelastic block with a vertical strike-slip fault that breaks the free surface; one end face is fixed, the other carries a harmonic traction; the sides are traction-free (or held at $u_x = u_z = 0$ if the open box proves too soft); the base is free-slip. Further faults are added later. (b) The end load: a normal traction and a horizontal shear traction, both harmonic at the orbital period, with a phase lag between them.*
The box model isolates the mechanism. A finite, vertical strike-slip fault that reaches the surface (blind under a damage zone in the first build, see Implementation) with Coulomb friction sits in a three-dimensional Maxwell block. One end of the block is held fixed; the other is driven by a traction with a normal component $N\sin(\omega t + \phi)$ and a horizontal shear component $S\sin(\omega t)$, the two-component periodic load that the tide applied at the stripes in the shell. The side faces are left unconstrained (traction-free); if that leaves too much of the box open, they are held at $u_x = u_z = 0$ instead, so material may leave through them but not slide along them. There is no history to transport across them. The base is free-slip; the top is a free surface.
- **Fault.** A planar fault in a 3-D mesh is placed and split into coincident node pairs (`BoxInternalPatch`, `split_along_label_3d`, `add_fault`), and the regularised Coulomb law with two in-plane slip components and the clamping from the no-opening reaction (`add_coulomb_fault_bc`) is in place and tested (`tests/test_0848`). The splitter welds the rim of the patch and refuses a patch that reaches the boundary, so a surface-breaking fault needs the rim rule relaxed where the rim lies in the free surface (the trace nodes are then pairs, not welds). The standing 3-D ruling is that a fault reaches daylight blind under a damage region, never split through the surface, and the placement supports it directly (`place_sheet(setback=...)` returns the would-be surface trace as the locator of the damage band). The first build uses this: a blind split fault a few cells below the surface with a weak band above it to the free surface.
- **Boundary conditions.** Fixed end, harmonic traction on the other end (`add_natural_bc` with time-dependent sympy expressions), traction-free sides (fallback $u_x = u_z = 0$; Underworld3 has no periodic box), free-slip base, free top.
