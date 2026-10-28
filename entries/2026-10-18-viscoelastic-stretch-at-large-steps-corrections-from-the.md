---
title: "Viscoelastic stretch at large steps: corrections from the adversarial review (Pakdel-McKinley inside the layer, time-scheme cost, tangent at 1/120, SPD scope, conformation-check scope, the refusals, merge order after #800)"
date: "2026-10-18"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "viscoelastic-stretch-at-large-steps"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps/0087e6b3d745cfa55b1a3e2504613f966503f755"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`0087e6b3`](https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps/0087e6b3d745cfa55b1a3e2504613f966503f755) by Louis Moresi, 2026-10-18: **Viscoelastic stretch at large steps: corrections from the adversarial review (Pakdel-McKinley inside the layer, time-scheme cost, tangent at 1/120, SPD scope, conformation-check scope, the refusals, merge order after #800)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Viscoelastic stretch at large steps

| `"tangent"` | each $\mathbf{L}\mathbf{A}\mathbf{L}^T$ by its tangent about the last step's $\mathbf{L}^n$ | matches implicit to $10^{-3}$ while it runs; at $\Delta t = 1/60$ stalls with it (step 52); at $1/120$ (Crank-Nicolson) went unstable at $t = 1.75$, where implicit ran to $2.75$ |
| `preconditioner_flux = "model"` | velocity block of the preconditioning matrix without the stretch terms (SPD for Stokes without yield) | Newton unchanged; inner iterations 22 against 7 at an easy step: at the wall the stretch is most of the operator (the viscous block's largest eigenvalue is a twelfth of the Jacobian's) |
| `"linear"`, backward Euler, $1/60$ | 5.74 | the time scheme: +14.5 % against `"linear"` Crank-Nicolson at the same step |
The step and the time scheme cost about equally (+11 % and +14.5 %); the `"linear"` form costs least (−5 %). The error is not monotone in $\Delta t$ (backward Euler at $1/30$ is closer than at $1/60$), and the drag still alternates in sign on about half the steps with backward Euler, so part of the ringing is not the time scheme. The two forms agree to first order in $\Delta t\,|\mathbf{L}|$: in the geodynamic regime, $\Delta t\,|\mathbf{L}| \ll 1$, they are interchangeable.
- **It may be an elastic instability.** The Pakdel–McKinley parameter $M = \sqrt{(\lambda U/\mathcal{R})(N_1/\sigma_{tn})}$ reaches 24 to 29 within two wall cells (Oldroyd-B, steps 41 and 48; 30 for FENE-P), above the critical values reported for curved-streamline flows (of order 5 to 10). At the sampling point nearest the wall it is 3.6 to 6.7, which is the value we first reported, wrongly, as the peak; further out it is larger still, but there the shear stress in its denominator vanishes and it means nothing. The indefinite Jacobian mode sits where the tension is largest, a prestressed, curved, unresolved sheet. Whether an instability is developing cannot be settled in 2-D on a mesh that does not resolve the layer.
- **The yield criterion must see the full stress invariant.** The stored stress here is almost entirely streamwise normal stress; a limit on resolved shear stress would not release it. `ViscoElasticPlasticFlowModel` yields on the invariant of the effective strain rate, which includes the carried stress and the objective terms, so it should (we have not run a yielding case on the cylinder).
- **Watch the conformation.** `constitutive_model.conformation_min_eigenvalue()` also returns `max`, the largest conformation eigenvalue; for a linear spring, a value much above one says the model is being used at elastic strains of order one, and the results are outside the regime it was chosen for. It reads the history's own points and is not available for the Eulerian SUPG history, where the stored tensor has to be sampled directly (as the wall report does).
- `ViscoElasticPlasticFlowModel(stretch_in_momentum="implicit" | "linear" | "tangent")`, settable between steps; the form each solve ran is in its solve report. Non-default forms need the deformation step (either integrator) and are refused elsewhere; `NavierStokesSLCN` / `NavierStokesSwarm` build their flux from the history and refuse them.
- `solver.preconditioner_flux = "jacobian" | "model"` on the saddle-point solvers, with `preconditioner_flux` on the constitutive models (the flux itself by default; without the objective-rate terms for the viscoelastic model). Refused with rotated free-slip, on the semi-Lagrangian Navier-Stokes solvers, and with a smooth Jacobian surrogate; the adjoint preconditions with the transposed Jacobian. The preconditioner block is symmetric positive-definite only for Stokes without a yield stress.
- Lands after #800 (FENE-P, the same constitutive code); the review record is `docs/reviews/2026-10/ve-stretch-split-adversarial-review.md`.
