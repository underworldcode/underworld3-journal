# Underworld journal

The lab journal of the Underworld project: what was tried, what happened, and what
we now think, one dated entry at a time. It is the home for knowledge in the
*learning* state, between a hub's working log and the versioned documentation,
and it replaces the wiki. The reasoning is in
[`INFORMATION-FLOW-PROPOSAL.md`](https://github.com/lmoresi/uw3-campaigns/blob/main/INFORMATION-FLOW-PROPOSAL.md).

Site: <https://underworldcode.github.io/underworld3-journal/>. Technical notes, the citable
series, are at <https://www.underworldcode.org/>; the documentation of the code at
a version is in `underworld3/docs/`.

## The three rules

1. **An entry is written once and never edited.** A correction is a new entry that
   links the old one. What can change is an entry's `status`: live, superseded,
   absorbed (into a guide, a subsystem page or a note), or discarded.
2. **An entry links its evidence**: the commit, the run, the transcript, the figure
   script. An entry with no link is an opinion, and says so.
3. **A topic page's conclusion is rewritten only with an entry underneath it** saying
   why. The entry list on a topic page is generated; the paragraph above it is yours.

## Closing a question

A comparison that ends with a good answer is not closed when the answer is written
down. It is closed when the preference reaches the places the next session reads
without looking for it. The fault-mesh construction is the example that set this rule
(entry `2026-10-28-which-fault-mesh-construction-is-used-in-practice`): the ladder
was ruled the hierarchy on 14 October, the ruling sat in one wiki section, the library
automated the other route, the figure scripts and the note followed the library, and
two weeks later the preference had to be re-derived.

So a `decision` entry carries three lines, and the entry is not sealed without them:

- **Preferred**: the route we use, in one sentence.
- **Allowed**: the kept alternative, and the one case in which it is the right choice.
- **Where enforced**: the places the preference now lives, each named: the capability
  guide's rulings section, the docstring of the alternative (which says it is the
  alternative and names the preferred route), the default or the convenient call
  (the preferred route must be the easier one to use, or it will lose), the example
  or fixture new work copies from.

A preference that exists only in the entry is a wish. The docs hub's monthly pass
reads every live `decision` entry and checks that each "where enforced" item exists;
one that does not is a docs issue, not a reminder.

## Writing an entry

Copy `templates/entry.md` to `entries/YYYY-MM-DD-<slug>.md`, fill in the front matter
and the three parts (what was tried, what happened, what we now think), and open a
pull request. The pull request is the discussion; its last act is the **verdict**
line at the foot of the entry (kept, and what it feeds; discarded, and why;
inconclusive, and the issue that names the next run). Then it merges and is sealed.

```
title:    one line stating the finding, not the topic
date:     YYYY-MM-DD, also the start of the filename
authors:  a person, or "session <id> on <machine>"
options:                 the journal's own fields, which MyST passes through
  kind:     finding | dead-end | measurement | decision | digest
  status:   live (the default) | superseded | absorbed | discarded
  topics:   [slug, ...]   each the stem of a page in topics/, benchmarks/ or campaigns/
  links:    the evidence
```

A **dead end** is an entry of equal standing with a finding. It is the thing a
polished document deletes and a transcript buries, and it is the main reason the
journal exists.

A **topic page** (`topics/<slug>.md`) opens with the current understanding in a few
paragraphs and ends with the generated list of its entries. A new topic is a new page
with that paragraph; the first entry tagged with it makes it live.

The **digest** (`digests/YYYY-Www.md`) is one page a week written by the docs hub:
what was learned, what shipped, what is stuck. It is the page to read to see what
others are doing.

## Building

```bash
npm install -g mystmd@1.6.7 && pip install pyyaml
python3 scripts/build_index.py        # regenerates index.md, entries.md, digests.md,
                                      # the entry lists on topic pages, and the toc
python3 scripts/build_index.py --check
myst start                            # local preview with hot reload
myst build --html                     # what CI builds and deploys
```

Run `build_index.py` before committing: CI fails if regenerating changes the tree.
Everything a reader navigates by is generated from the entries' front matter, so
nothing in the navigation can go stale.

## Layout

```
entries/      dated, immutable entries
topics/       one page per topic: current understanding + generated entry list
benchmarks/   benchmark pages (moving to underworld3/docs/advanced/benchmarks/)
campaigns/    campaign pages: what was run, what stands, what was discounted
digests/      the weekly digest
figures/      images referenced by pages and entries
templates/    the entry template
scripts/      build_index.py (generation and checks); migrate_wiki.py (the 2026-10-27
              migration from the wiki, kept as a record)
```

## Where the first hundred entries came from

The wiki (`underworld3.wiki`, 19 pages written 2026-10-05 to 2026-10-18) was
migrated on 2026-10-27: each commit became an entry dated as committed, each bullet
of a "What did not work" section became a dead-end entry dated by the commit that
introduced it, and each page became a topic, benchmark or campaign page with its
text as the starting point. The wiki is frozen with a pointer here.
