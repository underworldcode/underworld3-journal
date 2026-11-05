---
title: "No example needs an SVD coarse solve: 44 examples and tutorials lose the line, measured on hyperion where they run, and the one coarse-solve rule is in code and docs on A-prime (closes the 2026-11-05 decision)"
date: 2026-11-05
authors: ["hyperion session session_01HxWvnAXb5n85uEcw711tJC, which ran the examples", "integration session session_01HxWvn5rMK67zasgirdXszQ, which committed the bundle shift", "docs hub session_01HxWvn87HYCEJodpgCdaBro"]
options:
  kind: measurement
  status: live
  topics: [solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/tree/docs/examples-no-svd-coarse
    - https://github.com/underworldcode/underworld3/commit/4af44735
    - https://github.com/underworldcode/underworld3/issues/901
    - entries/2026-11-05-the-coarse-solve-has-one-rule-on-every-route-redundant-lu-with-a-zero-pivot-shift-and-no-svd-path.md
---

The decision entry of today left two lines of "where enforced" open: the zero-pivot shift
in the shared bundle, so the standard route carries it too, and the examples that set an
SVD coarse solve. Both are done.

## The code and the docs

A-prime (`bugfix/rotated-fmg-coarse-solve`) is at 4af44735: the docs branch
(`docs/coarse-solve-one-rule`) fast-forwarded in, and one commit that sets
`mg_coarse_redundant_pc_factor_shift_type = "nonzero"` in the shared bundle. `test_1021`
reads the shift off the live coarse solver on the native, custom-P and rotated routes;
native and custom-P multigrid on the annulus give bitwise-identical velocity and pressure,
with the same iterations, with and without it. The integration session corrected two of
the docs hub's sentences against the code: plain LU without the shift did not stop on the
one singular level measured (`test_1111`; it converged 5e-7 off), and the rotation test's
tolerance is a relative 1e-8. The pull request is not yet open; the branch is taking a
merge from `development`.

## The examples

Forty-four files under `docs/examples` and `docs/beginner/tutorials` set the velocity
block's coarse solve, or a Poisson solve's, to `svd`. All 44 lose the line on
`docs/examples-no-svd-coarse` (32966c18):

- 16 on Cartesian boxes with Dirichlet or free-slip walls and two Dirichlet Poisson solves,
  which leave no direction free, so the coarse operator is nonsingular;
- 28 on curved or periodic domains, each run twice on hyperion (np 1; underworld3 at the
  docs branch plus the bundle line, code-identical to 4af44735; PETSc 3.25.3), with and
  without the line.

What the run showed:

- **None of them ran the geometric rule.** Every example builds its mesh without a
  refinement hierarchy, so the velocity block fell back to GAMG and the line replaced only
  GAMG's own coarse solve. The rule itself is tested by A-prime's suite.
- **Where the solve ran, the line changed nothing.** Fourteen examples completed in both
  arms with the same velocity and pressure to 1e-9 or better and the same iteration
  counts: the free-slip annulus kernels, the annulus benchmark of Kramer et al., the
  free-slip spherical shell, the ellipse, tutorial 6 and nine submesh investigation
  scripts. No run met a zero pivot or `DIVERGED_PC_FAILED`.
- **Fourteen fail in both arms, for reasons that have nothing to do with the line.**
  Twelve user-facing ones stop on a removed `evalf` API, the three-index array shapes,
  pint units, `estimate_dt`, or do not parse. Tutorial 8 runs but its velocity solve hits
  its 200-iteration cap. Of the investigation scripts, `test_region_ds_phase3` segfaults
  in its first solve and `test_bootstrap_viscosity` stalls at its 1e-5 viscosity step.
- Six investigation scripts have the velocity sub-solve at its 200 cap in both arms while
  the outer SNES converges.

## What it shows beyond the coarse solve

The examples are not run by anything. On `development`, 9 of the 230 example scripts do
not parse and 33 files still call `evalf`. An issue proposing a CI parse check, a scheduled
smoke set and fix-or-retire is drafted; filing it from the docs hub was refused by the
auto-mode classifier, so it waits for Louis.

## Verdict

Kept. Closes the "where enforced" lines of the decision entry of 2026-11-05 except the
merges: A-prime's pull request and `docs/examples-no-svd-coarse`'s.
