# Add Repo — Copilot Agent Prompt

Use this prompt to add a GitHub repository to the correct location in this index.

## How to use

1. Start a Copilot Chat session in this repository.
2. Paste the prompt below (fill in the URL).
3. Answer the clarifying questions Copilot asks.
4. Copilot will write the entry to the correct file and commit it.

---

## Prompt (copy and paste this)

```
I want to add a GitHub repository to the Carter Home Lab Index.

Repo URL: <PASTE URL HERE>

Please:
1. Fetch the repo's metadata (name, description, topics, primary language).
2. Ask me the following questions before making any changes:
   a. Category — is this an agent, a learning resource/course, or a personal project?
   b. Status — is it planned, in-progress, or completed/done?
   c. Short description — one sentence on what it does (or confirm the GitHub description is accurate).
   d. Tags/topics — any extra tags beyond what GitHub shows?
   e. Where to file it — confirm the target folder based on my answers above.
3. Based on my answers, add an entry to the correct README.md:
   - Agent    → agents/active/<name>/README.md  (or agents/archive/ if retired)
   - Learning → learning/courses/<name>.md      (or learning/resources/)
   - Project  → personal-projects/active/<name>/README.md  (or ideas/ / completed/)
4. Use the existing frontmatter style already in that folder.
5. Commit with message:  feat(<category>): add <repo-name>
```

---

## Decision map

| Category | Status | Target path |
|---|---|---|
| agent | planned / in-progress | `agents/active/<name>/` |
| agent | retired | `agents/archive/<name>/` |
| learning | any | `learning/courses/<name>.md` or `learning/resources/<name>.md` |
| project | idea / planned | `personal-projects/ideas/<name>.md` |
| project | in-progress | `personal-projects/active/<name>/README.md` |
| project | done | `personal-projects/completed/<name>/README.md` |

---

## Entry format (reference)

### Course / learning entry (`learning/courses/<name>.md`)

```markdown
# <Repo / Course Name>

Status: planned
Progress: 0%

## Source

<URL>

## Description

<One sentence description.>

## Topics

- <topic 1>
- <topic 2>

## Notes
```

### Project entry (`personal-projects/active/<name>/README.md`)

```markdown
# <Project Name>

Status: in-progress
Progress: 0%

## Source

<URL>

## Description

<One sentence description.>

## Stack

- <language / framework>

## Next Step

<First concrete action.>

## Notes
```

### Agent entry (`agents/active/<name>/README.md`)

```markdown
# <Agent Name>

Status: in-progress

## Source

<URL>

## Goal

<One sentence on what this agent does.>

## Inputs / Outputs

**Input:**
**Output:**

## Run Command

```bash

```

## Notes
```
