---
title: "Shear-band length scales: re-planned around the formulations and examples"
date: "2026-10-09"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/81b2111bdbd5b0c2e66742ad761451b50880be89"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`81b2111b`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/81b2111bdbd5b0c2e66742ad761451b50880be89) by lmoresi, 2026-10-09: **Shear-band length scales: re-planned around the formulations and examples**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

# Shear-band length scales
Drucker–Prager plasticity has no length scale, so on the [Spiegelman notch benchmark](../benchmarks/spiegelman-notch-benchmark.md) the shear bands narrow with every mesh refinement and Newton eventually fails. We give the band a length of its own by adding a field to the continuum, solved in the same Newton system as the flow. Two formulations are implemented:
- the **micromorphic** (gradient-plasticity) model, which we use as the default;
- a **2-D Cosserat** continuum.
On the notch both converge at every refinement with no rate strengthening. The micromorphic band width is unchanged from refinement 3 to refinement 5 ($h_{\min}$ = 11 m).
Code: branch `feature/shear-band-length-scale`. Drivers, raw numbers and the full run log: `notch_length_scale/` in [uw3-campaigns](https://github.com/lmoresi/uw3-campaigns) (`REPORT.md`).
## Formulations
### Coupled fields in the Stokes solver
`stokes.add_coupled_field(field, F0, F1=None, momentum_flux=None)` adds a scalar or vector `MeshVariable` $c$ to the Stokes system as an extra DM field, with its own weak form
\int_\Omega \left( F_0\,\psi + \mathbf{F}_1 \cdot \nabla\psi \right) \mathrm{d}\Omega = 0 \qquad \forall \psi .
$F_0$ and $\mathbf F_1$ may depend on $\mathbf u$, $p$, $c$ and their gradients. `momentum_flux` is a stress added to the momentum flux. `add_coupled_dirichlet_bc(value, boundary, field)` fixes $c$ on a boundary; without it, $c$ has the natural condition $\mathbf F_1\cdot\mathbf n = 0$.
Every Jacobian block between $c$ and $(\mathbf u, p)$ is derived symbolically, so Newton sees the full coupling. Ordinary Stokes solves are unaffected; their generated C is byte-identical. Tests: `tests/test_1070_stokes_coupled_fields.py`.
### Micromorphic plasticity (the default)
A scalar field $\chi$, with the units of a strain rate, is tied to the strain-rate invariant $e = \dot\varepsilon_{II}$ by two terms added to the dissipation:
\Psi_\chi = \frac{H}{2}\,(e - \chi)^2 + \frac{A}{2}\,|\nabla\chi|^2, \qquad A = H\,\ell^2 .
Stationarity in $\chi$ makes $\chi$ the strain rate smoothed over the length $\ell$:
\chi - \ell^2\nabla^2\chi = m\,e ,
where $m$ masks the plastic layer, so a viscous inclusion does not drive $\chi$. Stationarity in $\mathbf u$ shifts the yield stress by $H(e - \chi) = -A\nabla^2\chi$:
\sigma_y = \mathrm{smoothmax}\!\left( C + p\sin\phi + m\,H\,(e - \chi),\; s_{\min} \right).
Where deformation is concentrated more sharply than $\ell$, $e > \chi$ and the material is stronger; on the flanks of a band it is weaker. Strain spreads until it varies over about $\ell$, and where it already does, $\chi \approx e$ and the law is plain Drucker–Prager. For a perturbation of wavenumber $k$ the shift is
\hat s = H\,\frac{\ell^2k^2}{1 + \ell^2k^2}\;\hat e ,
a rate strengthening of modulus $H$ that acts only on modes shorter than $\ell$. Rate strengthening $\xi$ acts at every wavelength and so sets no length.
Parameters:
- $\ell$, the length;
- $H = \beta\,\eta_{bg}$, the modulus. It must be comparable to the yielded viscosity $\tau_y/\dot\varepsilon_{\mathrm{band}}$: on the notch $\beta \ge 0.06$–0.08.
```python
chi = uw.discretisation.MeshVariable("chi", mesh, 1, degree=1, units="1/s")
H = uw.expression(r"H_{\chi}", uw.quantity(0.1 * eta_bg, "Pa*s"), "micromorphic modulus")
ell = uw.expression(r"\ell", uw.quantity(1.0, "km"), "micromorphic length")
e = stokes.Unknowns.Einv2           # strain-rate invariant
m = material.sym[0]                 # 1 in the plastic layer, 0 elsewhere
stokes.add_coupled_field(
    chi,
    F0=H * (chi.sym[0] - m * e),
    F1=H * ell**2 * chi.sym.jacobian(mesh.CoordinateSystem.N),
)
s_min = 0.02 * C
stokes.constitutive_model.Parameters.yield_stress = uw.maths.smooth_max(
    C + sin_phi * p.sym[0] + m * H * (e - chi.sym[0]), s_min, s_min)
```
### 2-D Cosserat continuum
A micro-rotation rate $\omega$ (a scalar in 2-D) relative to the continuum spin $W = \tfrac12(\partial_x u_y - \partial_y u_x)$ adds a skew stress to the momentum balance and has its own moment balance:
\boldsymbol\sigma \to \boldsymbol\sigma + 2\eta_c\,(W - \omega)\,\mathbf E,
\qquad \mathbf E = \begin{pmatrix}0&-1\\1&0\end{pmatrix},
-\nabla\cdot\mathbf{m} + 4\eta_c\,(\omega - W) = 0,
\qquad \mathbf{m} = 2\,\eta_{\mathrm{eff}}\,\ell^2\,\nabla\omega .
The yield law sees the generalised invariant $e_{\mathrm{gen}}^2 = \dot\varepsilon_{II}^2 + \tfrac12\ell^2|\nabla\omega|^2$. So $\eta_{\mathrm{eff}} = \tau_y/(2e_{\mathrm{gen}})$ scales both the deviatoric and the couple stress, and a band narrower than $\ell$ pays for its rotation gradient. The Cosserat viscosity $\eta_c = c\,\eta_{\mathrm{lin}}$ does not yield.
Parameters: $\ell$ and $c$.
```python
omega = uw.discretisation.MeshVariable("omega", mesh, 1, degree=1, units="1/s")
spin = stokes.Unknowns.W[1, 0]
grad_omega = omega.sym.jacobian(mesh.CoordinateSystem.N)
eta_c = c * eta_lin
cm = stokes.constitutive_model      # generalised invariant in the yield law
edot_II = cm._strainrate_inv_II.sym
cm._strainrate_inv_II.sym = sympy.sqrt(edot_II**2 + ell**2 * (grad_omega * grad_omega.T)[0, 0] / 2)
stokes.add_coupled_field(
    omega,
    F0=4 * eta_c * (omega.sym[0] - spin),
    F1=2 * cm.viscosity * ell**2 * grad_omega,
    momentum_flux=2 * eta_c * (spin - omega.sym[0]) * sympy.Matrix([[0, -1], [1, 0]]),
)
```
## Example: the Cosserat shear layer
A linear Cosserat layer $0 < y < 1$, sheared by $u_x(1) = U$ with $\omega = 0$ on both walls, has a closed form. Take $\eta = \eta_c = 1$ and couple modulus $B = 2\eta\ell^2 = 0.02$. The shear stress $\sigma_{xy} = T$ is constant, and
$$
\omega = -\frac{T}{2\eta}\left[1 - \frac{\cosh k(y - \tfrac12)}{\cosh(k/2)}\right],
\qquad k^2 = \frac{4\eta_c\,\eta}{B\,(\eta + \eta_c)},
\qquad (\eta + \eta_c)\,u_x' + 2\eta_c\,\omega = T .
$$
P2 $\omega$ and P2 $\mathbf u$ converge at third order:
| $h$ | $\lVert\omega - \omega_{\mathrm{exact}}\rVert_2$ | $\lVert u_x - u_{\mathrm{exact}}\rVert_2$ |
|---|---|---|
| 1/8 | 1.09e-3 | 1.16e-4 |
| 1/16 | 1.50e-4 | 1.53e-5 |
| 1/32 | 1.93e-5 | 1.94e-6 |
The two coarser levels are a regression test in `test_1070`.
## Example: the Spiegelman notch
The notch of the [Spiegelman notch benchmark](../benchmarks/spiegelman-notch-benchmark.md):
- $\eta_{bg} = 10^{23}$ Pa s, convergence 5 mm/yr, $\phi = 30°$, $C = 10^8$ Pa, residual strength $0.02\,C$;

*(53 more added lines; see the commit.)*
