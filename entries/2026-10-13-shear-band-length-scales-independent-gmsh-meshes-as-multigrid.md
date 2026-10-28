---
title: "Shear-band length scales: independent gmsh meshes as multigrid levels in 3-D; the unregularised capped-Krylov contrast; snapping, GAMG and timing in What did not work"
date: "2026-10-13"
authors:
  - "Louis Moresi"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/4a4114737b1ca61a1b72494608c8362d2bae1fe9"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`4a411473`](https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales/4a4114737b1ca61a1b72494608c8362d2bae1fe9) by Louis Moresi, 2026-10-13: **Shear-band length scales: independent gmsh meshes as multigrid levels in 3-D; the unregularised capped-Krylov contrast; snapping, GAMG and timing in What did not work**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Shear band length scales

The same capped tolerance on the law with no length scale ($\xi$ = 0.03) shows where this reading needs care:
| linear solves | ref 2: Newton / Krylov / $W$ | ref 3: Newton / Krylov / $W$ |
|---|---|---|
| every solve to $10^{-8}$ | 6 / 264 / 3.92 km | linear solve fails (500 iterations at step 2) |
| Eisenstat–Walker capped at $10^{-2}$ | 7 / 56 / 3.92 km | 12 / 152 / 3.49 km |
- **The loose solve gets the unregularised problem through refinement 3**, where every tight solve failed. Whether the solver converges does not tell the two problems apart.
- **The answer does.** Without a length scale the width keeps falling with $h$ (4.43, 3.92, 3.49 km at refinements 1–3), while the micromorphic width settles (4.61, 4.62, 4.64 km).
- **The tight linear solve is the symptom.** It fails on the unregularised problem because that problem is sensitive to small changes, and the inexact solve does not see this. The mesh dependence of $W$ is the test to use.
### Independent gmsh meshes as multigrid levels
On a fine base the direct solve on the coarsest multigrid level dominates the cost. With native LU, a 6,067-tet base cost 57 s per Krylov iteration, against 36 s on a 1,387-tet base carrying twice the fine mesh. The base has to be fine enough to mesh the notch's fillets, yet as coarse as possible for the direct solve. So we use independent gmsh meshes as the coarse levels, as the fault stack-on adaptation does:
- the coarsest gmsh mesh barely resolves the notch;
- each gmsh level meshes the true geometry, so the crude bottom does not reach the fine grid;
- nested refinement goes only on top of the largest gmsh mesh, because gmsh is slow for large 3-D meshes;
- the transfers between non-nested levels are barycentric (`utilities/custom_mg.py`), and the coarse operators are Galerkin products, as before.
The coupled field shares the velocity block, so the transfer has to carry $\chi$ with the velocity. `set_custom_fmg(field_id=0)` now builds one transfer per field of the block, each at its own degree, and scatters them into the block's numbering. Before this, a velocity-only transfer made PETSc's Galerkin product fail (test_1075).
Both runs below use the same fine mesh: a gmsh mesh with the fillet surfaces at 0.15 km (5,116 tets), refined once. Micromorphic β = 0.1, $\ell$ = 1 km, Krylov tolerance capped at $10^{-2}$, 8 ranks each. Both were started together and timed with PETSc's `-log_view`:
| coarse levels | coarsest direct solve | Newton | Krylov | Newton solve | whole run | preconditioner apply | coarse LU factorisation |
|---|---|---|---|---|---|---|---|
| nested refinement only | LU on 5,116 tets | 6 | 55 | 4514 s | 2 h 26 min | 7955 s | 3941 s |
| gmsh 230 → 619 tets, then nested | LU on 230 tets | 6 | 55 | 2477 s | 1 h 05 min | 3012 s | 7.1 s |
The solution and the iteration counts are identical, and $W$ = 4.874 km in both. In the nested run, factorising and applying the coarse LU take most of the time (3,941 s and 3,335 s), and in the gmsh run 7 s and 227 s. Smoothing then becomes the main cost. The nested run spent its last 80 minutes alone on the machine, so if anything the 1.8× and 2.2× gains are understated. The crude bottom costs the multigrid nothing in convergence and removes the coarse-solve bottleneck. With independent gmsh levels we no longer need snapping either (see "What did not work").
- **Snapping refined vertices onto the fillets in 3-D.** In 2-D a refinement callback that moves the refined fillet vertices back onto the arcs works: they land within $10^{-16}$ of the arc at every level, and no cell inverts. In 3-D, moving only the surface vertices turned tetrahedra inside out (2 at the first level, 11 at the second). Carrying the move into the volume did not help (2 and 17). Independent gmsh meshes per level replace it. In 2-D, snapped and unsnapped corners change $W$ by 0.13%.
- **GAMG as the coarse-level solve.** It leaves the multigrid's convergence unchanged, but it is weak on the coupled block, which it treats as one scalar system. On a 6,067-tet base it took three times as long as native LU.
- **Comparing wall times from separate runs on a shared machine.** The machine runs over its physical cores, and the same run took 221 s one night and 371 s the next. An apparent 2.4× slowdown of the gmsh levels in 2-D was this, plus a different monitor setting; run side by side it was 9%. We now time only arms started together, with identical options, and read PETSc's `-log_view`.
