---
title: "Shear-band length scales: figures for refinements 1-5"
date: "2026-10-10"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/7ca3fedb315bf1249df7fe00d12cd75cde56e379"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`7ca3fedb`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/7ca3fedb315bf1249df7fe00d12cd75cde56e379) by Louis Moresi, 2026-10-10: **Shear-band length scales: figures for refinements 1-5**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

**Refinements 1–5** ($h_{\min}$ = 172, 86, 43, 21, 11 m; β = 0.1, ξ = 0; rendered from the saved runs, no re-solve):
![Strain-rate maps, refinements 3-5](../figures/notch-length-scale-refinement-maps.png)
*$\log_{10}\dot\varepsilon_{II}$ at refinements 3, 4, 5 (columns), l = 1 and 0.5 km (rows), on one colour scale covering every panel. A few vertices at the weak inclusion's corners evaluate to $\dot\varepsilon_{II} \le 0$ on the rebuilt model and are drawn grey.*
![The left band with the mesh](../figures/notch-length-scale-refinement-zoom.png)
*An 8 km window on the left band at x = −15 km, with the mesh. The elements crossing the band are 530, 265 and 132 m: 9, 18 and 35 cells across W at l = 1 km. $h_{\min}$ is reached only at the notch tip.*
![Profiles across the left band, refinements 1-5](../figures/notch-length-scale-refinement-profiles.png)
*$\dot\varepsilon_{II}$ over the far-field background on the cut x = −15 km. Refinement 1 is under-resolved; refinements 2–5 lie on one curve.*
![W and peak against h](../figures/notch-length-scale-width-peak-vs-h.png)
*Integral width (background = median outside ±9 km of the peak) and peak over that background, against $h_{\min}$, for every $l$. At l = 2 km this background is noisy for the peak, because the broad band leaves only a few km of the cut outside the window.*
