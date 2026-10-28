---
title: "Math in fenced math blocks and $...$ inline, so markdown does not eat the backslashes (\\, became a comma)"
date: "2026-10-05"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "benchmarks"
    - "solvers-and-multigrid"
    - "viscoelastic-constitutive-models"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Benchmarks/8f65e54902f2f470aa869931b4bdfeaecec4a80b"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`8f65e549`](https://github.com/underworldcode/underworld3/wiki/Benchmarks/8f65e54902f2f470aa869931b4bdfeaecec4a80b) by lmoresi, 2026-10-05: **Math in fenced math blocks and $`...`$ inline, so markdown does not eat the backslashes (\, became a comma)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Benchmarks

*Left: at Re 200, Wi 0.5 the settled lift amplitude falls with resolution in every scheme, so coarse "nice vortices" are an artefact. Right: FENE-P steady shear against the cubic $f^2(f-1) = 2\mathrm{Wi}^2/L^2$, first order in $\Delta t/\lambda$.*

### Added to Solvers and multigrid

Drucker–Prager in the form the notch model uses, with $p$ the total pressure the solver carries (lithostatic plus dynamic, gauge fixed by the free surface):
$$
\sigma_y = C_{\mathrm{eff}} + p\sin\varphi, \qquad \eta_{pl} = \frac{\sigma_y}{2\dot\varepsilon_{II}}, \qquad \eta = \eta_{\min}\vee\big(\eta_{ve} \wedge \eta_{pl}\big),
$$
where $\wedge$ is the yield branch selection and $\vee$ the viscosity floor, both smoothed as below; a positive residual strength keeps $\sigma_y \ge 0.02\,C$ where $p\sin\varphi$ would take it negative (an exact floor at zero gives $\eta_{pl} = 0$, a singular operator, and was every `DIVERGED_LINEAR_SOLVE` on the gradient-damage fixture). Spiegelman's $C\cos\varphi$ is absorbed into $C_{\mathrm{eff}}$.
**The soft-min substrate** (`yield_mode="softmin"`), with $f = \eta_{ve}/\eta_{pl}$ the overstress ratio ($f = 1$ at yield):
$$
\eta = \frac{\eta_{ve}}{g(f)}, \qquad g = 1 + \tfrac12\!\left(f - 1 + \sqrt{(f-1)^2 + \delta^2}\right) - \text{offset},
$$
the `sqrt` family; `offset` $= \delta/2$ under the `"yield"` anchor (exact at $f = 1$, law $\ge$ the hard Min everywhere, unyielded material stiffened by at most a factor 2 and by ~3% at $\delta = 0.1$), $0$ under `"onset"` (exact as $f \to 0$, law *below* the hard Min at and above yield — a weaker problem than the stated one, which is why it is no longer the default). The power mean $\eta = ((\eta_{ve}^{-s} + \eta_{pl}^{-s})/2)^{-1/s}$, $s = 1/(\delta + 10^{-3})$, is the other family; $\delta$ is not the same parameter in the two. Default since 2026-10-05: `sqrt`, `"yield"`, $\delta = 0.1$.
**Rate strengthening** $\xi$: $\tau_y \to \sigma_y + 2\xi\eta_{bg}\dot\varepsilon_{II}$, i.e. $\eta_{pl} \to \sigma_y/2\dot\varepsilon_{II} + \xi\eta_{bg}$, an additive modulus along the strain-rate direction in every yielded element. $\xi = 1$ is the viscous solution, $\xi \to 0$ the stated law. Without elasticity the plastic-rate (Perzyna) and total-rate (consistency) placements differ only by the factor $(1+\xi)$.
**The tangents.** With $\mathbf F(\mathbf u, p)$ the residual, the frozen (Picard) tangent $J_p$ differentiates the flux with $\eta$ held as a constant atom; the consistent tangent $J_n$ unwraps $\eta(\dot\varepsilon, p)$ and carries $\partial\eta/\partial\nabla\mathbf v$ (the $(\mathbf I - \mathbf n\otimes\mathbf n)$ structure of a yielded element, $\mathbf n = \dot{\boldsymbol\varepsilon}/\dot\varepsilon_{II}$) and, for a pressure-dependent yield, a $\partial\eta/\partial p$ term in the velocity–pressure block. The continuation tangent is
$$
J(\alpha) = J_p + \alpha\,(J_n - J_p), \qquad \alpha = \mathrm{clip}\!\left(\frac{\log_{10}(F_{\mathrm{ref}}/\|F\|) - L_0}{L_1 - L_0},\,0,\,1\right), \quad F_{\mathrm{ref}} = \|F(\mathbf u = 0)\|,
$$
one SNES solve, $\alpha$ set per iteration, monotone except for a back-off when $\|F\|$ grows tenfold above its minimum; $\alpha$ is a `constants[]` atom so the switch costs no recompile. Keying on $F(0)$ rather than the solve's own $F_0$ is what makes warm starts enter the ramp where they belong. The partial tangent `newton_pressure_coupling=False` keeps the Newton velocity block and takes the pressure column from the frozen flux ($J_{vp} = -B^T$) — it is "lag $p$ in $\sigma_y$", quasi-Newton in the pressure sensitivity, and it is not a point on the $\alpha$ line.
- **Picard is an entry requirement, not an accelerator.** From a cold state the consistent tangent is undefined at $\dot\varepsilon = 0$ (the $\sqrt{g}$ guard makes it zero rather than NaN) and the first step needs the frozen operator; after that Newton is the cheaper tangent, and a controller that starts in Picard costs 27 iterations where Newton takes 7. One automatic Picard step on a cold start is the whole of the entry; a warm start takes none.
- **Two linear failures of the consistent tangent far from the solution, both measured with −F(x) at a cold Newton state (notch, 5e24).** (1) The $\partial\eta/\partial p$ column puts $J_{vp}$ 41% off $-B^T$ and the Schur complement $S = J_{pv}A^{-1}J_{vp}$ becomes indefinite (40 of 1968 eigenvalues of $W^{-1}S$ of the wrong sign; 35% non-symmetric); no definite Schur approximation — the production $W$, augmented Lagrangian at any $\gamma$, $\mathrm{diag}(S)$ — can precondition it, the exact Picard-type Schur fails too, and the Picard matrix as a preconditioner fails (0.98/iteration). Only the exact $S$ (2 iterations) or a direct solve works. Dropping the column restores a convergent structure (149 iterations at 0.883). (2) The Newton velocity block of a yielded layer carries a mechanism mode: the element tangent has ~zero modulus along $\mathbf n$, so a block of the layer slides along its yielded neighbours at almost no cost (Rayleigh quotient 1.8e-7 against a smallest diagonal of 4.7e-4; one negative MUMPS pivot). Geometric FMG with every smoother and GAMG stall on it at 0.996–0.999 per cycle; LU solves it. The $\alpha$-blend keeps $(1-\alpha)$ of the Picard modulus along $\mathbf n$, which is why it converges where pure Newton cannot: it is a tangent regularisation. Inside the basin (converged state) neither failure exists — 0 wrong-sign eigenvalues, 0 negative pivots, 13–15 velocity cycles per application — so the full tangent is right there and is cheaper (13 Newton iterations vs 53 partial on 5e24).
- **Augmented Lagrangian in the preconditioner only** does nothing on the indefinite Schur but gives the textbook gain once the structure is standard (149 → 67 → 24 → 12 outer iterations for $\gamma$ = 1, 10, 100 on the partial operator) and the velocity FMG tolerates $A_\gamma$ to $\gamma \approx 10$. Not built; the penalty in the *residual* stays ruled out for DP (it changes the pressure the yield law reads).
- **Approach from above works when the entry is at the onset.** A viscous solve gives, per cell, the cohesion multiple $s = (\tau_{II} - p\sin\varphi)/C$ at which it reaches the surface; from $0.95\,s^*$ down, full Newton converges on every rung of a plain cohesion ladder (5e24: 8 rungs, 235 iterations) and gives n3+yield a viable entry where the blend had none. The entry rung is the cost at every parameter tried (gravity sets $F(0)$), so ladders buy robustness, not a cheaper single solve. Ladders in V (the near-static end is the hardest nonlinear problem) and in the rate-weakening cohesion homotopy (indefinite tangent at large $\alpha$) go the wrong way. $\xi$ is the regularisation the mechanism analysis asks for and works as a ladder down to the floor scale; the hand-off to $\xi = 0$ is the hard step. On a ladder the blend beats Newton-with-fallback 3–4× in cycles; Newton wins only on near-viscous rungs.
- **The pressure gauge.** With a free surface there is no nullspace and the level is physical (top-row $p$ = $2\eta\dot\varepsilon_{yy}$ to 3% rms); a mean-pressure projection there would hand a gauge-fixed $p$ to $\sigma_y(p)$ and move it between iterations. The solver now records the gauge it ran under (`solve_report.config["gauge"]`) and warns when a nullspace projection feeds a pressure-dependent viscosity; a closed box needs the physical level supplied separately.
- **The sparse "sign-capturing" Schur** $J_{pv}\,\mathrm{diag}(A)^{-1}J_{vp}$: no positive diagonal where the exact Schur has 90; the indefiniteness lives in $A^{-1}$'s off-diagonal structure.
- **Yielded fraction as a switch** between tangents (ruled out earlier) and any cheap local test for the Schur sign: the coupling is $O(\sin\varphi)$ in every yielding cell at every state; the sign flip is global. The velocity block's mechanism, by contrast, is element-local (the modulus along $\mathbf n$) and could be a pre-solve check; the Ritz values of the outer Krylov are the free by-product that would say which failure a stall is.

### Added to Viscoelastic Constitutive models

Notation: $\mathbf{L} = \nabla \mathbf{u}$ the velocity gradient, $\mathbf{D} = \tfrac12(\mathbf{L} + \mathbf{L}^T)$ the strain rate, $\boldsymbol{\sigma}$ the total deviatoric stress, $\boldsymbol{\tau}$ the elastic (memory) part of it, $\eta_s$ the solvent viscosity, $\eta_p$ the viscosity of the elastic branch, $\lambda$ its relaxation time, $G = \eta_p/\lambda$ its modulus, $\mathbf{c}$ the conformation (the ensemble-average dyad of the dumbbell end-to-end vector, $\mathbf{I}$ at rest), $d$ the dimension. The upper-convected derivative is
$$
\overset{\nabla}{\mathbf{A}} = \frac{D\mathbf{A}}{Dt} - \mathbf{L}\mathbf{A} - \mathbf{A}\mathbf{L}^T .
$$
The dimensionless groups of the cylinder work are $\mathrm{Re} = \rho U D/(\eta_s + \eta_p)$, $\mathrm{Wi} = \lambda U/D$ and $\beta = \eta_s/(\eta_s + \eta_p)$.
$$
\boldsymbol{\sigma} = \boldsymbol{\tau}, \qquad \boldsymbol{\tau} + \lambda\,\overset{\nabla}{\boldsymbol{\tau}} = 2\eta_p \mathbf{D}.
$$
$$
\boldsymbol{\sigma} = 2\eta_s \mathbf{D} + \boldsymbol{\tau}, \qquad \boldsymbol{\tau} + \lambda\,\overset{\nabla}{\boldsymbol{\tau}} = 2\eta_p \mathbf{D}.
$$
In conformation form, which is what the code integrates, $\boldsymbol{\tau} = G(\mathbf{c} - \mathbf{I})$ and
$$
\frac{D\mathbf{c}}{Dt} = \mathbf{L}\mathbf{c} + \mathbf{c}\mathbf{L}^T - \frac{1}{\lambda}(\mathbf{c} - \mathbf{I}).
$$
The spring is Hookean, so in a steady extension with $\lambda\dot\epsilon > 1/2$ the conformation grows without bound. On the cylinder wake that happens between Wi 1 and 2: the stress fills the wake with structure at the mesh scale on every mesh, and it is the model rather than the scheme.
**Jeffreys element, FENE-P spring.** The spring stiffens as the dumbbell approaches its maximum extension $L$ (Peterlin's closure replaces $\langle f(\mathbf{Q})\mathbf{Q}\mathbf{Q}\rangle$ by $f(\langle\mathbf{Q}\mathbf{Q}\rangle)\langle\mathbf{Q}\mathbf{Q}\rangle$):
$$
f(\mathbf{c}) = \frac{L^2 - d}{L^2 - \mathrm{tr}\,\mathbf{c}}, \qquad \boldsymbol{\tau} = G\,(f\mathbf{c} - \mathbf{I}), \qquad \frac{D\mathbf{c}}{Dt} = \mathbf{L}\mathbf{c} + \mathbf{c}\mathbf{L}^T - \frac{1}{\lambda}(f\mathbf{c} - \mathbf{I}).
$$
The relaxation rate is $f/\lambda$ and the relaxation target is $\mathbf{I}/f$; $\mathrm{tr}\,\mathbf{c} < L^2$ always, so the stress saturates. With $L^2 \to \infty$, $f \to 1$ and the model is Oldroyd-B. The parameter is `Parameters.extensibility` $= L^2$ (dimensionless; 100 on the cylinder, 10 in the tests). The trace of $f\mathbf{c} = \boldsymbol{\tau}/G + \mathbf{I}$ gives $f$ from the stress in closed form,
$$
f = 1 + \frac{\mathrm{tr}\,\boldsymbol{\tau}}{G L^2},
$$
**Steady simple shear** ($\dot\gamma$, $\mathrm{Wi} = \lambda\dot\gamma$), the closed forms the tests use. Oldroyd-B: $\tau_{xy} = \eta_p\dot\gamma$, $N_1 = 2\eta_p\lambda\dot\gamma^2 = 2G\,\mathrm{Wi}^2$. FENE-P in two dimensions: $c_{yy} = 1/f$, $c_{xy} = \mathrm{Wi}/f^2$, $c_{xx} = (1 + 2\mathrm{Wi}^2/f^2)/f$, and the closure gives one cubic for $f$,
$$
f^2 (f - 1) = \frac{2\,\mathrm{Wi}^2}{L^2}, \qquad \tau_{xy} = \frac{\eta_p\dot\gamma}{f}, \qquad N_1 = \frac{2G\,\mathrm{Wi}^2}{f^2}.
$$
At Wi 1, $L^2 = 10$: $f = 1.1510$, $\tau_{xy} = 0.8688\,\eta_p\dot\gamma$, $N_1 = 1.5097\,G$.
**What the code stores and steps.** The history carries $\boldsymbol{\psi} = \log(\boldsymbol{\tau}/G + \mathbf{I})$, which is $\log\mathbf{c}$ for a linear spring and $\log(f\mathbf{c})$ for FENE-P; the exponential of a symmetric record is positive definite, which is what makes the log store survive large Wi. One step of length $\Delta t$ with the exponential integrator at first order, written for the stress with $x = \Delta t\,f^*/\lambda$ and $\alpha = e^{-x}$ ($f^* = 1$ for a linear spring, the lagged factor of the carried record for FENE-P):
$$
\boldsymbol{\tau}^{n+1} = \alpha\,\boldsymbol{\tau}^* + (1-\alpha)\,2\eta_p\mathbf{D}^{n+1} + \alpha\,\Delta t\,f^*\,\mathcal{S}\!\left(G(\mathbf{c}^* - \mathbf{I})\right) + \frac{b^2}{(1-\alpha) f^*}\,\frac{G}{\lambda}\,\mathbf{L}\mathbf{L}^T, \qquad \mathcal{S}(\mathbf{A}) = \mathbf{L}\mathbf{A} + \mathbf{A}\mathbf{L}^T, \quad b = \lambda\left(1 - (1+x)e^{-x}\right).
$$
Here $\boldsymbol{\tau}^*$ and $\mathbf{c}^*$ are the carried (transported) record decoded at the new time level, $\mathcal{S}$ is the stretching source of the objective rate, taken explicitly with the current gradient on the carried strain $G(\mathbf{c}^* - \mathbf{I})$ rather than on the stress (the two differ for FENE-P), and the last term is the positive-definite correction: without it the stretched relaxation target is $(1-\alpha)\mathbf{I} + b\,\mathcal{S}(\mathbf{I})$, which is not a product of two factors; with it the target is $(\sqrt{1-\alpha}\,\mathbf{I} + b\mathbf{L}/\sqrt{1-\alpha})(\cdot)^T$ and stays positive semi-definite. That term is what let the cross-slot bifurcation appear. The $f^*$ on the relaxation rate cancels the $f^*$ on the stress $G f^* \mathbf{c}$ for every source, which is why the source keeps its Oldroyd-B weight $\alpha\,\Delta t$ (times $f^*$) and not $\alpha\,\Delta t/f^*$; the first form of the step had one $1/f$ too many on the stretching source and sat 3% and 13% off the closed form at every $\Delta t$.
*Right: the FENE-P shear box against the cubic, first order in $\Delta t/\lambda$. Left belongs to [Transport histories](../topics/transport-histories.md).*
