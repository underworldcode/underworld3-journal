---
title: "Dead end: Very small $\\ell$ under FMG"
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

**Very small $\ell$ under FMG.** At $\ell$ = 0.25 km the FMG-preconditioned solve needs more than 100 Krylov iterations per Newton step and stalls near $3\times10^{-8}$. Inexact Newton converges it.

The longer account of the unregularised problem is on [Spiegelman notch campaign 2026](../campaigns/spiegelman-notch-campaign-2026.md).

Recorded on the wiki page [Shear band length scales](../topics/shear-band-length-scales.md) under "What did not work, and why"; the date is the commit that first carried it.
