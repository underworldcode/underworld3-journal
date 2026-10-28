---
title: "Shear-band length scales: corrected seeded micromorphic Newton counts; band trace offset"
date: "2026-10-11"
authors:
  - "lmoresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/8446443f8fcb8bd691d56d9ee23b07ee1165a22e"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`8446443f`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/8446443f8fcb8bd691d56d9ee23b07ee1165a22e) by lmoresi, 2026-10-11: **Shear-band length scales: corrected seeded micromorphic Newton counts; band trace offset**

The seeded rows for l = 0.25 and 0.5 km had taken the cold runs' counts
(uw3-campaigns 7c5d6c4). The Cosserat c = 1 band at W = 4.62 km is offset,
not rotated.

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

- **At equal width the bands are nearly the same.** Peaks agree within 3–6%. At $c$ = 1 the Cosserat $\ell$ is 0.4–0.55 of the micromorphic one. At 4.62 km the $c$ = 1 band has the same dip (45°) but its trace lies about 1 km higher on every cut, so it roots higher on the notch; the small-$c$ trace follows the micromorphic one within about 0.3 km. At 3.63 km the traces agree within the 1 km left–right scatter of the micromorphic band itself.
| 2.66 | micromorphic $\ell$ 0.25 | 8 / 10 / stalled | — | stalled | 1+8 / 1+10 / stalled |
| 3.63 | micromorphic $\ell$ 0.5 | 6 / 8 / 9 | 54 | 5 | 1+7 / 1+7 / 1+9 |
