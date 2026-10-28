---
title: "Box fault: ETD expression-viscosity bug, stress-history flavour, cost"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "box-fault-cyclic-loading"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/d70da590716dfd9a720495de5c971f074cd8eff2"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`d70da590`](https://github.com/underworldcode/underworld3/wiki/Box-fault-cyclic-loading/d70da590716dfd9a720495de5c971f074cd8eff2) by Louis Moresi, 2026-10-17: **Box fault: ETD expression-viscosity bug, stress-history flavour, cost**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Box fault cyclic loading

**Status (2026-10-17, midday): the driver runs in parallel with geometric multigrid, a silent integrator bug found on the way is fixed, the stress-history flavour is settled; no science runs yet.** Branch `feature/tidal-shell` (pushed), scripts `scripts/sessions/box_fault_cyclic/box_fault_cyclic.py` (driver) and `box_fault_plot.py` (figures).
- **Rheology.** Maxwell (`ViscoElasticPlasticFlowModel`, ETD integrator, no objective rate), shear modulus 1, viscosity De in periods, so the Wallace number is 1/De. De = 0 gives a viscous block. *Bug found and fixed here:* the ETD coefficients took the viscosity as a float, and a viscosity that varies in space (the damage band) made that fail and fall silently to the viscous limit, so the whole block lost its elastic response (first-step end velocity 0.007, the viscous value, against 0.061 with a constant viscosity). The coefficients are now formed symbolically when the Maxwell time is an expression; `tests/test_1093` holds the regression (a uniform-valued expression must match the constant; a weak band must not make the block viscous). Every box run before the fix was effectively viscous.
- **Stress history.** The solver's default history is semi-Lagrangian. On a uniform block all flavours reproduce the exact Maxwell creep benchmark (`tests/test_1094`: ETD-1's first step is the creep rate over $1 - e^{-x}$, then the creep rate, all within 3 %). On the faulted box the semi-Lagrangian and Eulerian flavours disagree by a quarter on the second step's slip rate: the trace-back queries a field that is double-valued across the split, and a point query sees one side only. The displacement per step here is far below a cell, so the history is kept on the grid with no transport at all (`stress_transport = "none"`, added to `Stokes` for this), which is also the cheapest: the semi-Lagrangian history cost about 45 s of the 95 s step.
- **Cost.** With the true Maxwell response the pressure solve takes 36 iterations (10 when the block was effectively viscous) and the velocity solve 27, so a step is about 110 s on 8 ranks at 16k cells with the semi-Lagrangian history under load; the no-transport history removes its share. Loosening the solver tolerance from 1e-3 to 1e-2 saved a quarter at most, and the 100:1 damage band is not what drives the iteration count (26 velocity, 15 pressure without it). The problem needs to be smaller or the Schur loop cheaper before parameter sweeps; the base mesh and the box aspect are the first knobs, periodic side walls (a new meshing capability) the second.
