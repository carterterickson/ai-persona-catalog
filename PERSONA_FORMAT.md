# Persona file format

Every persona is one Markdown file in `personas/`, named `<id>.md` (lowercase, hyphens).
The persona-hub skill reads these files. The persona-builder skill writes them.
Keep a persona under ~150 lines so several can load at once.

## Template

```markdown
---
id: senior-software-developer          # matches the file name
title: Senior Software Developer       # shown to the user
version: 1                             # bump on every edit
domains: [code architecture, code review, refactoring, testing]
pick_when: >
  One or two sentences: the requests this persona should be chosen for.
skip_when: >
  One sentence: near-misses that belong to another persona.
pairs_with: [senior-database-engineer] # personas it often works beside
---

## Who I am
Background, years, what kinds of systems they have shipped. 3–5 lines.

## What I look at
The review lens. A checklist of the things this expert checks, in priority order.

## Red flags I always call out
Problems this expert never lets slide.

## How I give advice
Voice and stance: blunt or gentle, how they rank findings, what they refuse to hand-wave.

## What I hand off
Topics this persona defers to other personas, by id.
```

## Roster entry

Every persona also gets one row in `roster.md`:

```
| id | title | domains | pick when |
```

The hub reads the roster first and loads only the persona files it picks,
so the `pick when` column must be specific enough to choose from on its own.
