---
title: "Which fault-mesh construction is used in practice: the placed ladder with a hand-built split chain; adapt-and-cut is the automated route the hierarchy was measured on"
date: 2026-10-28
authors: [docs hub session_01HxWvn87HYCEJodpgCdaBro, for Louis Moresi]
options:
  kind: finding
  status: live
  topics: [fault-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/b99c323/zg95_lid_regimes/drivers/annulus_fault.py
    - https://github.com/lmoresi/uw3-campaigns/blob/b99c323/zg95_lid_regimes/drivers/annulus_faults.py
    - https://github.com/lmoresi/uw3-campaigns/blob/main/zg95_lid_regimes/drivers/box_fault.py
    - https://github.com/underworldcode/underworld3/tree/feature/fault-split-integration/scripts/sessions/fault_mg
    - https://github.com/underworldcode/underworld3/blob/feature/fault-split-integration/docs/developer/subsystems/fault-split-multigrid.md
---

Louis, 2026-10-28, on the UWTN 2026-022 draft: "In the diagram, we are not using the
meshing ladder which we always use in practice. That seems unwise and is difficult to
see in the mesh diagram itself." Sessions had drifted into describing two
constructions as one. This entry says which is which, from the code on the
integration head and the drivers on the campaign branch.

## What was tried

Read `place_surface.py`, `fault_mg.py`, `custom_mg.py`, `rotated_bc.py`,
`discretisation_mesh.Mesh.add_fault` and `subsystems/fault-split-multigrid.md` on
`feature/fault-split-integration` (d81a2588); the production drivers
`annulus_fault.py`, `annulus_faults.py` (zg95-annulus-for-kaiju at b99c323) and
`box_fault.py` (main); hyperion's `scripts/sessions/fault_mg/zg95_annulus.py`; and the
figure scripts behind the note's `stack.png` and `iterations.png`.

## What happened

**Production uses the ladder, with no bisection.** Every production driver (kaiju's
annulus and slab drivers, the box-fault driver, hyperion's annulus example) builds the
faulted mesh as:

1. a copy of the base's finest level (base: `Annulus(cellSize=0.5, refinement=4)`
   in the annulus drivers; the finest cell near 0.03 on a unit outer radius);
2. the fault as a structured ladder band placed into it,
   `place_fault_ribbon_2d(host, [(name, trace)], width, spines=[(name, spine)],
   margin_rings=1, clearance=0.7, split=True, mesher="ladder")`, rung spacing
   `S = 0.004`, band width `2S`, the spine split along its own rungs;
3. the multigrid tail: the base's own coarse levels, welded, and beneath the finest
   `uw_chain = 2` split ladder levels, each the same ladder at `2^k S` placed into the
   base level `k` steps below the finest. The spine is resampled so the finest rung
   count is a multiple of `2^chain`, so every coarser rung set is a subset of the
   finer one and the levels nest by vertices. A chain level the placement refuses stays
   welded (the base level itself) and the run logs it. All levels go to
   `set_custom_fmg(stokes, levels, field_id=0)`.
4. The faulted mesh is rebuilt when the trench has moved `uw_rebuild_rungs = 4` rung
   spacings (the box driver: 1); placement falls back to a wider band or two margin
   rings when the fill ring self-crosses. The network mesher is ruled out for
   production in the driver's own comment: its levels do not nest and it deadlocked
   in parallel on 2026-10-18. Hyperion's annulus example used the ladder on the
   finest only, with the welded base tail (chain 0) and an optional band patch.

**Adapt-and-cut is the route the hierarchy study was done on, and the one the library
automates.** `base.adapt(metric)` then `child.add_fault(..., split_levels=True)`
replays the cut on every add-on level (`fault_mg`'s replay knows `"line"` and
`"sheet"` recipes); that is strategy C as measured in `library_c.py`, and it is what
`fig_hierarchy_render.py` (`stack.png`) and `library_c.py` (`iterations.png`) draw.
The ladder is **not** replayed by the library: "a placed band's spines (`cut=False`)
are not replayed on the levels" (subsystem doc, limitations), and the topic page
records the ribbon replay as the next piece of library work. The production chain is
therefore driver code, about twenty-five lines, on the API the head provides.

**On the ladder the levels nest by vertices, not by P2 degrees of freedom**: the 2:1
subsampled rungs coincide, the edge midpoints do not (fault-patch record, 2026-08-24).
The transfer between any pair of levels of which either is split is the side-aware
cell-located one (`custom_mg` dispatches to `fault_mg.cell_located_transfer_parallel`
when `is_split_level` holds for either level): each fine node is located through its
own cell's centroid, so a slit node interpolates from its own side; from the welded
base to the first split ladder level the same rule applies and is unambiguous. The
clamp exists for the cut, where each cut pulls vertices onto the trace and a fine node
can lie outside its located coarse cell; on the ladder the levels nest and the clamp
never fires (measured 2026-10-13). Unreached coarse unknowns are dropped on every
hierarchy. Each split level carries its own pair frame.

**Measured on the ladder** (test_1022 rig, frictionless contact, 2026-10-13/14):
velocity iterations 6, 9, 25 with no mid level at band-to-base ratios 6, 12, 25;
welded mid levels change nothing for the split fault (21, 21, 21 at ratio 25); the
chain of split ladders from near the base's spacing brings 25 to 13, which is C on
the ladder and what the production `uw_chain` reproduces; the TI realisation gains
monotonically from welded mids (8, 6, 5, 4). Unlike C on the cut, whose counts fall
with depth (6, 5, 4), the ladder's rise with band resolution (9 to 13), because its
tail starts with a 3:1 welded-to-split jump.

**Figures that exist for the ladder**: `fig_ladder_render.py` draws the real ladder
levels of the rig zoomed to the band with the band cells shaded and the Plus and
Minus copies drawn apart (the journal's `fault-mg-ladder_levels.png`), and
`fig_ladder_depth.py` draws iterations against band depth with the tails tried
(`fault-mg-ladder_depth.png`). No figure renders the production drivers' own levels;
that needs a run.

## What we now think

The construction used in practice is the ladder with a hand-built split chain, and
the ruling of 2026-10-14 already prescribes it (the placed ladder, sub-sampled 2:1,
is the one add-on hierarchy; the finest ladder is the constraint, the tail the
choice). Adapt-and-cut is the automated library route and the route the hierarchy
strategies were compared on; it is supported and tested on the head, and it is not
what production runs. A note describing "the method we use" shows the ladder, with
the chain as the drivers build it, and labels the cut-based figures as the
hierarchy exploration. Three statements in the 2026-022 draft follow from the cut
and are not true of the ladder: the levels being non-nested, the clamp mattering,
and iteration counts falling with depth.

## Verdict

Kept. Feeds UWTN 2026-022's construction section, recipe and figure captions, the
fault-multigrid guide (a sentence saying production uses the ladder chain by hand
until the ribbon replay lands), and the integration plan (the ribbon replay is the
first library item after B and C).
