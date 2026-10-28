---
title: "Dead end: Rewiring the smoothing expression unconditionally"
date: "2026-10-05"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "viscoelastic-constitutive-models"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-Constitutive-models"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Rewiring the smoothing expression unconditionally** forced a C-source regeneration every step for every history commit; comparing the value first cut the Oldroyd-B shear-box step from 7.5 to 1.2 s.

Recorded on the wiki page [Viscoelastic Constitutive models](../topics/viscoelastic-constitutive-models.md) under "What did not work, and why"; the date is the commit that first carried it.
