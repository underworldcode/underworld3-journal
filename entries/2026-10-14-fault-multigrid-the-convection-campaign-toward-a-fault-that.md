---
title: "Fault multigrid: the convection campaign toward a fault that matters (in progress); the inode rule"
date: "2026-10-14"
authors:
  - "Louis Moresi"
options:
  kind: "decision"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/cada0a93793e0d4b3cd666c1cfbfe1b4e0e8720d"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`cada0a93`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/cada0a93793e0d4b3cd666c1cfbfe1b4e0e8720d) by Louis Moresi, 2026-10-14: **Fault multigrid: the convection campaign toward a fault that matters (in progress); the inode rule**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

**Toward a convection run where the fault matters (in progress, 2026-10-14 evening).** The purely viscous state above has no bendable plate and no ridge, so the fault cannot organise plate motion. The campaign now running (`zg95_annulus.py --heating --yield0 --yield_depth`, eight ranks each, 600 steps) adds internal heating of 10 with the base held at $T = 1$ (a weak lower boundary layer), a viscosity contrast of $10^{4}$ in temperature, and a yield stress: constant at $10^{4}$, $3\times10^{4}$ and $10^{5}$, and one arm with $2\times10^{3}$ at the surface rising by $10^{5}$ per unit depth, so that yielding is easy but confined to the cold boundary layer. Each step logs mobility (surface rms over volume rms), the lid depth from the horizontally averaged profile, and the yielded fraction of nodes overall and within the top 0.15. First steps: the $10^{5}$ arm is a stagnant lid (mobility 0.05, lid thickening past 0.17); the depth-dependent arm is mobile at once (mobility 0.9 to 1.0, a third of the lid nodes yielded, 4 to 14 Newton iterations per step after the first). The fault phase will restart from each arm's checkpoint with the same rheology on the add-on (the bridge an isotropic weak zone, since the TI model carries a yield stress only with elasticity), and the question is whether the plate away from the fault yields less once the fault carries the convergence.
The two machinery arms on the viscous state (split spine with the TI bridge, and TI all the way) are running to 200 steps meanwhile; both converge at every step through the trench's rebuilds (the split arm's slip 9.8 to 10.0, the trench migrating with the overriding plate), and the rotated level operators now drop PETSc's inode grouping, after a four-rank restart met a singular 2x2 block in the inode SOR on the base's two finest levels with every scalar diagonal healthy.
