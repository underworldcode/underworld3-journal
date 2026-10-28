---
title: "Solvers and multigrid"
options:
  kind: "topic"
  migrated_from: "https://github.com/underworldcode/underworld3/wiki/Solvers-and-multigrid"
  wiki_created: "2026-10-05"
  wiki_last_edited: "2026-10-16"
---

```{note}
Migrated from the wiki page [Solvers-and-multigrid](https://github.com/underworldcode/underworld3/wiki/Solvers-and-multigrid) on 2026-10-27 as this topic page's starting text (written 2026-10-05 to 2026-10-16). The dated entries at the foot are the record; this text is trimmed as its content moves into guides, subsystem pages and entries.
```


What we understand about making the nonlinear Stokes and Navier–Stokes solves converge, and how they fail. The recipes for the viscoplastic cases are skills in the repository (`nonlinear-solver`, `plasticity-solvers`); the campaign that established most of this is [Spiegelman notch campaign 2026](../campaigns/spiegelman-notch-campaign-2026.md); this page keeps the moving parts.

## Standing rules

Full multigrid always, with three or four levels: a coarse gmsh base and `refinement=2` with a smoothing callback is the happy medium for graded meshes. The consistent Newton tangent is the default (since 2026-10-05, with one automatic Picard step on a cold start); Picard throughout is the opt-in, by name. The yield law is smooth by default (soft-min, anchored at the yield point); the exact Min and any hard Max are explicit choices. A positive residual strength under the tension floor, never zero. No pressure nullspace on a domain with an open boundary. Krylov restart at least 100 on the outer and the velocity solve. Test a linear solver with −F(x), never with a random solution (it probes only the stiff modes) or a random right-hand side (noise modes; stalls even on a Picard block). Test a tangent with a central-difference h-sweep, never one fixed-h comparison. Count velocity multigrid cycles and Krylov iterations, not wall clock.

## The equations

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

## What we have seen

- **Picard is an entry requirement, not an accelerator.** From a cold state the consistent tangent is undefined at $\dot\varepsilon = 0$ (the $\sqrt{g}$ guard makes it zero rather than NaN) and the first step needs the frozen operator; after that Newton is the cheaper tangent, and a controller that starts in Picard costs 27 iterations where Newton takes 7. One automatic Picard step on a cold start is the whole of the entry; a warm start takes none.
- **Two linear failures of the consistent tangent far from the solution, both measured with −F(x) at a cold Newton state (notch, 5e24).** (1) The $\partial\eta/\partial p$ column puts $J_{vp}$ 41% off $-B^T$ and the Schur complement $S = J_{pv}A^{-1}J_{vp}$ becomes indefinite (40 of 1968 eigenvalues of $W^{-1}S$ of the wrong sign; 35% non-symmetric); no definite Schur approximation — the production $W$, augmented Lagrangian at any $\gamma$, $\mathrm{diag}(S)$ — can precondition it, the exact Picard-type Schur fails too, and the Picard matrix as a preconditioner fails (0.98/iteration). Only the exact $S$ (2 iterations) or a direct solve works. Dropping the column restores a convergent structure (149 iterations at 0.883). (2) The Newton velocity block of a yielded layer carries a mechanism mode: the element tangent has ~zero modulus along $\mathbf n$, so a block of the layer slides along its yielded neighbours at almost no cost (Rayleigh quotient 1.8e-7 against a smallest diagonal of 4.7e-4; one negative MUMPS pivot). Geometric FMG with every smoother and GAMG stall on it at 0.996–0.999 per cycle; LU solves it. The $\alpha$-blend keeps $(1-\alpha)$ of the Picard modulus along $\mathbf n$, which is why it converges where pure Newton cannot: it is a tangent regularisation. Inside the basin (converged state) neither failure exists — 0 wrong-sign eigenvalues, 0 negative pivots, 13–15 velocity cycles per application — so the full tangent is right there and is cheaper (13 Newton iterations vs 53 partial on 5e24).
- **FGMRES at restart 30 stalls completely on a mechanism mode; restart 100 converges.** Same preconditioner, same exact velocity solve: outer 1.000 vs 188 iterations; velocity FMG on the hard right-hand side 3000 cycles unfinished vs 155. The pattern "restart + 88" says the first Krylov cycle builds the mode and the rest is a Picard-like count. LGMRES, DGMRES and GCR at restart 30 do not substitute; no PETSc KSP picks its restart. UW did not set the restart; PETSc's default is 30.
- **Augmented Lagrangian in the preconditioner only** does nothing on the indefinite Schur but gives the textbook gain once the structure is standard (149 → 67 → 24 → 12 outer iterations for $\gamma$ = 1, 10, 100 on the partial operator) and the velocity FMG tolerates $A_\gamma$ to $\gamma \approx 10$. Not built; the penalty in the *residual* stays ruled out for DP (it changes the pressure the yield law reads).
- **Approach from above works when the entry is at the onset.** A viscous solve gives, per cell, the cohesion multiple $s = (\tau_{II} - p\sin\varphi)/C$ at which it reaches the surface; from $0.95\,s^*$ down, full Newton converges on every rung of a plain cohesion ladder (5e24: 8 rungs, 235 iterations) and gives n3+yield a viable entry where the blend had none. The entry rung is the cost at every parameter tried (gravity sets $F(0)$), so ladders buy robustness, not a cheaper single solve. Ladders in V (the near-static end is the hardest nonlinear problem) and in the rate-weakening cohesion homotopy (indefinite tangent at large $\alpha$) go the wrong way. $\xi$ is the regularisation the mechanism analysis asks for and works as a ladder down to the floor scale; the hand-off to $\xi = 0$ is the hard step. On a ladder the blend beats Newton-with-fallback 3–4× in cycles; Newton wins only on near-viscous rungs.
- **The pressure gauge.** With a free surface there is no nullspace and the level is physical (top-row $p$ = $2\eta\dot\varepsilon_{yy}$ to 3% rms); a mean-pressure projection there would hand a gauge-fixed $p$ to $\sigma_y(p)$ and move it between iterations. The solver now records the gauge it ran under (`solve_report.config["gauge"]`) and warns when a nullspace projection feeds a pressure-dependent viscosity; a closed box needs the physical level supplied separately.
- **SNES-FAS equals Newton, give or take.** It runs on the notch once each coarse level has an auxiliary vector (the law reads mesh variables through it; without one the coarse residual is NaN), with the production fieldsplit/FMG as the level solve; warm, 2 V-cycles against Newton's 10 iterations at parity in Krylov work; cold, its coarse solve fails exactly as Newton does. Ruling: not a magic bullet; build the infrastructure only if another reason appears.
- **A stall that looks like a hang** is usually a coefficient the smoother cannot handle. The FENE-P cylinder runs spent their full 300 Krylov iterations per Newton step and the Newton loop ran to its maximum once the wall layer alternated between a saturated and a free spring, a coefficient contrast of 5 within one cell layer. The guard read 15 minutes without a force write as a hang. The cause was in the constitutive record (see [Constitutive models](https://github.com/underworldcode/underworld3/wiki/Constitutive-models)), not in the solver.

## What did not work, and why

- **The exact hard Min and Max, re-litigated.** Ruled out 2026-09-18 (the kink breaks the consistent tangent at the corner, sympy's fuzzy comparisons recurse, a zero tension floor is singular); the notch driver carried `smooth_max(…, 0, 0)` through the campaign anyway and a session proposed testing the corner. A ruling is applied, not re-tested; now the model default.
- **Nonlinear remedies for a linear failure.** Three weeks of line searches (bt kills Picard, l2 accepts uphill steps, nleqerr, cp, Anderson, NGMRES, damping, Eisenstat–Walker caps) against a solve that was failing inside Newton's linear solve. Diagnose the linear solve with −F(x) before touching the nonlinear loop.
- **Random-solution and random-RHS tests of the velocity multigrid.** The first showed 0.909/cycle on an operator the fieldsplit could not solve at all; the second gave 1.000 even on the Picard block. Neither is the Newton right-hand side.
- **A fixed-h `-snes_test_jacobian`** on a power-law rheology reported 1.5e-3 and looked like a tangent error; the central-difference h-sweep converged as h² to 1e-6 in every case. Truncation error, not the Jacobian.
- **The sparse "sign-capturing" Schur** $J_{pv}\,\mathrm{diag}(A)^{-1}J_{vp}$: no positive diagonal where the exact Schur has 90; the indefiniteness lives in $A^{-1}$'s off-diagonal structure.
- **Picard-matrix or blended-matrix preconditioners for the Newton operator** (0.977–0.988): the Newton and Picard velocity blocks differ by 51% at the cold state, and Krylov cannot deflate band-segment modes one at a time.
- **Smoother and hierarchy changes against the mechanism mode** (SOR ×4/×8, Richardson, Chebyshev, deeper hierarchies, GAMG, three settings): 0.99 per cycle throughout. The mode needs Krylov space, not a better smoother.
- **Yielded fraction as a switch** between tangents (ruled out earlier) and any cheap local test for the Schur sign: the coupling is $O(\sin\varphi)$ in every yielding cell at every state; the sign flip is global. The velocity block's mechanism, by contrast, is element-local (the modulus along $\mathbf n$) and could be a pre-solve check; the Ritz values of the outer Krylov are the free by-product that would say which failure a stall is.
- **Nested iteration (coarse solve, interpolate, fine Newton).** Bands are one cell wide and mesh-dependent, so the coarse solution is far in residual (F₀ 0.32 vs 0.42 cold); fine Newton from it fails, the fine blend saves 30%, the coarse solve cost more than that. The same information is all a FAS coarse correction can carry.
- **Ladders in V and in the rate-weakening cohesion homotopy** (100k and 604k cycles against 20k): see above.
- **Nitsche free-slip with γ = 10** was a cliff, 100 times worse than 12.5, because h had been redefined under it. Rotated strong free-slip is preferred and needs no calibration.
- **Preconditioning an indefinite viscoelastic velocity block** (confined cylinder, 2026-10): a stretch-free SPD preconditioning matrix tripled the inner iterations, GMRES + ASM smoothing stalled at the same step; the failure was the Newton problem. See [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md).
- **Running 16 ranks on the 12-core laptop** froze the machine for its owner. All Claude jobs together stay within 8 cores; count ranks before every launch.

## Open

- A Krylov stagnation test in `solver_health` (contraction-based) in place of the blunt outer cap, with the Ritz values recorded so a stall carries its cause.
- Defaults still to set: restart 100 on the outer and velocity KSP; a viscosity-floor and residual-strength default tied to the model's own scales; `newton_pressure_coupling` on the approach.
- The onset ladder and blend-on-failure as a solver-level entry (they are driver code today).
- A faster guard: treat a Newton divergence as a failure and stop within one step rather than waiting for the hang limit.

## History

- 2026-10-05 — created.
- 2026-10-05 — the notch campaign's solver findings added: equations (yield law, soft-min substrate, tangents), the two linear failure modes, the restart, AL in the PC, the ladders, the gauge, FAS; "What did not work" extended; the new defaults recorded.
- 2026-10-16 — the viscoelastic velocity block at large steps added to "What did not work" (preconditioning cannot fix it), with a link to its topic page.

<!-- BEGIN ENTRIES (generated by scripts/build_index.py; do not edit) -->

## Entries

- 2026-10-29 · [A per-level wall rotation cuts a rotated free-slip custom-FMG solve on an adapted annulus from 18 serial and 197 parallel velocity iterations to 3 and 4](../entries/2026-10-29-per-level-wall-rotation-cuts-rotated-freeslip-fmg-iterations-on-an-adapted-annulus.md) · measurement
- 2026-10-29 · [A datum-only cold start on the rotated path sets its convergence reference from the lifted iterate and takes one increment more than it needs](../entries/2026-10-29-datum-only-cold-start-reference-on-the-rotated-path-costs-one-increment.md) · finding
- 2026-10-28 · [The fault-split integration head reproduces UWTN 2026-022's numbers; the suites pass but for two failures that predate it](../entries/2026-10-28-fault-split-integration-head-reproduces-uwtn-2026-022.md) · measurement
- 2026-10-28 · [Coarse solve on the rotated path: handle the null space, leave the coarse level to PETSc's defaults; MUMPS is not the default](../entries/2026-10-28-coarse-solve-null-space-first-petsc-defaults-not-mumps.md) · decision
- 2026-10-16 · [Dead end: Preconditioning an indefinite viscoelastic velocity block](../entries/2026-10-16-dead-end-preconditioning-an-indefinite-viscoelastic.md) · dead-end
- 2026-10-05 · [Working notes: topic pages (constitutive models, transport histories, projection, solvers, benchmarks), the cylinder campaign, how we plan](../entries/2026-10-05-working-notes-topic-pages-constitutive-models-transport.md) · finding
- 2026-10-05 · [Math in fenced math blocks and $...$ inline, so markdown does not eat the backslashes (\, became a comma)](../entries/2026-10-05-math-in-fenced-math-blocks-and-inline-so-markdown-does-not-eat.md) · finding
- 2026-10-05 · [Dead end: Yielded fraction as a switch](../entries/2026-10-05-dead-end-yielded-fraction-as-a-switch.md) · dead-end
- 2026-10-05 · [Dead end: The sparse "sign-capturing" Schur](../entries/2026-10-05-dead-end-the-sparse-sign-capturing-schur.md) · dead-end
- 2026-10-05 · [Dead end: The exact hard Min and Max, re-litigated](../entries/2026-10-05-dead-end-the-exact-hard-min-and-max-re-litigated.md) · dead-end
- 2026-10-05 · [Dead end: Smoother and hierarchy changes against the mechanism mode](../entries/2026-10-05-dead-end-smoother-and-hierarchy-changes-against-the.md) · dead-end
- 2026-10-05 · [Dead end: Running 16 ranks on the 12-core laptop](../entries/2026-10-05-dead-end-running-16-ranks-on-the-12-core-laptop.md) · dead-end
- 2026-10-05 · [Dead end: Random-solution and random-RHS tests of the velocity multigrid](../entries/2026-10-05-dead-end-random-solution-and-random-rhs-tests-of-the.md) · dead-end
- 2026-10-05 · [Dead end: Picard-matrix or blended-matrix preconditioners for the Newton operator](../entries/2026-10-05-dead-end-picard-matrix-or-blended-matrix-preconditioners.md) · dead-end
- 2026-10-05 · [Dead end: Nonlinear remedies for a linear failure](../entries/2026-10-05-dead-end-nonlinear-remedies-for-a-linear-failure.md) · dead-end
- 2026-10-05 · [Dead end: Nitsche free-slip with γ = 10](../entries/2026-10-05-dead-end-nitsche-free-slip-with-10.md) · dead-end
- 2026-10-05 · [Dead end: Nested iteration (coarse solve, interpolate, fine Newton)](../entries/2026-10-05-dead-end-nested-iteration-coarse-solve-interpolate-fine.md) · dead-end
- 2026-10-05 · [Dead end: Ladders in V and in the rate-weakening cohesion homotopy](../entries/2026-10-05-dead-end-ladders-in-v-and-in-the-rate-weakening-cohesion.md) · dead-end
- 2026-10-05 · [Dead end: A fixed-h `-snes_test_jacobian`](../entries/2026-10-05-dead-end-a-fixed-h-snes-test-jacobian.md) · dead-end

<!-- END ENTRIES -->
