#!/usr/bin/env python3
"""Structural check for a persona file in the ai-persona-catalog v2 format.

Usage: python check_persona.py personas/<id>.md [more files...]
Exit code 0 = all files pass; 1 = at least one problem.
"""
import re
import sys
from pathlib import Path

CORE_MAX_LINES = 150
REQUIRED_FRONTMATTER = ["id", "title", "version", "format", "researched",
                        "domains", "pick_when", "skip_when", "pairs_with"]
CORE_SECTIONS = ["Who I am", "How I think", "Questions I ask first", "What I look at",
                 "Red flags I always call out", "How I help you", "Voice and stance",
                 "Limits and hand-offs"]
DEEP_SECTIONS = ["Body of knowledge", "Heuristics", "Decision frameworks", "Failure modes",
                 "Task checklists", "Junior vs. senior vs. master", "Where experts disagree",
                 "State of the field", "Sources"]


def check(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Frontmatter
    if not lines or lines[0].strip() != "---":
        return ["file must start with a '---' frontmatter block"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ["frontmatter block is not closed with '---'"]
    fm = "\n".join(lines[1:end])
    for key in REQUIRED_FRONTMATTER:
        if not re.search(rf"^{key}:", fm, re.M):
            problems.append(f"frontmatter missing '{key}'")
    m = re.search(r"^id:\s*(\S+)", fm, re.M)
    if m and m.group(1) != path.stem:
        problems.append(f"id '{m.group(1)}' does not match file name '{path.stem}'")
    m = re.search(r"^researched:\s*(\d{4}-\d{2}-\d{2})", fm, re.M)
    if not m:
        problems.append("'researched' must be a YYYY-MM-DD date")
    researched = m.group(1) if m else None
    if not re.search(r"^format:\s*2\b", fm, re.M):
        problems.append("'format' must be 2")

    body = lines[end + 1:]

    # Zone markers
    core_idx = [i for i, l in enumerate(body) if l.rstrip() == "# Core"]
    deep_idx = [i for i, l in enumerate(body) if l.rstrip() == "# Deep knowledge"]
    if len(core_idx) != 1:
        problems.append(f"need exactly one '# Core' line, found {len(core_idx)}")
    if len(deep_idx) != 1:
        problems.append(f"need exactly one '# Deep knowledge' line, found {len(deep_idx)}")
    if problems and (len(core_idx) != 1 or len(deep_idx) != 1):
        return problems
    c, d = core_idx[0], deep_idx[0]
    if c > d:
        problems.append("'# Core' must come before '# Deep knowledge'")
        return problems

    core = body[c:d]
    deep = body[d:]
    core_len = len(core)
    if core_len > CORE_MAX_LINES:
        problems.append(f"Core is {core_len} lines; limit is {CORE_MAX_LINES}")

    def headings(block):
        return [l[3:].strip() for l in block if l.startswith("## ")]

    core_h, deep_h = headings(core), headings(deep)
    for s in CORE_SECTIONS:
        if not any(h.startswith(s) for h in core_h):
            problems.append(f"Core missing section '## {s}'")
    for s in DEEP_SECTIONS:
        if not any(h.startswith(s) for h in deep_h):
            problems.append(f"Deep missing section '## {s}'")

    # State of the field date matches frontmatter
    sotf = [h for h in deep_h if h.startswith("State of the field")]
    if sotf:
        dm = re.search(r"\d{4}-\d{2}-\d{2}", sotf[0])
        if not dm:
            problems.append("'State of the field' heading needs '(researched YYYY-MM-DD)'")
        elif researched and dm.group(0) != researched:
            problems.append("State of the field date differs from frontmatter 'researched'")

    # Citations vs sources
    deep_text = "\n".join(deep)
    src_start = deep_text.find("## Sources")
    before_sources = deep_text[:src_start] if src_start >= 0 else deep_text
    sources_text = deep_text[src_start:] if src_start >= 0 else ""
    cited = set(int(n) for n in re.findall(r"\[(\d{1,3})\](?!\()", before_sources))
    listed = set(int(n) for n in re.findall(r"^\s*(?:-\s*)?\[(\d{1,3})\]\s*\[.+?\]\(https?://", sources_text, re.M))
    if not listed:
        problems.append("Sources has no entries in the form '[n] [Title](https://...)'")
    missing = sorted(cited - listed)
    if missing:
        problems.append(f"cited but not listed in Sources: {missing[:15]}")
    if listed and not cited:
        problems.append("Sources listed but nothing in Deep cites them as [n]")

    stats = f"Core {core_len} lines, Deep {len(deep)} lines, {len(listed)} sources, {len(cited)} cited"
    print(f"{path}: {stats}")
    return problems


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    failed = False
    for arg in sys.argv[1:]:
        p = Path(arg)
        probs = check(p)
        if probs:
            failed = True
            print(f"FAIL {p}")
            for pr in probs:
                print(f"  - {pr}")
        else:
            print(f"PASS {p}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
