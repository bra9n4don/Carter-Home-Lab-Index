# Agent Templates

Reusable templates, prompts, and scaffolds for agents.

## How to use

1. If a matching template folder exists here, copy it into `agents/active/<name>/`; otherwise create `agents/active/<name>/` using the template shape below.
2. Fill in `README.md` (goal, inputs, outputs, run command) and `prompt.md` (the full system prompt).
3. Pull in shared context from [`ai/shared-prompts.md`](../../ai/shared-prompts.md) where applicable.

## Template shape

```
agents/active/<name>/
  README.md   ← goal, inputs, outputs, run command
  prompt.md   ← the agent system prompt
```

Add new template folders here as you develop reusable patterns.
