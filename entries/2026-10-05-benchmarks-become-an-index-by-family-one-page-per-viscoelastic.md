---
title: "Benchmarks become an index by family; one page per viscoelastic benchmark with the notch page's structure; LaTeX for the formulas"
date: "2026-10-05"
authors:
  - "lmoresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "benchmarks"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Benchmarks/5219031e6e7b12f04e2a8269d8d741d90f323d16"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`5219031e`](https://github.com/underworldcode/underworld3/wiki/Benchmarks/5219031e6e7b12f04e2a8269d8d741d90f323d16) by lmoresi, 2026-10-05: **Benchmarks become an index by family; one page per viscoelastic benchmark with the notch page's structure; LaTeX for the formulas**

Created the pages [Confined cylinder benchmark](../benchmarks/confined-cylinder-benchmark.md), [Creeping confined cylinder benchmark](../benchmarks/creeping-confined-cylinder-benchmark.md), [Cross slot benchmark](../benchmarks/cross-slot-benchmark.md), [Viscoelastic steady shear benchmark](../benchmarks/viscoelastic-steady-shear-benchmark.md), [Waters King start up benchmark](../benchmarks/waters-king-start-up-benchmark.md); that text is on the page, not repeated here.

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Benchmarks

The index of benchmarks we run, by family. Each benchmark type has its own page with the same structure: the problem (with its equations), what the references report, our status, figures, what we claim and do not claim, the next target, and a History. A campaign that produced the numbers has its own campaign page; the methods lessons live on the topic pages.
## Viscoelastic
| Benchmark | What it tests | Status (2026-10-05) |
|---|---|---|
| [Viscoelastic steady shear benchmark](../benchmarks/viscoelastic-steady-shear-benchmark.md) | the constitutive step against closed forms (Oldroyd-B, FENE-P) | **Done**: Oldroyd-B exact, FENE-P first order in $\Delta t/\lambda$ |
| [Waters King start-up benchmark](../benchmarks/waters-king-start-up-benchmark.md) | a transient with an analytic solution; separates integrator from transport | **Done**: nodal history converges, integration-point degrades as $\Delta t$ falls, Eulerian diverges |
| [Confined cylinder benchmark](../benchmarks/confined-cylinder-benchmark.md) | the DFG 2D-2 cylinder: Newtonian validation, then viscoelastic at Re 100 and 200 | Newtonian **passed**; viscoelastic **open** (no reference for this geometry, scheme-dependent regime) |
| [Cross-slot benchmark](../benchmarks/cross-slot-benchmark.md) | the purely elastic symmetry-breaking instability | **Found, threshold off by two**; parked |
| [Creeping confined cylinder benchmark](../benchmarks/creeping-confined-cylinder-benchmark.md) | drag against Wi at Re 0, the one tabulated VE cylinder reference | **Next target**; not started |
## Viscoplastic
| Benchmark | What it tests | Status (2026-10-05) |
|---|---|---|
| [Spiegelman notch benchmark](../benchmarks/spiegelman-notch-benchmark.md) | nonlinear solver robustness for Drucker–Prager localisation | reference behaviour reproduced and explained; widths and angles not yet measured |
- A benchmark is a page of its own, inside a family. A flat list of every benchmark one after another stopped working at the second family.

### Added to Cylinder campaign 2026

*Re 100, Wi 0.5, res 40: lift and drag for every stress scheme (see [Confined cylinder benchmark](../benchmarks/confined-cylinder-benchmark.md)).*

### Added to Spiegelman notch benchmark

The viscoplastic notch-localisation problem of Spiegelman, May and Wilson (2016, G³, doi:10.1002/2015GC006228), also run as the ASPECT Newton-solver benchmark set and in Fraters et al. (2018, GJI). One page per benchmark type: this is the notch; the index of all benchmark types is [Benchmarks](../benchmarks/benchmarks.md). The campaign that produced our numbers is [Spiegelman notch campaign 2026](../campaigns/spiegelman-notch-campaign-2026.md); the solver lessons are on [Solvers and multigrid](../topics/solvers-and-multigrid.md).
