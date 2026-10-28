---
title: "Tidal faulted shell: site sweep, strength balance, the walking and its Maxwell-time scaling, slip profiles, the first far-field result"
date: "2026-10-16"
authors:
  - "Louis Moresi"
options:
  kind: "measurement"
  status: "live"
  topics:
    - "tidal-faulted-shell"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Tidal-faulted-shell/ac9db5d13dfe7aee9b855f188c747096012bc350"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`ac9db5d1`](https://github.com/underworldcode/underworld3/wiki/Tidal-faulted-shell/ac9db5d13dfe7aee9b855f188c747096012bc350) by Louis Moresi, 2026-10-16: **Tidal faulted shell: site sweep, strength balance, the walking and its Maxwell-time scaling, slip profiles, the first far-field result**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Tidal faulted shell

## Where the asymmetry comes from (site and orientation sweep)
On a stripe plane the shear and normal tractions are sinusoids in mean anomaly; the clamping's phase relative to the shear sets the kind of asymmetry. In phase or antiphase, one shear extreme meets full clamping and the other full tension: one episode is suppressed (one-sided slip). In quadrature, both extremes meet the same clamping: equal episodes, shifted onsets. The south-polar stripes at 30° sit between (clamping 80° behind the shear) and show both. Maps from the locked shell's global stress (`tidal_site_analysis.py`: traction amplitudes, clamping phase, a size index from the Coulomb windows, a timing index from the onset offsets), planes at the paper's orientation:
![site maps](../figures/tidal-shell-site-maps.png)
Frictional runs at five sites confirm the maps: pole 30° double-peaked and lopsided; pole 90° two equal rounded episodes with a shifted onset; latitude −45° on the sub-planet meridian one-sided left-lateral; latitude −45° at longitude 90° one-sided the other way; the sub-planet point no slip at all.
![sites](../figures/tidal-shell-sites.png)
## Strength against driving shear
Stripe mean, last cycle, μ = 0.4: the tidal shear peaks at 0.0275 while the strength μ(T_b − σ_n) swings from 0.0004 to 0.031, so the shear exceeds the strength over 62 % of the orbit. The right-lateral window (112–225°) opens because the tension drives the strength to nearly zero while the shear is still rising: the excess reaches three times the strength and the fault slides freely (slip 0.007). The left-lateral window (320–100°) runs against a strength 0.02 to 0.03 with an excess under 10 % of it: creep against a matched strength, the sensitive episode (the onset moves 60°, 90°, 100° for μ = 0.2, 0.4, 0.6).
![strength](../figures/tidal-shell-strength.png)
## Slip totals: the walking and its mechanism
Per orbit the two episodes last the same fraction of the cycle (0.34 each at μ = 0.4); their peak rates differ by 15 to 25 % and their totals by 10 to 33 %, growing with friction (right/left 0.99, 1.10, 1.23, 1.33 at μ = 0, 0.2, 0.4, 0.6). In an elastic shell the totals must cancel every orbit; here their difference is the net slip per orbit. Against the Maxwell time it falls close to 1/De: fitted asymptotes 0.0015, 0.0006, 0.0002 per orbit (stripe mean) at De = 1, 3, 10, so it vanishes in the elastic limit and the mechanism is the relaxation of the shear stored while the stripes are locked. The first orbit's net slip (0.008 to 0.009) is the cold-start transient at every De.
![walk](../figures/tidal-shell-walk-De.png)
Along the stripes (the paper's Fig. 4a): activity peaks at 0.4 to 0.6 of the length and stays at 66 to 76 % of its maximum one spacing from the tips; the outer stripes are 15 % more active than the inner pair, which they shield; the net offset peaks mid-stripe and halves at the ends.
![profile](../figures/tidal-shell-slip-profile.png)
## Far-field deformation (first result)
Net tangential displacement over one orbit, faulted minus unfaulted (De = 1, μ = 0.4, overburden 0.04, stripe-mean net slip 0.0028):
![far field](../figures/tidal-shell-farfield-De1.png)
| region | rms net displacement per orbit |
|---|---|
| within 15° of the stripe set | 0.0008 |
| beyond 15° | 0.0003 |
| beyond 90° | 0.00013 |
| unfaulted shell's own residual (noise floor) | 0.00006 |
The walking is not confined to the stripe block: it loads the shell as a four-lobed field, contraction across the stripes and extension along them, at about 30 % of the stripe offset in the near field and 5 % in the far hemisphere, with lobes reaching mid-latitudes along several meridians. At an ice Maxwell time of ten orbits the offset per orbit is 2 % of the diurnal slip, so the far-field strain accumulates at that fraction of the diurnal strain cycle per orbit.
A cut defect found on the way: a stripe built as a chain of great-circle arcs between exponential-map points (kinks at every vertex) lost part of its cut silently (11 of 16 facets at 9 points, fragments at 13); stripes are now single great-circle arcs. The library should refuse rather than truncate such a chain (open).
- The De 10 run to sixteen orbits (the slow Maxwell tail) and its far-field map; the far-field strain (surface divergence and shear of the net displacement).
- Opening on the stripes; stripes of the real geometry; the Jaumann rate on a drag-free sphere (fails in the linear solve; not needed for the tide).
- The cut's silent truncation of a kinked polyline.
