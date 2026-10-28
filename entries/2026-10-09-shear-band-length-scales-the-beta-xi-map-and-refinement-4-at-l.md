---
title: "Shear-band length scales: the beta-xi map, and refinement 4 at l = 0.5 km"
date: "2026-10-09"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/03691780aec51dcc07c1ac066a8bb0221eff1199"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`03691780`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/03691780aec51dcc07c1ac066a8bb0221eff1199) by Louis Moresi, 2026-10-09: **Shear-band length scales: the beta-xi map, and refinement 4 at l = 0.5 km**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

  Once $l$ has fixed the width, rate strengthening only flattens the contrast across the band. This is the linearised picture: $\xi$ adds the modulus $2\xi\eta_{bg}$ at every wavelength, $\beta$ only below $l$. Below the threshold the two add: $\beta$ = 0.05 fails at refinement 3, but with $\xi$ = 0.01 it converges. $\xi$ alone never regularises, because it has no length. The map below shows that $\xi$ counts for more than its share of $\beta + 2\xi$.
- **Which parameters are needed: the $\beta$–$\xi$ map.** 32 runs at refinement 3, exact Newton:
  ![beta-xi map](../figures/notch-length-scale-beta-xi-map.png)
  - **$\xi$ is not needed for convergence.** With $\xi = 0$ every $\beta \ge 0.06$ converges at $l$ = 1 km, and every $\beta \ge 0.08$ at $l$ = 0.5 km. The threshold in $\beta$ rises as $l$ falls: a narrower band needs a stiffer micro-continuum.
  - **A little $\xi$ removes the threshold.** $\xi$ = 0.005 makes every $\beta \ge 0.06$ converge at $l$ = 0.5 km; $\xi$ = 0.02 gives 5 Newton steps in every cell.
  - **$\xi$ is worth more than 2ξ of $\beta$.** At $l$ = 0.5 km, (β, ξ) = (0.06, 0.005) converges in 12 steps while (0.07, 0) diverges, though both have $\beta + 2\xi$ = 0.07. So $(\beta + 2\xi)$ is not the controlling combination. In the linearised picture, $\xi$ also stiffens the long wavelengths, where $\beta$'s coupling vanishes ($\hat s \to 0$ for $kl \ll 1$). Newton's difficulties are evidently not confined to modes shorter than $l$.
  - **Width: $l$ first, then $\beta$, then $\xi$.** At β = 0.1, $l$ = 1 km, ξ = 0 → 0.02 changes $W$ by 1%. Near the threshold, $\xi$ widens the band by 11% at $l$ = 1 km and 16% at 0.5 km.
  - **$\xi$ lowers the peak** by a factor of 2–3 between 0 and 0.02, in every row.
  - **The strength shift stays moderate.** The largest $H\chi$ is at most 1.0 $C$, and the yield floor is never approached.
  **In practice:** to leave the band intensity alone, use $\xi = 0$ with $\beta$ just above the threshold for the chosen $l$. Adding $\xi \approx$ 0.005–0.01 halves the Newton steps near the threshold, at under 10% in $W$ and 20–40% in the peak. Caveat: these are refinement-3 numbers, and near the threshold $W$ still moved with $h$ at coarser refinements, so the low-β cells need a refinement-4 check.
- **Refinement 4 is slow serially**: 5 Newton steps at about 80 minutes each on the loaded campaign machine. $l$ = 0.5 km has converged ($W$ = 3.39 km against 3.40 at refinement 3, 5 Newton steps). At $l$ = 0.25 km the FMG-preconditioned Krylov solve needs more than 100 iterations per Newton step, against 30–40 at $l$ = 1 km. That run is going with inexact Newton. Parallel runs agree with serial at np = 2 (same Newton count, widths to 9 digits); the np = 4 check and refinement 5 (about 2.2M dofs) are queued.
4. What sets the band: $l$ sets the width (saturating where the notch geometry takes over), $\beta$ must clear a threshold and then widens the band slightly, and $\xi$ sets the intensity, not the width. $\xi$ is optional, and a small amount of it buys Newton robustness out of proportion to its modulus.
Still needed: the $\beta$ threshold against the softening modulus, and the low-β cells of the map at refinement 4; the saturation of $W(l)$ against the notch size (a wider notch should lift the plateau); other $\eta_{bg}V$ and $\phi$; refinement 5 in parallel.
