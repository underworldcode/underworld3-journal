---
title: One line that states the finding, not the topic
date: 2026-10-27
authors: [Louis Moresi]            # a person, or "session <id> on <machine>"
options:                           # the journal's fields; MyST passes these through
  kind: finding                    # finding | dead-end | measurement | decision
  status: live
  topics: [fault-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/pull/NNN
    - https://github.com/lmoresi/uw3-campaigns/tree/main/<campaign>/<run>
---

Two or three sentences a reader can stop after: what was tried, what happened, what
we now think. Every paragraph introduces itself; a heading is a label, not a first
sentence.

## What was tried

The setup, with the numbers that matter: mesh, resolution, rank count, the branch and
commit, the options that differ from the defaults.

## What happened

The result, with the figure or table that shows it. A figure's script lives beside the
entry or in the campaign repository and is linked above.

| approach | what it does | result |
|---|---|---|
| | | |

## What we now think

The conclusion, and what it rests on. Say what is claimed and what is not.

## Verdict

One of: kept, and the topic page or guide it feeds; discarded, and why; inconclusive,
and the issue that names the next run. Appended at the end of the discussion, before
the entry is merged; after that the entry does not change.

A `decision` entry closes a question only with these three lines (see README,
"Closing a question"):

- **Preferred**: the route we use.
- **Allowed**: the kept alternative, and the one case where it is right.
- **Where enforced**: the guide's rulings section, the alternative's docstring, the
  default or convenient call, the example new work copies from; each named.
