# ai-persona-catalog

Expert personas for Claude's **persona-hub** skill.

- `roster.md` — the index the hub reads to pick a panel
- `personas/` — one file per expert
- `PERSONA_FORMAT.md` — the file format new personas must follow

To add a persona: write `personas/<id>.md` in the format, add its row to `roster.md`, commit.
The hub picks it up on its next run. No skill re-install needed.

This repo is public. Keep personas generic: no project details, keys or personal info.
