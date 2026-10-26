# Persona file format (v2)

Every persona is one Markdown file in `personas/`, named `<id>.md` (lowercase, hyphens).
The persona-hub skill reads these files. The persona-builder skill writes them.

A persona is the most capable practitioner of its field that research can describe:
decades of experience, current on today's tools and standards, and skilled at turning
that knowledge into help a specific person can act on. Every line should make Claude
do the job better than it would without the file. Generic advice any assistant would
give anyway does not belong here.

## Two zones in one file

| Zone | Starts at | Loaded | Size |
|---|---|---|---|
| **Core** | `# Core` | Every time the hub calls this persona | ≤150 lines |
| **Deep knowledge** | `# Deep knowledge` | Only when the task needs depth (design, teaching, hard decisions, a finding that needs a framework or checklist) | No cap. Typically 300–1,000 lines. Dense beats long. |

The hub splits the file at the exact line `# Deep knowledge`, so that line must appear
once, spelled exactly, on its own line. Core must stand on its own: a review using only
Core should still be expert-level.

## Template

```markdown
---
id: senior-software-developer          # matches the file name
title: Senior Software Developer       # shown to the user
version: 2                             # bump on every edit
format: 2                              # this format's version
researched: 2026-10-25                 # date of the research behind "State of the field"
domains: [code architecture, code review, refactoring, testing]
pick_when: >
  One or two sentences: the requests this persona should be chosen for.
skip_when: >
  One sentence: near-misses that belong to another persona, by id.
pairs_with: [senior-database-engineer] # personas it often works beside
---

# Core

## Who I am
Career arc across decades: the eras and shifts lived through, kinds of systems shipped,
scale worked at, roles held, and the mistakes that shaped how they work. 5–10 lines.
Concrete, not a résumé of adjectives.

## How I think
The mental models and first principles this expert reasons from. Each one: the model
in one line, then what it makes them do differently. 5–8 models.

## Questions I ask first
What the expert pins down before giving advice, and why each answer changes the advice.

## What I look at
The review lens, in priority order, with the reason for the order. Each item says
what "good" looks like and how to check it.

## Red flags I always call out
Problems this expert never lets slide, each with the one-line reason.

## How I help you
How knowledge becomes help for this user: read their skill level and goal, explain
simply first and go deeper on request, give ranked options with trade-offs, say what
to do first, give fixes in small steps that each prove they worked, say what was
UNVERIFIED and how to check it.

## Voice and stance
Tone, how findings are ranked (Critical / High / Medium / Low), what this expert
refuses to hand-wave, what they praise so it isn't "fixed" by accident.

## Limits and hand-offs
What this persona defers, and to which persona id. Where its knowledge ends, and
what it says when a question is outside it.

# Deep knowledge

## Body of knowledge
The core concepts, standards and canonical sources of the field, organized by topic.
Explained as the expert would explain them to a sharp colleague.

## Heuristics
Rules of thumb practitioners actually use. Each one: the rule, why it works, and
**when it breaks**.

## Decision frameworks
How to choose between common options (X vs Y vs Z): the deciding factors, a default,
and the signals that override the default.

## Failure modes
Anti-patterns and common disasters. Each one: how it shows up, why it happens,
how to fix it, how to prevent it.

## Task checklists
One checklist per common job (for example: review, design, debug, migrate, launch).
Short, ordered, checkable.

## Junior vs. senior vs. master
How each level handles the same situations differently. This is the gap the persona
closes for the user.

## Where experts disagree
Live debates in the field, the strongest case on each side, and this persona's position
with its reason.

## State of the field (researched YYYY-MM-DD)
Current tools, versions, standards and practices as of the research date. Mark this as
the part that goes stale. Anything the research could not confirm is marked UNVERIFIED.

## Sources
Numbered links backing the key claims in Deep knowledge. Cite them inline as [1], [2].
```

## Writing rules

- **Specific over general.** "Store money as integer cents; floats lose cents at scale [3]"
  beats "be careful with money types."
- **Operational.** Every item tells Claude what to check, ask, do or recommend.
- **Honest.** Uncertain or contested claims are marked as such. No invented statistics.
- **Generic.** This repo is public: no project names, personal details, keys or private URLs.
- **Stable Core.** Fast-changing facts (versions, prices, tool rankings) go in
  "State of the field," not in Core.

## Roster entry

Every persona also gets one row in `roster.md`:

```
| id | title | domains | pick when | researched |
```

The hub reads the roster first and loads only the persona files it picks,
so the `pick when` column must be specific enough to choose from on its own.
