---
name: persona-builder
description: Builds a deeply researched, expert persona (decades of experience in a domain, process or role) for the persona-hub library, runs multi-agent deep research on the field, writes the persona in the catalog's Core + Deep knowledge format, has a skeptical expert critique it, and commits it to the ai-persona-catalog GitHub repo with its roster row. Use this whenever the user wants to create, build, add, research, upgrade or refresh an expert persona, says things like "make me a persona for X", "I need an expert in Y for the hub", "add a UX designer to my experts", "rebuild the database engineer with research", or "my hub doesn't have anyone who knows Z", or wants a build to run unattended while they're away, even if they don't say "persona-builder" or "skill".
---

# Persona Builder

Builds one expert persona at a time for the persona-hub library: the most capable
practitioner research can describe, current on today's tools, and skilled at applying
that knowledge to help the user. The result is one Markdown file committed to the
catalog repo, ready for persona-hub on its next run.

**Catalog repo:** https://github.com/carterterickson/ai-persona-catalog
- `PERSONA_FORMAT.md` is the contract. Read it every run; it can change.
- `roster.md` lists existing personas.
- `personas/<id>.md` holds each persona.

## Why this is built the way it is

A persona can't teach Claude things it doesn't know. Its value comes from three places,
and every step below serves one of them:
1. **Current, sourced facts** from research: today's standards, tools and failure
   patterns, which training data may have stale or thin.
2. **A sharper lens:** the priorities, heuristics and red flags of a master, written
   down so they get applied every time instead of sometimes.
3. **Better help:** how to turn knowledge into advice this user can act on.

Generic advice adds nothing, so the process filters it out at the end.

## Step 0: Get the repo and format

Clone the catalog (shallow) into the working directory, or `git pull` if it's already
there. Read `PERSONA_FORMAT.md` and `roster.md` in full from the clone.

If cloning fails, fetch the raw files with `curl -sL
https://raw.githubusercontent.com/carterterickson/ai-persona-catalog/main/<file>`.
Don't use a summarizing web fetch for these files; it drops detail. If neither works,
say so in one line and ask the user to attach `PERSONA_FORMAT.md`.

## Step 1: Scope the persona

Pin down, from the request or with at most 3 short questions (skip any the user
already answered):
- **The role.** Title and seniority, phrased as a job ("Senior UX Designer for iOS
  apps"), not a vibe ("design guru").
- **The jobs it will do.** Review work, design from scratch, teach, plan, debug, decide?
  This decides which Deep sections get the most research.
- **Scope edges.** Platforms, tools, industries or sub-fields in and out of scope.

Restate the scope in one line before researching: "Building: Senior UX Designer,
iOS-first, for app reviews and flow design. Out of scope: marketing sites."

Then check the roster for overlap:
- **Same role exists** → this is an upgrade. Keep the id, bump `version`, and treat
  the existing file as a starting draft.
- **Partial overlap** → say which persona covers what, and set `skip_when`,
  `pairs_with` and hand-offs so the two don't report the same issue twice.

The repo is public. User context can shape *what to research*, but the persona file
stays generic: no project names, people, keys or private details.

## Step 1b: Unattended runs

A build makes dozens of web requests over about 25 minutes. In an interactive session
each one may need the user's approval, which nobody can sit through. So when the user
says "unattended", "run it while I'm away", "I'm leaving", or otherwise signals they
won't be watching, hand the build to a scheduled task instead of running it here:

1. Finish Step 1 first, while the user is still here: ask any scoping questions now,
   because nobody will answer them later.
2. Create a **one-time scheduled task** with the session's scheduling tool (search for
   it with ToolSearch if it isn't loaded), set to run about 2 minutes from now, with
   push notifications on. Leave the approval setting unset so the server picks it.
   Never use in-session cron tools; they die when this session ends.
3. Write the task's prompt as a complete standalone instruction, because the run
   starts a fresh session with no memory of this one:
   > FIRST, before any research: put the GitHub repo carterterickson/ai-persona-catalog
   > in this session's sources by calling the add_repo tool (owner
   > `carterterickson`, repo `ai-persona-catalog`, access `push`; load it with
   > ToolSearch if needed), clone it, and prove you can push with
   > `git push --dry-run origin HEAD:refs/heads/persona/{id}`. If that push is
   > refused, stop right away and report the exact error; don't research.
   > Then use the persona-builder skill to build (or upgrade/refresh) the persona:
   > {scope line from Step 1}. Id: {id}. Nobody is watching this run: don't ask
   > questions, take the most reasonable reading, and commit and push to the branch
   > `persona/{id}`, not `main`. If the final push fails anyway, save the persona
   > file and roster row to Google Drive (claude-memory/inbox) so the work isn't
   > lost with this session. Finish with a short summary of what was built, the
   > branch link, and anything UNVERIFIED.

   **Why the repo step comes first:** a scheduled run starts in a fresh cloud session
   whose GitHub access covers only the repos in its sources, and the scheduling tool
   can't set sources. Without `add_repo`, every push is refused ("not in this
   session's authorized repository set") and the finished persona dies with the
   session's container. A 2026-10-25 run lost a full build this way.
4. Tell the user in 2–3 lines: when it runs, which approval setting the task got,
   and, if its runs will ask before acting, that they can switch the task to
   **Automatically approve** in its settings (if their organization allows it).
   Name the trade-off in one line: auto-approve means nobody checks the pages the
   researchers read, so the branch-only commit is the safety net.
5. Stop. Don't also start the build in this session.

When the user comes back, they review the branch and merge it, or ask you to.

**In Claude Code**, the alternative is permanent allow rules for web research in
`.claude/settings.json` (`"allow": ["WebSearch", "WebFetch"]`; confirm the current
syntax with `/permissions`), after which the build can run in the foreground
without prompts.

## Step 2: Research the field

Create `persona_research/<id>/` in the working directory for notes.

**With subagents (the Agent or Task tool):** spawn the research lanes in
`references/research-lanes.md` **in parallel, in one turn**, as foreground
general-purpose agents. Fill each lane's prompt with the role, scope, today's date and
the notes path. Each researcher reads `references/researcher.md` (bundled here, so
this works whether or not the deep-research skill is installed). Add a scoped lane
for any major sub-field from Step 1 that the standard lanes would skim.

Web search has a shared limit per session. Six to seven lanes for one persona fits;
building two personas at once (12+ researchers) ran out of searches late in testing,
so build personas one at a time. If a researcher reports the limit, its unfinished
items go under Gaps as UNVERIFIED, and the writer keeps them marked.

Allow one follow-up round only if a lane came back empty or a core topic is missing.
More rounds risk timeouts and add little.

**Without subagents:** research the lanes yourself, one at a time, saving notes to the
same folder. Fewer searches per lane, same coverage.

Research is the expensive part. Tell the user it's running and roughly how long
(usually 10–20 minutes).

## Step 3: Write the persona

Spawn one writer agent (or do it yourself without subagents) with
`references/persona-writer.md`, the notes folder, `PERSONA_FORMAT.md`, the scope
line, and the existing persona file for an upgrade. It writes
`persona_research/<id>/<id>.md`.

## Step 4: Critique and fix

Spawn one critic agent with `references/critic.md`, the draft path, and
`persona_research/<id>/critique.md` as its output path. It reads the draft cold, as a
skeptical master of the field, and lists what is wrong, missing, generic, outdated or
unsourced. Apply the fixes it gets right (the writer or you), and note any you reject
and why. Without subagents, do the critique yourself after a break from the draft:
reread `references/critic.md` first and take the critic's stance honestly.

Then run the structural check and fix until it passes:

```bash
python <this skill dir>/scripts/check_persona.py persona_research/<id>/<id>.md
```

It checks the frontmatter, the exact `# Deep knowledge` split, Core ≤150 lines, all
required sections, a dated State of the field, and that cited [n] numbers exist in
Sources. A passing check is necessary, not sufficient: read the Core yourself and cut
any line a generic assistant would say anyway.

## Step 5: Show the user

Send the draft file and a short summary:
- Scope line and size (Core lines / Deep lines / source count)
- 3–5 of the most useful, non-obvious things the persona knows
- What the critic changed, and anything still UNVERIFIED
- Any changes to other personas (hand-offs, `pairs_with`)

Ask for approval before committing. If the user is away, commit to a branch named
`persona/<id>` instead of `main` and say so.

## Step 6: Commit

In the clone:
1. Copy the file to `personas/<id>.md`.
2. Add or update its row in `roster.md`: `| id | title | domains | pick when | researched |`.
   The `pick when` text must be specific enough to choose from on its own.
3. Update related personas: add the new id to their `pairs_with` and hand-offs where
   the domains touch, and bump their `version`.
4. Run the check script on every persona file you touched.
5. Commit with a message like `Add senior-ux-designer persona (researched 2026-10-25)`
   and push. Fetch first so the push is current.

If push fails (no access), give the user the files and the exact commands to commit them.
Don't commit the research notes; they stay in the working directory.

## Step 7: Report

One line on what was added and where, the persona's file link on GitHub, and one
suggested next step (for example: "Try it: ask persona-hub to review X").

## Refreshing a persona

When asked to refresh or update an existing persona: rerun only the State of the
field and failure-mode lanes, update those sections and `researched`, bump `version`,
and leave the rest unless research shows it's wrong. Personas researched more than
6 months ago are worth a refresh in fast-moving fields.
