---
title: "Viscoelastic stretch at large steps: the wall layer measured (extension at the stagnation point, tension on the shoulders, unresolved), FENE-P capped at the same place and step, the consequences for yielding"
date: "2026-10-17"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "viscoelastic-stretch-at-large-steps"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps/932cb8f39c81c56e35caba731842feb40fa527cf"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`932cb8f3`](https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps/932cb8f39c81c56e35caba731842feb40fa527cf) by Louis Moresi, 2026-10-17: **Viscoelastic stretch at large steps: the wall layer measured (extension at the stagnation point, tension on the shoulders, unresolved), FENE-P capped at the same place and step, the consequences for yielding**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Viscoelastic stretch at large steps

## What the wall layer is
Sampled on rays normal to the cylinder at 15° intervals (driver flag `-uw_wall_report`), wall frame ($\mathbf{n}$ outward, $\mathbf{t}$ along the wall), angle measured from the downstream axis so that 180° is the front stagnation point; stresses in units of $\rho U^2$, tension positive; $\lambda = 0.05$.
| angle | $\dot\gamma$ | $\lambda\dot\gamma$ | tr c | $N_1/\lvert\sigma_{tn}\rvert$ | pressure | total $\sigma_1$ | total $\sigma_2$ |
|---|---|---|---|---|---|---|---|
| 180° (front stagnation) | 3 | 0.1 | 270 | 1200 | 2.35 | 0.35 | −2.39 |
| 165° | 281 | 14 | 780 | 264 | 2.16 | 5.6 | −2.18 |
| 150° (upstream shoulder) | 309 | 15 | 3500 | 17 | 1.81 | 33.5 | −1.81 |
| 135° | 188 | 9 | 3300 | 66 | 0.93 | 32.2 | −0.94 |
| 90° (top) | 65 | 3 | 44 | 12 | −0.38 | 0.81 | 0.37 |
| 0°–60° (downstream) | < 25 | < 1.2 | < 6 | < 3 | ≈ −0.5 | ≈ 0.6 | ≈ 0.5 |
*Oldroyd-B at step 41 (t 0.68); step 48, just before the failing step, is the same to a few per cent (tr c 3620, $N_1$ 36).*
- **It starts in extension.** Along the upstream stagnation streamline $\lambda\dot\varepsilon$ reaches 2.1, four times the value (½) above which the Oldroyd-B extensional stress is unbounded. The front face stretches the material along the wall with no shear at all (tr c 270 at the stagnation point).
- **Shear carries and amplifies it.** On the upstream shoulders the local Weissenberg number is 15 and tr c 3500: the Hookean dumbbell is stretched forty times its rest length. What accumulates is the streamwise normal stress, not the shear stress: $N_1$ is 17 to 1200 times $\sigma_{tn}$, so $\tau_{II} \approx N_1/2$.
- **It is a tension.** In total stress the shoulders carry a principal tension of 32 along the wall, 15 to 30 times the local pressure, against a mild compression normal to it. (In incompressible flow the pressure level is a gauge set at the outflow: an ambient pressure above $32\rho U^2$ would make the layer compressive.)
- **It is unresolved.** The half-width of the tension layer is 0.21 wall cells.
- **It is not an elastic instability.** The Pakdel–McKinley parameter $M^2 = (\lambda U/\mathcal{R})(N_1/\sigma_{tn})$ peaks at 3.6, below the usual critical values. The indefinite Jacobian mode sits where the tension is largest: a geometric-stiffness term from a prestressed, curved, unresolved sheet.
## Finite extensibility does not remove it
FENE-P with $L^2 = 100$ (branch `feature/forward-from-nodes`), the same mesh, step and implicit stretch, from $t = 0$:
![The wall layer, Oldroyd-B against FENE-P](../figures/ve-wall-layer.png)
*Conformation trace and first normal stress difference along the wall at step 48 ($t = 0.80$), nearest sampling distance. The dashed line is $L^2$.*
The cap does what it is for: tr c on the rays stays below 90, the wall tension is nine times smaller ($N_1$ 4 against 35) and the layer twice as wide (0.62 wall cells), and the drag is 3.45 against 5.2. But the largest nodal conformation reaches the cap, tr c 99.95 at the upstream shoulder at step 48, where the FENE-P spring factor $(L^2 - d)/(L^2 - \mathrm{tr}\,c)$ diverges (54 on the record), and step 49 hangs, as the Oldroyd-B run does. Bounding the spring moves the singular behaviour from unbounded stretch to a diverging spring stiffness at the same place and the same step. The extension rate is unchanged ($\lambda\dot\varepsilon = 2.2$): the flow imposes the deformation, and at this resolution no spring can absorb it without its stiffness entering the tangent.
## For our own problems
This regime is a polymer one, outside rock deformation: elastic strains of order ten, a layer narrower than a cell. Rock stores elastic strain of order $10^{-3}$ before it yields, so the same flow in a geodynamic model is limited by yielding long before anything like this. Two consequences for how we set up viscoelastic-plastic models:
- **The yield criterion must see the full stress invariant.** The stored stress here is almost entirely streamwise normal stress; a limit on resolved shear stress would not release it. `ViscoElasticPlasticFlowModel` yields on the invariant of the effective strain rate, which includes the carried stress and the objective terms, so it does.
- **Under lithostatic pressure the layer is compressive in total stress**, and the release is deviatoric (von Mises / Drucker–Prager); a tension cut-off matters only where the total stress can actually be tensile (near-surface, or with fluid pressure).
- **Watch the conformation.** `constitutive_model.conformation_min_eigenvalue()` also returns `max`, the largest conformation eigenvalue; for a linear spring, a value much above one says the model is being used at elastic strains of order one, and the results are outside the regime it was chosen for.
