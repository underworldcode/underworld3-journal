---
title: "Dead end: Snapping refined vertices onto the fillets in 3-D"
date: "2026-10-13"
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

**Snapping refined vertices onto the fillets in 3-D.** In 2-D a refinement callback that moves the refined fillet vertices back onto the arcs works: they land within $10^{-16}$ of the arc at every level, and no cell inverts. In 3-D, moving only the surface vertices turned tetrahedra inside out (2 at the first level, 11 at the second). Carrying the move into the volume did not help (2 and 17). Independent gmsh meshes per level replace it. In 2-D, snapped and unsnapped corners change $W$ by 0.13%.

Recorded on the wiki page [Shear band length scales](../topics/shear-band-length-scales.md) under "What did not work, and why"; the date is the commit that first carried it.
