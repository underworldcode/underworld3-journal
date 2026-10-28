---
title: "Shear-band length scales: the W(l) plateau is partly the estimator's background"
date: "2026-10-09"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/ef708be866a313871645b3f0dffd4e284f4cd95e"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`ef708be8`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/ef708be866a313871645b3f0dffd4e284f4cd95e) by Louis Moresi, 2026-10-09: **Shear-band length scales: the W(l) plateau is partly the estimator's background**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

  - $W$ rises steeply up to $l \approx 1$ km and flattens beyond. Part of that flattening is the estimator, not the notch. Widening the integration window from ±6 km to the whole cut moves $W$ by at most 1%. But the background (the median of the cut) sits inside the band's broad tails at large $l$. With the background taken from outside the band, $W$ = 3.63, 4.62, 5.42 km at $l$ = 0.5, 1, 2 km: still sublinear, but not saturated by 2 km. Refinement 3 → 4 ratios are unchanged under every variant. Over $l$ = 0.25–1 km, $W \approx 2 + 2.3\,l$ km roughly. That is not proportional to $l$: the band has a structure set by the notch and the yield law on which $l$ acts.
4. What sets the band: $l$ sets the width (sublinearly; whether the notch caps it needs a far-field background), $\beta$ must clear a threshold and then widens the band slightly, and $\xi$ sets the intensity, not the width. $\xi$ is optional, and a small amount of it buys Newton robustness out of proportion to its modulus.
