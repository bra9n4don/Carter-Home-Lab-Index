# AI Instructions — Carter Home Lab Index

These instructions apply to Copilot and any AI agents working in this repo.

## Operating style

1. Lead with the next action.
2. Keep responses short and practical.
3. Number multi-step instructions.
4. End with one concrete next step.
5. Avoid tangents unless the user asks.
6. Use actual file names, paths, and commands — never generic placeholders.
7. If something is missing or unclear, say what it is and what to check next.

## Repo behavior

- Answer relative to this repo's structure, not generic advice.
- The top-level areas are:
  - `agents/` — agent prompts, workflows, and configs
  - `learning/` — courses, notes, resources, and cert prep
  - `personal-projects/` — personal builds and experiments
  - `ai/` — these instructions and any shared prompts
- See [`ai/profile.md`](profile.md) for Brandon's background, current homelab focus areas, and working preferences.
- When planning work, break it into small steps and reference the relevant folder.
- Do not invent files that do not exist. If a file is missing, say so.

## Response format

- Start with the result or recommendation.
- Use short bullet lists (5 items max).
- For setup steps, use this shape:
  1. Do X
  2. Then do Y
  3. Verify with Z

## Planning shape

When asked to plan a task, produce:

- **Goal** — one sentence
- **Files to create or change** — list with paths
- **Steps** — numbered
- **Verification** — how to confirm it worked

## Entry templates

### New agent

```
agents/active/<name>/
  README.md   ← goal, inputs, outputs, run command
  prompt.md   ← the agent prompt
```

### New learning item

```
learning/courses/<platform>/<topic>.md
  # <Topic>
  Source: <url or course name>
  Status: in-progress | done
  Progress: 0%
  Notes: ...
```

Example: `learning/courses/github/intro-to-actions.md`

### New project

```
personal-projects/active/<name>/
  README.md   ← goal, status, stack, next step
```
