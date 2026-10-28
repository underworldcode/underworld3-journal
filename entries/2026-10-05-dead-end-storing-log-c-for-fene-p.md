---
title: "Dead end: Storing log c for FENE-P"
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

**Storing log c for FENE-P.** The conformation is bounded by L²; the nodal Galerkin projection that commits the record is not. At a cylinder wall, where log c jumps by 4 across one cell, the projection overshot by a factor 1.5 in c and committed a record with trace 105 of L² 100 from a stress whose own conformation had 70. The spring factor hit its floor, the wall layer alternated between saturated and free, and the velocity multigrid ground to the guard's hang limit. Lesson: a bounded variable is not the one to project.

Recorded on the wiki page [Viscoelastic Constitutive models](../topics/viscoelastic-constitutive-models.md) under "What did not work, and why"; the date is the commit that first carried it.
