---
title: "Constitutive models"
options:
  kind: "topic"
  migrated_from: "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-Constitutive-models"
  wiki_created: "2026-10-05"
  wiki_last_edited: "2026-10-16"
---

```{note}
Migrated from the wiki page [Viscoelastic-Constitutive-models](https://github.com/underworldcode/underworld3/wiki/Viscoelastic-Constitutive-models) on 2026-10-27 as this topic page's starting text (written 2026-10-05 to 2026-10-16). The dated entries at the foot are the record; this text is trimmed as its content moves into guides, subsystem pages and entries.
```


What we understand about the viscoelastic constitutive models and their time integration. Usage: `docs/developer/subsystems/stress-transport.md`. Argument: [Discussion #815](https://github.com/underworldcode/underworld3/discussions/815).

## The library

A model is named by three independent choices on `ViscoElasticPlasticFlowModel`: the **element** (maxwell, or jeffreys with a parallel solvent dashpot), the **relaxation law** (linear, or FENE-P with extensibility L²) and the **objective rate**. UCM, Oldroyd-B and FENE-P are three points in that space, and a Burgers element would be a second history. We treat this as a library of methods rather than one scheme, as a code carries several turbulence models, and we use domain-neutral names because the same machinery describes transient mantle rheology.

The stress is stored as the logarithm of a conformation and stepped with an exponential (ETD) integrator at first order; the positive-definite update (the `deformation` convected step) adds the b² L Lᵀ term that makes the stretched target a product of two factors, and the cross-slot bifurcation appears only with it. Taken with the new velocity gradient, that step puts the stored stress into the momentum tangent; at a wall with $\Delta t\,|\boldsymbol{\sigma}^*|/\eta \sim 1$ Newton stalls, and `stretch_in_momentum` chooses how much of the stretch the momentum sees ([Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md)). For FENE-P the step is taken on the conformation at the lagged rate f*/λ, with f* carried as a nodal field so the matrix exponential of the record does not enter the compiled flux twice (inlined, it made the C-source generation take 85 s per step).

## The equations

Notation: $\mathbf{L} = \nabla \mathbf{u}$ the velocity gradient, $\mathbf{D} = \tfrac12(\mathbf{L} + \mathbf{L}^T)$ the strain rate, $\boldsymbol{\sigma}$ the total deviatoric stress, $\boldsymbol{\tau}$ the elastic (memory) part of it, $\eta_s$ the solvent viscosity, $\eta_p$ the viscosity of the elastic branch, $\lambda$ its relaxation time, $G = \eta_p/\lambda$ its modulus, $\mathbf{c}$ the conformation (the ensemble-average dyad of the dumbbell end-to-end vector, $\mathbf{I}$ at rest), $d$ the dimension. The upper-convected derivative is


$$
\overset{\nabla}{\mathbf{A}} = \frac{D\mathbf{A}}{Dt} - \mathbf{L}\mathbf{A} - \mathbf{A}\mathbf{L}^T .
$$


The dimensionless groups of the cylinder work are $\mathrm{Re} = \rho U D/(\eta_s + \eta_p)$, $\mathrm{Wi} = \lambda U/D$ and $\beta = \eta_s/(\eta_s + \eta_p)$.

**Maxwell element, linear spring (UCM).** No solvent branch; the whole stress relaxes:


$$
\boldsymbol{\sigma} = \boldsymbol{\tau}, \qquad \boldsymbol{\tau} + \lambda\,\overset{\nabla}{\boldsymbol{\tau}} = 2\eta_p \mathbf{D}.
$$


**Jeffreys element, linear spring (Oldroyd-B).** A solvent dashpot in parallel:


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


which is what the log(f c) record below relies on.

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

![FENE-P steady shear convergence and the Re 200 resolution collapse](../figures/resolution_and_fene_convergence.png)

*Right: the FENE-P shear box against the cubic, first order in $\Delta t/\lambda$. Left belongs to [Transport histories](../topics/transport-histories.md).*

## FENE-P: the record is log(f c)

The record for FENE-P is log(σ/G + I), the same record Oldroyd-B keeps, which for FENE-P is log(f c) rather than log c. The conformation is recovered through the trace, f* = 1 + (tr e^ψ − d)/L², c* = e^ψ/f*. Every SPD record then decodes to an admissible conformation, whatever the projection that commits it did. The relaxation rate, the strain source and the deformation term read the lagged f*; the stress decode has no lag. Against the closed-form steady shear the scheme is first order in dt/λ with errors that halve cleanly (+0.0068, +0.0034, +0.0018 in shear stress at dt 0.1, 0.05, 0.025).

Two derivation traps, both found by the shear-box test: the stretching source acts on G(c − I), not on σ (they differ for FENE-P), and the f* on the rate cancels the f* on the stress for every source, so the source weights keep their Oldroyd-B form.

## What did not work, and why

- **Storing log c for FENE-P.** The conformation is bounded by L²; the nodal Galerkin projection that commits the record is not. At a cylinder wall, where log c jumps by 4 across one cell, the projection overshot by a factor 1.5 in c and committed a record with trace 105 of L² 100 from a stress whose own conformation had 70. The spring factor hit its floor, the wall layer alternated between saturated and free, and the velocity multigrid ground to the guard's hang limit. Lesson: a bounded variable is not the one to project.
- **Our first two diagnoses were wrong.** We blamed saturation (the snapshots said the spring factor was 4.65 against a floor of 100) and then the lagged rate, and encoded the record with the exact factor of the stress, f = 1 + tr σ/(G L²). That made it worse: the stress a step produces is not a FENE-P stress on 50 to 80 wall nodes (its trace fell to −11 where −2 is the physical minimum), so f went toward zero and amplified the conformation 400-fold in one step. A floor on that f left the real cause in place. The per-step diagnostic that printed the record's trace at the nodes against the stress's own closed-form trace is what settled it, after three attempts.
- **Naming the FENE-P fields by `id(self)`** gave different names on different ranks and deadlocked the first snapshot in parallel. Names come from a counter now.
- **Rewiring the smoothing expression unconditionally** forced a C-source regeneration every step for every history commit; comparing the value first cut the Oldroyd-B shear-box step from 7.5 to 1.2 s.
- **Infinite extensibility** gave 0/0 in the spring factor; it is refused, and L² at or below the dimension is refused too (the trace decode would divide by zero).

## Open

Second order for the positive-definite path (the second-order schemes combine levels with negative weights, which does not preserve positivity). A Burgers element as a second history. FENE-P at Re 100 against Richter et al. 2010 as a trend comparison.

## History

- 2026-10-05 — created from the FENE-P work on PR #800; Louis renamed it; the equations for each model and the step were added with the convergence figure.
- 2026-10-16 — the deformation step's cost in the momentum tangent at large steps, and `stretch_in_momentum`, linked to [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md).

<!-- BEGIN ENTRIES (generated by scripts/build_index.py; do not edit) -->

## Entries

- 2026-10-05 · [Updated Constitutive models (markdown)](../entries/2026-10-05-updated-constitutive-models-markdown.md) · finding
- 2026-10-05 · [Math in fenced math blocks and $...$ inline, so markdown does not eat the backslashes (\, became a comma)](../entries/2026-10-05-math-in-fenced-math-blocks-and-inline-so-markdown-does-not-eat.md) · finding
- 2026-10-05 · [Equations for each VE model and the step; figures: meshes, frames, force traces, validation, convergence](../entries/2026-10-05-equations-for-each-ve-model-and-the-step-figures-meshes-frames.md) · finding
- 2026-10-05 · [Dead end: Storing log c for FENE-P](../entries/2026-10-05-dead-end-storing-log-c-for-fene-p.md) · dead-end
- 2026-10-05 · [Dead end: Rewiring the smoothing expression unconditionally](../entries/2026-10-05-dead-end-rewiring-the-smoothing-expression.md) · dead-end
- 2026-10-05 · [Dead end: Our first two diagnoses were wrong](../entries/2026-10-05-dead-end-our-first-two-diagnoses-were-wrong.md) · dead-end
- 2026-10-05 · [Dead end: Naming the FENE-P fields by `id(self)`](../entries/2026-10-05-dead-end-naming-the-fene-p-fields-by-id-self.md) · dead-end
- 2026-10-05 · [Dead end: Infinite extensibility](../entries/2026-10-05-dead-end-infinite-extensibility.md) · dead-end

<!-- END ENTRIES -->
