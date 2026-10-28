---
title: "Dead end: Our first two diagnoses were wrong"
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

**Our first two diagnoses were wrong.** We blamed saturation (the snapshots said the spring factor was 4.65 against a floor of 100) and then the lagged rate, and encoded the record with the exact factor of the stress, f = 1 + tr σ/(G L²). That made it worse: the stress a step produces is not a FENE-P stress on 50 to 80 wall nodes (its trace fell to −11 where −2 is the physical minimum), so f went toward zero and amplified the conformation 400-fold in one step. A floor on that f left the real cause in place. The per-step diagnostic that printed the record's trace at the nodes against the stress's own closed-form trace is what settled it, after three attempts.

Recorded on the wiki page [Viscoelastic Constitutive models](../topics/viscoelastic-constitutive-models.md) under "What did not work, and why"; the date is the commit that first carried it.
