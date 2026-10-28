---
title: "Shear-band length scales: refinement 5, mesh-independent"
date: "2026-10-10"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/0545e0fd2d16d68944bff8c6a9d7134af26ae1a5"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`0545e0fd`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/0545e0fd2d16d68944bff8c6a9d7134af26ae1a5) by Louis Moresi, 2026-10-10: **Shear-band length scales: refinement 5, mesh-independent**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

| model | ref 1 | ref 2 | ref 3 | ref 4 | ref 5 |
|---|---|---|---|---|---|
| micromorphic β = 0.1, l = 0.25 km | 3.55 / 1.77 | 2.59 / 2.66 | 2.45 / 2.72 | **2.44 / 2.77** | |
| micromorphic β = 0.1, l = 0.5 km | 3.82 / 1.39 | 3.45 / 1.74 | 3.40 / 1.80 | **3.39 / 1.82** | **3.39 / 1.83** |
| micromorphic β = 0.1, l = 1 km | 4.28 / 0.97 | 4.27 / 1.13 | 4.26 / 1.17 | **4.26 / 1.18** | **4.26 / 1.18** |
| micromorphic β = 0.1, l = 2 km | 4.10 / 0.72 | 4.36 / 0.75 | 4.49 / 0.76 | **4.52 / 0.76** | |
| micromorphic β = 0.2, l = 1 km | 4.58 / 0.63 | 4.64 / 0.69 | 4.67 / 0.71 | | |
| Cosserat c = 1, l = 0.5 km | | 4.42 / 0.73 | 4.45 / 0.74 | | |
| Cosserat c = 1, l = 1 km | 4.89 / 0.27 | 4.91 / 0.29 | 4.93 / 0.30 | | |
- From refinement 3 to 4, and from 4 to 5 ($h_{\min}$ = 11 m), $W$ and the peak change by under 1%.
- Newton takes 5 steps at refinements 4 and 5, on tight FMG and grid-sequenced from the level below. The Krylov count per Newton step does not grow with refinement: 37–39 at refinement 4, 24–47 at refinement 5 on 16 ranks. Refinement 5 took 74 and 92 minutes at $l$ = 1 and 0.5 km.
- **Small $l$ is expensive for the preconditioner.** At $l$ = 0.25 km the FMG-preconditioned Krylov solve needs more than 100 iterations per Newton step and stagnates near 3e-8 relative, against 30–40 at $l$ = 1 km. Inexact Newton (Eisenstat–Walker) converges it at refinement 4 in 13 steps.
- **Parallel:** np = 2 and np = 4 agree with serial (same Newton count, widths to 1e-9); refinement 5 ran at np = 16.
3. Mesh independence on the notch, by integral width and peak strain rate, through refinement 5.
Still needed: the $\beta$ threshold against the softening modulus, and the low-β cells of the map at refinement 4; the saturation of $W(l)$ against the notch size (a wider notch should lift the plateau); other $\eta_{bg}V$ and $\phi$.
