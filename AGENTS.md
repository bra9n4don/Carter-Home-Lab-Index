# AGENTS.md

Guidance for AI coding agents working in this repository.

## Scope

This repository is an umbrella index for:

- `agents/` — agent prompts, workflows, configs, and docs
- `learning/` — courses, notes, resources, and certification prep
- `personal-projects/` — personal builds and experiments
- `ai/` — shared AI instructions and prompts

## Primary instructions

Read and follow:

- `/home/runner/work/Carter-Home-Lab-Index/Carter-Home-Lab-Index/ai/instructions.md`

## Working style

1. Lead with the next action.
2. Keep responses short and practical.
3. Use real file paths and concrete commands.
4. If information is missing, state exactly what is missing and what to check next.

## Change guidelines

1. Keep changes minimal and focused on the request.
2. Place new content in the correct top-level area.
3. Do not invent files or structure that do not exist; if a target file is missing, say so.
4. Prefer small, verifiable edits over broad refactors.

## Common placement patterns

### New agent

```text
agents/active/<name>/
  README.md
  prompt.md
```

### New learning item

```text
learning/<area>/<topic>.md
```

### New personal project

```text
personal-projects/active/<name>/
  README.md
```
