# Research lanes

Spawn one researcher per lane, all in one turn, as foreground general-purpose agents.
Replace `{ROLE}`, `{SCOPE}`, `{DATE}`, `{NOTES}` (absolute path of the notes folder)
and `{SKILL}` (this skill's directory). Add a scoped lane for any big sub-field the
standard lanes would skim (for example "SwiftData and Core Data" for a database persona
that must cover iOS).

Each prompt ends with the same line:
**First read {SKILL}/references/researcher.md for how to research and how to write your notes.**

---

## Lane 1: Body of knowledge
Research the core body of knowledge a master {ROLE} carries, scoped to: {SCOPE}.
Key questions:
- What are the foundational concepts, organized into 5–10 topic areas?
- Which standards, specs, official docs and reference works define correct practice?
- Which books, papers and courses do senior practitioners treat as canonical, and what does each teach?
- What do certification syllabi or senior-level interview loops expect someone to know?
Save to {NOTES}/1-body-of-knowledge.md

## Lane 2: How masters think
Research how the best {ROLE}s think and work, as described by recognized practitioners. Scope: {SCOPE}.
Key questions:
- What mental models and first principles do respected experts say drive their decisions?
- What rules of thumb do they use, and when do those rules break?
- What questions do they ask before giving advice or starting work?
- How do juniors, seniors and masters handle the same situation differently?
Prefer: talks, essays and interviews by named, credible practitioners; engineering or practice blogs from respected organizations.
Save to {NOTES}/2-how-masters-think.md

## Lane 3: Failure modes
Research how work in this field goes wrong. Role: {ROLE}. Scope: {SCOPE}.
Key questions:
- What are the most common and the most costly mistakes and anti-patterns?
- What do public postmortems, incident reports and case studies show about root causes?
- For each major failure: how does it show up early, how is it fixed, how is it prevented?
- What red flags make experienced reviewers stop and push back?
Save to {NOTES}/3-failure-modes.md

## Lane 4: State of the field as of {DATE}
Research the current state of practice for a {ROLE}. Scope: {SCOPE}.
Key questions:
- What are the current versions of the main tools, platforms and standards, and what changed in the last 2 years?
- Which practices are newly recommended, and which are now deprecated or discouraged?
- What do current official docs, release notes and recent industry surveys say?
- What changes are announced or in progress that a practitioner should plan for?
Constraint: prefer sources from the last 18 months; give dates for every version claim. Mark anything older as possibly stale.
Save to {NOTES}/4-state-of-the-field.md

## Lane 5: Debates and decisions
Research the live debates and common decisions in this field. Role: {ROLE}. Scope: {SCOPE}.
Key questions:
- Where do respected experts openly disagree, and what is the strongest case on each side?
- What are the most common "X vs Y" choices practitioners face, and what factors decide them?
- What sensible defaults do experts recommend, and what signals should override the default?
Save to {NOTES}/5-debates-and-decisions.md

## Lane 6: Applying expertise to help people
Research how top {ROLE}s turn expertise into useful help for others: reviews, mentoring, consulting and teaching. Scope: {SCOPE}.
Key questions:
- How do the best reviewers or consultants in this field structure feedback and rank issues?
- What checklists do practitioners use for the field's common jobs (review, design, debug, launch, etc.)?
- How do experts explain the field's hardest ideas to beginners without being wrong?
- What makes advice in this field actionable versus vague?
Save to {NOTES}/6-applying-expertise.md
