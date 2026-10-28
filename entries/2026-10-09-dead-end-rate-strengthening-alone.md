---
title: "Dead end: Rate strengthening alone"
date: "2026-10-09"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Rate strengthening alone.** $\xi$ adds a modulus at every wavelength and no length, and the band width followed $W \approx 31\sqrt{\xi h}$ km. At refinement 3 with $\xi \le 0.01$, no solver route converged, even with exact linear solves: line search, trust region, warm start, homotopy, pseudo-transient continuation and partial Newton all failed.

Recorded on the wiki page [Shear band length scales](../topics/shear-band-length-scales.md) under "What did not work, and why"; the date is the commit that first carried it.
