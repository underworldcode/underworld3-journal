---
title: "Spiegelman notch benchmark"
options:
  kind: "benchmark"
  migrated_from: "https://github.com/underworldcode/underworld3/wiki/Spiegelman-notch-benchmark"
  wiki_created: "2026-10-05"
  wiki_last_edited: "2026-10-09"
---

```{note}
Migrated from the wiki page [Spiegelman-notch-benchmark](https://github.com/underworldcode/underworld3/wiki/Spiegelman-notch-benchmark) on 2026-10-27 as this benchmark page (to move to `docs/advanced/benchmarks/` in underworld3)'s starting text (written 2026-10-05 to 2026-10-09). The dated entries at the foot are the record; this text is trimmed as its content moves into guides, subsystem pages and entries.
```


The viscoplastic notch-localisation problem of Spiegelman, May and Wilson (2016, G³, doi:10.1002/2015GC006228), also run as the ASPECT Newton-solver benchmark set and in Fraters et al. (2018, GJI). One page per benchmark type: this is the notch; the index of all benchmark types is [Benchmarks](../benchmarks/benchmarks.md). The campaign that produced our numbers is [Spiegelman notch campaign 2026](../campaigns/spiegelman-notch-campaign-2026.md); the solver lessons are on [Solvers and multigrid](../topics/solvers-and-multigrid.md).

## The problem

A 4H × H domain, H = 30 km: a strong viscous layer (η_bg) over a weak layer (η_b = 1e21 Pa·s), a notch cut into the base of the strong layer, convergence V imposed on the sides, free top, no-slip base, gravity on (ρ = 2700 kg/m³). Drucker–Prager yielding in the strong layer, σ_y = C cos φ + p sin φ with C = 1e8 Pa and φ = 30° (our model absorbs cos φ into C); the pressure in the yield law is the total pressure, whose gauge the free surface fixes. The reference runs it at η_bg = 1e24–1e25 Pa·s and V = 2.5–10 mm/yr. The difficulty is set by the single group η_bg·V (the buoyancy and cohesion numbers both go as its inverse); at η_bg·V = 2.5e24 Pa·s·mm/yr, 94% of the strong layer is above the yield surface in the viscous solution, at 1e25 95%.

The mesh is Spiegelman's gmsh geometry: our runs use a 492-triangle base refined once (9895 dofs, P2–P0) or twice, with a Galerkin velocity multigrid on that hierarchy.

## What the references report

Not a number — a behaviour. The consistent Newton tangent has a small basin of attraction: from the viscous initial guess it stalls or diverges as φ, resolution and η_bg·V grow, and Picard converges but slowly; the published remedy is a Newton–Picard hybrid with a stabilised (SPD-modified) Jacobian and a line search, with iteration counts tabulated against resolution and friction. The shear bands form at angles near the Coulomb value 45° ± φ/2 in the sharp limit (Kaus 2010 for the angle discussion; Spiegelman et al. show the band patterns rather than fitting angles). Band width is not mesh-converged in the sharp problem — the localisation sits at the cell scale — which the regularisation literature (Duretz et al. 2019, 2021, 2023) addresses with a viscoplastic damper that sets a width D_c ~ η_vp V / C.

## Our status (2026-10-05)

| quantity | reference | ours |
|---|---|---|
| Newton from the viscous guess at η_bg·V ≳ 1e24 | stalls / diverges | reproduced; and explained — two linear failures of the consistent tangent (the yield–pressure coupling makes the Schur complement indefinite; the yielded layer gives the velocity block a mechanism mode), plus FGMRES at PETSc's default restart stagnating on that mode |
| converged sharp-law states | Newton–Picard hybrid | the residual-keyed Picard → Newton blend converges η_bg·V up to 2.5e24 from cold (5e24 case: 91 iterations, 20k velocity cycles); a cohesion ladder from the onset converges with full Newton on every rung; a power-law (n = 3) variant with yield converges only at a floor-scale rate strengthening ξ = 1e-3 |
| Picard's basin | global, slow | confirmed: Picard throughout converges where Newton cannot, at 3–4× the iterations; our default is now Newton with one automatic Picard step on a cold start |
| band angles | ≈ 45° ± φ/2 | not measured |
| band width vs h | not converged (sharp); D_c ~ η_vp V / C regularised | not measured; the width-versus-h scan of the ξ-regularised problem is the first Phase 2 item |

![the velocity mode a cold Newton state cannot solve](../figures/notch-stalled-velocity-mode.png)

*The hard state (η_bg 5e24, iteration 2 from cold): the strong layer entirely yielded (top), and the Newton velocity block's mechanism mode — a near-rigid translation of the left half of the layer about the notch (middle), with strain rate two to three decades below the notch value (bottom). Rayleigh quotient 1.8e-7 against a smallest diagonal of 4.7e-4; no multigrid resolves it and FGMRES(30) cannot build it. This is the reference behaviour, reproduced and explained.*

![shear bands across the η_bg·V ladder](../figures/notch-regime-bands.png)

*Strain-rate invariant across the η_bg·V ladder at the viscous-seed start: the band pattern is contrast-invariant, which is why the (η_bg, V) plane is one-dimensional in difficulty.*

## What we claim and do not claim

We claim the reference behaviour and its cause, and converged sharp-law states on the ladder of η_bg·V. We do not claim a band angle or a width, and we do not claim a solution of the sharp problem at n = 3 — that case converges only with the regularisation, and whether a floor-scale ξ is the stated problem is a decision on the roadmap.

## Next target

The width-versus-h scan at fixed ξ (ref 1/2/3, Gaussian-fit widths, the Duretz 2019 protocol), then band angles against the Coulomb value on the regularised problem.

## Regularised with a length scale

The micromorphic and Cosserat continua on [Shear-band length scales](../topics/shear-band-length-scales.md) converge on this benchmark at refinement 3 with no rate strengthening, and the band's peak strain rate stops changing with h. That is where the length-scale work lives; this page keeps the benchmark as posed.

## History

- 2026-10-05 — created, from the row first placed on [Benchmarks](../benchmarks/benchmarks.md); one page per benchmark type.
- 2026-10-09 — link to [Shear-band length scales](../topics/shear-band-length-scales.md), the regularised notch.

<!-- BEGIN ENTRIES (generated by scripts/build_index.py; do not edit) -->

## Entries

No entries yet.

<!-- END ENTRIES -->
