# Second Brain — Agent Hub

## Goal

A collection of AI assistants that act as a personal second brain: capturing, organizing, and surfacing information across research and notes workflows.

## Assistants

| Subfolder | Purpose |
|---|---|
| `research/` | Deep-dive research on any topic; returns summaries and source links |
| `notes/` | Captures and organizes freeform notes into structured entries |

## Shared context

Shared prompts and system context live in [`ai/shared-prompts.md`](../../../ai/shared-prompts.md).

## How to add a new assistant

1. Create a subfolder: `agents/active/second-brain/<name>/`
2. Add `README.md` (goal, inputs, outputs, run command)
3. Add `prompt.md` (the full system prompt)
4. Reference any shared context from `ai/shared-prompts.md`
