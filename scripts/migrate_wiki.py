#!/usr/bin/env python3
"""One-off migration of the underworld3 wiki into the journal (2026-10-27).

    python3 scripts/migrate_wiki.py /path/to/underworld3.wiki

What it makes, from a clone of the wiki with its full history:

- one entry per wiki commit, dated as committed, holding the commit message and the
  text that commit added to pages that already existed (a page's creation is not
  repeated: the page itself carries that text);
- one `dead-end` entry per bullet of every "What did not work" section, dated by the
  commit that introduced it;
- one page per wiki page under topics/, benchmarks/ or campaigns/, converted from
  GitHub-wiki markdown to MyST (wiki links, inline and display math, image paths),
  with the migration noted at the top;
- figures/ with the wiki's images.

Home and How-we-plan are not migrated: the journal's front page replaces the first and
the information-flow proposal the second.

Kept as a record of how the migration was done; it is not meant to run twice.
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI_URL = "https://github.com/underworldcode/underworld3/wiki"

GROUPS = {
    "topics": [
        "Fault-multigrid", "Shear-band-length-scales", "Solvers-and-multigrid",
        "Viscoelastic-Constitutive-models", "Viscoelastic-stretch-at-large-steps",
        "Transport-histories", "Particle-to-field-projection",
    ],
    "benchmarks": [
        "Benchmarks", "Confined-cylinder-benchmark", "Creeping-confined-cylinder-benchmark",
        "Cross-slot-benchmark", "Spiegelman-notch-benchmark",
        "Viscoelastic-steady-shear-benchmark", "Waters-King-start-up-benchmark",
    ],
    "campaigns": [
        "Cylinder-campaign-2026", "Spiegelman-notch-campaign-2026",
        "Box-fault-cyclic-loading", "Tidal-faulted-shell",
    ],
}
SKIP = {"Home", "How-we-plan"}
PAGE_GROUP = {p: g for g, ps in GROUPS.items() for p in ps}

# A commit subject usually opens with the page it is about.
SUBJECT_PREFIX = [
    ("box fault", "Box-fault-cyclic-loading"),
    ("tidal faulted shell", "Tidal-faulted-shell"),
    ("fault multigrid", "Fault-multigrid"),
    ("shear-band length scales", "Shear-band-length-scales"),
    ("shear band length scales", "Shear-band-length-scales"),
    ("viscoelastic stretch at large steps", "Viscoelastic-stretch-at-large-steps"),
    ("solvers and multigrid", "Solvers-and-multigrid"),
    ("transport histories", "Transport-histories"),
    ("particle-to-field", "Particle-to-field-projection"),
    ("constitutive models", "Viscoelastic-Constitutive-models"),
    ("benchmarks", "Benchmarks"),
    ("cylinder campaign", "Cylinder-campaign-2026"),
    ("spiegelman notch campaign", "Spiegelman-notch-campaign-2026"),
    ("notch campaign", "Spiegelman-notch-campaign-2026"),
]


def slug(name):
    return name.lower()


def git(wiki, *args):
    return subprocess.run(["git", "-C", str(wiki), *args], check=True,
                          capture_output=True, text=True).stdout


def convert(text, depth):
    """GitHub-wiki markdown to MyST. `depth` is the directory depth of the output file."""
    up = "../" * depth

    def wiki_link(m):
        target, label = m.group(1).strip(), (m.group(2) or m.group(1)).strip()
        page = target.replace(" ", "-")
        for name in PAGE_GROUP:
            if name.lower() == page.lower():
                return f"[{label}]({up}{PAGE_GROUP[name]}/{slug(name)}.md)"
        if page in SKIP:
            return label
        return f"[{label}]({WIKI_URL}/{page})"

    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", wiki_link, text)
    text = re.sub(r"\$`([^`]*)`\$", r"$\1$", text)
    text = re.sub(r"```math\n(.*?)\n```", r"$$\n\1\n$$", text, flags=re.S)
    text = re.sub(r"\]\(images/", f"]({up}figures/", text)
    return text


def yaml_str(s):
    # A JSON string is a valid YAML double-quoted scalar, backslashes included.
    return json.dumps(str(s), ensure_ascii=False)


def front_matter(title, date=None, authors=None, **options):
    """MyST front matter. The journal's own fields go under `options:`, the one key
    MyST passes through without complaint; top-level keys it does not know draw a
    warning per page."""
    lines = ["---", f"title: {yaml_str(title)}"]
    if date:
        lines.append(f"date: {yaml_str(date)}")
    if authors:
        lines.append("authors:")
        lines += [f"  - {yaml_str(a)}" for a in authors]
    lines.append("options:")
    for k, v in options.items():
        if v is None or v == [] or v == "":
            continue
        if isinstance(v, list):
            lines.append(f"  {k}:")
            lines += [f"    - {yaml_str(x)}" for x in v]
        else:
            lines.append(f"  {k}: {yaml_str(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def file_slug(title, limit=64):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(s) > limit:
        s = s[:limit].rsplit("-", 1)[0]
    return s


def unique(path):
    base, n = path, 2
    while path.exists():
        path = base.with_name(f"{base.stem}-{n}{base.suffix}")
        n += 1
    return path


def kind_for(subject):
    s = subject.lower()
    if re.search(r"retired|did not work|dead end|wrong|blows up|misread", s):
        return "dead-end"
    if re.search(r"ruling|decision|chosen|rule\b", s):
        return "decision"
    if re.search(r"measured|counts?\b|cost|scaling|sweep|iteration|resolution|profile", s):
        return "measurement"
    return "finding"


def topics_for(subject, files):
    for prefix, page in SUBJECT_PREFIX:
        if subject.lower().startswith(prefix):
            return [slug(page)]
    pages = [pathlib.Path(f).stem for f in files]
    return [slug(p) for p in pages if p in PAGE_GROUP]


def migrate_pages(wiki):
    made = []
    for group, names in GROUPS.items():
        out_dir = ROOT / group
        out_dir.mkdir(exist_ok=True)
        for name in names:
            src = wiki / f"{name}.md"
            if not src.exists():
                print(f"missing wiki page {name}", file=sys.stderr)
                continue
            text = src.read_text()
            m = re.match(r"^# (.+)\n", text)
            title = m.group(1).strip() if m else name.replace("-", " ")
            body = text[m.end():] if m else text
            created = git(wiki, "log", "--reverse", "--format=%cs", "--", src.name).splitlines()[0]
            last = git(wiki, "log", "-1", "--format=%cs", "--", src.name).strip()
            note = {
                "topics": "topic page",
                "benchmarks": "benchmark page (to move to `docs/advanced/benchmarks/` in underworld3)",
                "campaigns": "campaign page",
            }[group]
            head = front_matter(title, kind=group[:-1] if group != "topics" else "topic",
                                migrated_from=f"{WIKI_URL}/{name}", wiki_created=created,
                                wiki_last_edited=last)
            banner = (f"```{{note}}\nMigrated from the wiki page [{name}]({WIKI_URL}/{name}) on "
                      f"2026-10-27 as this {note}'s starting text (written {created} to {last}). "
                      "The dated entries at the foot are the record; this text is trimmed as its "
                      "content moves into guides, subsystem pages and entries.\n```\n\n")
            (out_dir / f"{slug(name)}.md").write_text(head + banner + convert(body, 1))
            made.append(name)
    return made


def migrate_figures(wiki):
    src, dst = wiki / "images", ROOT / "figures"
    dst.mkdir(exist_ok=True)
    n = 0
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, dst / f.name)
            n += 1
    return n


def added_text(wiki, sha, path):
    diff = git(wiki, "show", "--format=", "--unified=0", sha, "--", path)
    out = []
    for line in diff.splitlines():
        if line.startswith("+++") or not line.startswith("+"):
            continue
        line = line[1:]
        if re.match(r"^- 20\d\d-\d\d-\d\d", line):   # a History bullet duplicates the commit
            continue
        out.append(line)
    return out


def migrate_commits(wiki):
    log = git(wiki, "log", "--reverse", "--format=%H%x09%cs%x09%an%x09%s")
    (ROOT / "entries").mkdir(exist_ok=True)
    n = 0
    for row in log.splitlines():
        sha, date, author, subject = row.split("\t", 3)
        body = git(wiki, "show", "-s", "--format=%b", sha).strip()
        status = git(wiki, "show", "--format=", "--name-status", sha)
        files, new_files = [], []
        for line in status.splitlines():
            parts = line.split("\t")
            if len(parts) < 2 or not parts[-1].endswith(".md"):
                continue
            files.append(parts[-1])
            if parts[0].startswith("A"):
                new_files.append(parts[-1])
        pages = [pathlib.Path(f).stem for f in files]
        if pages and all(p in SKIP for p in pages):
            continue
        topics = topics_for(subject, files)
        if not topics:
            continue
        sections = []
        for f in files:
            page = pathlib.Path(f).stem
            if page in SKIP or page not in PAGE_GROUP or f in new_files:
                continue
            lines = added_text(wiki, sha, f)
            lines = [l for l in lines if l.strip()]
            if not lines:
                continue
            capped = lines[:80]
            more = len(lines) - len(capped)
            block = "\n".join(capped)
            if more > 0:
                block += f"\n\n*({more} more added lines; see the commit.)*"
            sections.append(f"### Added to {page.replace('-', ' ')}\n\n{block}")
        created = [pathlib.Path(f).stem for f in new_files if pathlib.Path(f).stem in PAGE_GROUP]
        intro = [f"Wiki commit [`{sha[:8]}`]({WIKI_URL}/{pathlib.Path(files[0]).stem}/{sha}) "
                 f"by {author}, {date}: **{subject}**"]
        if body:
            intro.append(body)
        if created:
            intro.append("Created the page" + ("s " if len(created) > 1 else " ") +
                         ", ".join(f"[{c.replace('-', ' ')}](../{PAGE_GROUP[c]}/{slug(c)}.md)" for c in created) +
                         "; that text is on the page, not repeated here.")
        if sections:
            intro.append("The text this commit added, as written that day (the integrated version "
                         "is on the topic page):")
        text = front_matter(convert(subject, 1), date=date, authors=[author], kind=kind_for(subject),
                            status="live", topics=topics,
                            links=[f"{WIKI_URL}/{pathlib.Path(files[0]).stem}/{sha}"],
                            origin="wiki commit, migrated 2026-10-27")
        text += "\n\n".join(intro) + "\n"
        if sections:
            text += "\n" + convert("\n\n".join(sections), 1) + "\n"
        path = unique(ROOT / "entries" / f"{date}-{file_slug(subject)}.md")
        path.write_text(text)
        n += 1
    return n


def bullets_of_section(text, heading_re):
    m = re.search(heading_re, text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    section = rest[:end.start()] if end else rest
    bullets, cur = [], None
    for line in section.splitlines():
        if re.match(r"^- ", line):
            if cur:
                bullets.append("\n".join(cur))
            cur = [line]
        elif cur is not None and (line.startswith("  ") or line.strip() == ""):
            cur.append(line)
        elif cur is not None and line.strip():
            cur.append(line)
    if cur:
        bullets.append("\n".join(cur))
    return [b.strip() for b in bullets if b.strip()]


def migrate_dead_ends(wiki):
    n = 0
    for group, names in GROUPS.items():
        for name in names:
            src = wiki / f"{name}.md"
            if not src.exists():
                continue
            text = src.read_text()
            for bullet in bullets_of_section(text, r"^## What did not work.*$"):
                first = bullet.splitlines()[0][2:].strip()
                m = re.match(r"\*\*(.+?)\*\*", first)
                title = (m.group(1) if m else " ".join(first.split()[:10])).rstrip(".:")
                needle = (m.group(1) if m else first)[:40]
                dates = git(wiki, "log", "--reverse", "--format=%cs", "-S", needle, "--", src.name).splitlines()
                date = dates[0] if dates else git(wiki, "log", "--reverse", "--format=%cs", "--", src.name).splitlines()[0]
                body = convert(bullet[2:] if bullet.startswith("- ") else bullet, 1)
                body = re.sub(r"^  ", "", body, flags=re.M)
                fm = front_matter(f"Dead end: {convert(title, 1)}", date=date, authors=["Underworld sessions (wiki)"],
                                  kind="dead-end", status="live", topics=[slug(name)],
                                  links=[f"{WIKI_URL}/{name}"],
                                  origin="wiki 'What did not work' section, migrated 2026-10-27")
                page_link = f"[{name.replace('-', ' ')}](../{group}/{slug(name)}.md)"
                out = fm + body + f"\n\nRecorded on the wiki page {page_link} under \"What did not work, and why\"; the date is the commit that first carried it.\n"
                path = unique(ROOT / "entries" / f"{date}-dead-end-{file_slug(title, 48)}.md")
                path.write_text(out)
                n += 1
    return n


def main():
    wiki = pathlib.Path(sys.argv[1]).resolve()
    pages = migrate_pages(wiki)
    figs = migrate_figures(wiki)
    commits = migrate_commits(wiki)
    dead = migrate_dead_ends(wiki)
    print(f"pages {len(pages)}, figures {figs}, commit entries {commits}, dead-end entries {dead}")


if __name__ == "__main__":
    main()
