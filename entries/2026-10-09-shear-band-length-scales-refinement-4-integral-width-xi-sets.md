---
title: "Shear-band length scales: refinement 4, integral width, xi sets intensity not width, Cosserat comparison corrected"
date: "2026-10-09"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/9629f53ee7650e6b11d53f2940e0505b9e5c82a1"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`9629f53e`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/9629f53ee7650e6b11d53f2940e0505b9e5c82a1) by Louis Moresi, 2026-10-09: **Shear-band length scales: refinement 4, integral width, xi sets intensity not width, Cosserat comparison corrected**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

| micromorphic β = 0.1, l = 0.25–2 km | ✓ | ✓ | ✓ (5–12 steps); ref 4 ✓ (5 steps) at l = 1, 2 km |
**The width measure.** The band width is the *integral width*: on a vertical cut through one limb, the area of $\dot\varepsilon_{II}$ above the far-field background within ±6 km of the peak, divided by the peak height, times $\cos 37.5°$ for the width normal to the band; then the median over 8 cuts at $|x|$ = 12–21 km.
- It needs no support cut-off.
- The equivalent width used earlier stops its support at 10% of the peak. On these profiles, which have a long tail on the upper side, that cut-off moved by ±0.5 km between limbs and refinements.
- The spread between the 8 cuts (0.4–1.3 km) is real: each limb widens toward the surface.
**Mesh independence.** Cells are $W$ (km) / peak over background; $\xi = 0$.
| model | ref 1 | ref 2 | ref 3 | ref 4 |
|---|---|---|---|---|
| micromorphic β = 0.1, l = 0.25 km | 3.55 / 1.77 | 2.59 / 2.66 | 2.45 / 2.72 | |
| micromorphic β = 0.1, l = 0.5 km | 3.82 / 1.39 | 3.45 / 1.74 | 3.40 / 1.80 | |
| micromorphic β = 0.1, l = 1 km | 4.28 / 0.97 | 4.27 / 1.13 | 4.26 / 1.17 | **4.26 / 1.18** |
| micromorphic β = 0.1, l = 2 km | 4.10 / 0.72 | 4.36 / 0.75 | 4.49 / 0.76 | **4.52 / 0.76** |
| micromorphic β = 0.2, l = 1 km | 4.58 / 0.63 | 4.64 / 0.69 | 4.67 / 0.71 | |
| Cosserat c = 1, l = 0.5 km | | 4.42 / 0.73 | 4.45 / 0.74 | |
| Cosserat c = 1, l = 1 km | 4.89 / 0.27 | 4.91 / 0.29 | 4.93 / 0.30 | |
- From refinement 3 to 4, $W$ and the peak change by under 1%.
- From 2 to 3 they change by 0–4% in every (β, l) pair. Without a length scale the peak would roughly double with each refinement, and $W \propto \sqrt h$.
- Newton takes 5 steps at refinement 4, on tight FMG and grid-sequenced from refinement 3.
- **$l$ sets the width.** At refinement 3, β = 0.1: $W$ = 2.45, 3.40, 4.26, 4.49 km at $l$ = 0.25, 0.5, 1, 2 km.
  - $W$ rises steeply up to $l \approx 1$ km and then nearly saturates: at large $l$ the notch geometry, not $l$, bounds the band. Over $l$ = 0.25–1 km, $W \approx 2 + 2.3\,l$ km roughly. That is not proportional to $l$: the band has a structure set by the notch and the yield law on which $l$ acts.
  - The peak falls about 1.5× per doubling of $l$.
  - $l$ must be resolved: refinement 1 ($h_{\min}$ = 172 m) is under-resolved at every $l$, while refinements 2–4 agree down to $l$ = 0.25 km.
  - $\beta$ = 0.01 does nothing measurable;
  Above the threshold, a larger $\beta$ widens the band a little ($W$ = 4.26 → 4.67 km for β = 0.1 → 0.2 at $l$ = 1 km) and lowers the peak (1.17 → 0.71). It raises the yield stress near the band by up to 1.7 $C$, so $\beta$ is a physical parameter, not a numerical knob. The softening modulus estimated in the campaign handoff, $\tau_y/e_{\mathrm{band}} \approx 0.02\,\eta_{bg}$, puts the threshold at a few times that.
- **$\xi$ sets the intensity, not the width.** At β = 0.1, $l$ = 1 km, refinement 3:
  | ξ | W (km) | peak |
  |---|---|---|
  | 0 | 4.26 | 1.17 |
  | 0.01 | 4.28 | 0.78 |
  | 0.05 | 4.18 | 0.23 |
  Once $l$ has fixed the width, rate strengthening only flattens the contrast across the band. This is the linearised picture: $\xi$ adds the modulus $2\xi\eta_{bg}$ at every wavelength, $\beta$ only below $l$. Below the threshold the two add: $\beta$ = 0.05 fails at refinement 3, but with $\xi$ = 0.01 it converges, with a short-wave modulus $(\beta + 2\xi)\eta_{bg}$ = 0.07 η_bg. $\xi$ alone never regularises, because it has no length.
- **Cosserat:** $l$ sets the width there too (4.45 km at 0.5 km, 4.93 km at 1 km). The width is insensitive to $c$ (0.5 or 1), to the degree of $\omega$, and to $\xi$, which again only lowers the peak (0.30 → 0.24 at ξ = 0.01). $c \to 0$ recovers the plain problem continuously. **At the same $l$, Cosserat bands are only about 15% wider than micromorphic ones, but about 4× weaker in peak strain rate:** diffuse shear zones rather than sharp bands. (An earlier version of this page said "twice as wide"; that came from the horizontal-cut estimator and is withdrawn.)
- **Width estimators that cut the support are noisy.** The horizontal cuts cross both limbs low down; the vertical equivalent width stops at 10% of the peak. Both jitter by ±0.5 km on these tailed profiles. The integral width above replaces them.
- **Refinement 4 is slow serially**: 5 Newton steps at about 80 minutes each on the loaded campaign machine. $l$ = 0.25 and 0.5 km are still running. Parallel runs agree with serial at np = 2 (same Newton count, widths to 9 digits); the np = 4 check and refinement 5 (about 2.2M dofs) are queued.
3. Mesh independence on the notch, by integral width and peak strain rate, to refinement 4 (5 for the final word).
4. What sets the band: $l$ sets the width (saturating where the notch geometry takes over), $\beta$ must clear a threshold and then widens the band slightly, and $\xi$ sets the intensity, not the width. Below the threshold $\beta$ and $\xi$ add as $\beta + 2\xi$.
5. Micromorphic against Cosserat: both regularise. At the same $l$ the Cosserat bands are about 15% wider and about 4× weaker in peak strain rate. Their width is insensitive to $c$ and $\xi$.
Still needed: the $\beta$ threshold mapped against $\xi$ and against the softening modulus; the saturation of $W(l)$ against the notch size (a wider notch should lift the plateau); other $\eta_{bg}V$ and $\phi$; refinement 5 in parallel.
