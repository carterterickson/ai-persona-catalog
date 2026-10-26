# ai-persona-catalog

Expert personas for Claude's **persona-hub** skill, built by the **persona-builder** skill.

- `roster.md` — the index the hub reads to pick a panel
- `personas/` — one file per expert
- `PERSONA_FORMAT.md` — the file format every persona follows (v2: Core + Deep knowledge)
- `skills/` — source for the persona-hub and persona-builder skills

To add a persona: run the persona-builder skill ("build me a persona for …"), or write
`personas/<id>.md` in the format by hand, add its row to `roster.md`, and commit.
The hub picks it up on its next run. No skill re-install needed.

This repo is public. Keep personas generic: no project details, keys or personal info.
