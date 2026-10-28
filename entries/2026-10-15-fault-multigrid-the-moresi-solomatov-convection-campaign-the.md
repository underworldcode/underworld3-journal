---
title: "Fault multigrid: the Moresi-Solomatov convection campaign, the fault sequence, the solver item and the hand-over"
date: "2026-10-15"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/d9dff9b6320e4227301b56c25569589e71e2bce9"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`d9dff9b6`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/d9dff9b6320e4227301b56c25569589e71e2bce9) by Louis Moresi, 2026-10-15: **Fault multigrid: the Moresi-Solomatov convection campaign, the fault sequence, the solver item and the hand-over**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

**A convection run where the fault matters (2026-10-14/15).** The purely viscous state above has no bendable plate and no ridge, so the fault cannot organise plate motion. The campaign was re-anchored on Moresi & Solomatov (GJI 133, 669, 1998): non-dimensionalised on the basal viscosity, $Ra_0 = 10^{7}$, contrast $3\times10^{4}$, Byerlee yield $\tau = 10^{5} + 10^{7} z$ (their mobile-lid reference; the depth gradient at $\tau_1/Ra_0 = 1$ keeps the interior strong, where a tenth of that let the interior yield and run away), internal heating 7 with the base held at $T = 1$, the interior started at 0.8. Implicit SUPG transport, steps capped at $10^{-3}$, eight ranks, 27 to 35 s per step on the base.
![the control](../figures/fault-mg-zg95_control_400.png)
*The control (`conv_ms98`) at step 400: a steady six-cell mobile lid from step 100 on, plateau surface speeds near 80 with sharp reversals over narrow slabs, lid 0.105, a third of it yielding, mid-depth temperature 0.70. Restarting it at equilibrium with the contrast raised to $10^{5}$ and the cohesion to $2\times10^{5}$ gave the sluggish distributed-deformation regime (lid 0.15, mobility 0.2 to 0.4, one broad plate stretching uniformly) with no overturn in 600 steps.*
The fault phase restarts from the control's step-150 checkpoint with the same rheology on the add-on, the trench dipping under the plate on the positive-theta side above the seeded downwelling. Two runs of 300 steps:
![the fault sequence](../figures/fault-mg-zg95_fault_sequence.png)
*`fault_ms98_split`, trench velocity sampled 1.7 degrees into the hanging wall, which goes stationary once the fault takes the slip, so the fault stood still. In order: the fault localises the plate boundary (slip 70 to 90) and leaves a stationary sliver, the overriding plate yielding over 35 degrees; the downwelling becomes one-sided, a slab dipping under the overriding plate, the deformation zone narrowing to 10 degrees and the slip rising to 120; the slab breaks off; the sinking fragment pulls the overriding lid in at 250 to 300, an overturn in the Moresi & Solomatov sense triggered locally by the fault; a ridge opens behind the trench and a steep slab re-forms. The five cells away from the fault never changed. Lid yielding averaged 0.40 against the control's 0.33: the fault added yielding on the overriding side, and only approached the control's value while the subduction wedge was mature.*
![the moving fault](../figures/fault-mg-zg95_move_200.png)
*`fault_ms98_move` (running): the trench follows the overriding plate proper (median surface velocity over a window 0.1 to 0.3 rad beyond the fault), advancing over the subducting plate at 85 to 95. The slab follows the fault at a lag of about 12 degrees and, at this stage, stays vertical and symmetric.*
**What the fault phase cost, and the solver item it exposed.** A cold first step on the faulted add-on took 742 s: 24 nonlinear iterations, and in every Newton-phase solve the pressure (Schur) iteration hit its cap of 200 (42 to 54 in the Picard phase). Picard-only at the same tolerance capped too, from iteration 14, so the cap is not the Newton tangent: it sets in once the nonlinear residual has dropped about a hundredfold, and the base mesh never shows it. Each pressure iteration nests a full velocity multigrid solve, so a capped solve is about 3400 cycles. The working hypotheses are the nested Schur stalling on the inner-solve noise floor once the outer residual is small, or the yielded viscosity on the faulted add-on defeating the $1/\eta$ Schur preconditioner; the probe is one step at two ranks from the checkpoint with the pressure KSP monitored per outer iteration. The runs above use a relative tolerance of $10^{-2}$, Picard-only, which Picard reaches before the cap, and a warm start across the add-on rebuilds (the previous velocity and pressure evaluated onto the new add-on), which halves the step: 25 to 300 s depending on whether the trench moved a rung.
Three parallel-safety defects in the driver came out of the same runs and are the reason the first 8-rank fault run "stuck": a rank-local test deciding whether to write the yield indicator onto the base variable (a collective flush) hung seven ranks in a reduction; a cross-mesh evaluation of the effective-viscosity expression, which holds velocity gradients, cannot be lambdified (evaluate on the owning mesh into a P1 variable and transfer that); the figure's temperature panel was drawn only in serial. The ruling that followed: build parallel-safe infrastructure and then use it, in drivers and examples as much as in the library, since a rank-local shortcut in a script is what users and AI tools copy.
The hand-over note for this campaign is `scripts/sessions/fault_mg/CAMPAIGN.md` on the branch.
- The pressure-cap solver item of the fault phase (above); the dynamic topography sign convention (peaks over the downwellings in the step figures); the trench rule once the moving-fault run has finished.
