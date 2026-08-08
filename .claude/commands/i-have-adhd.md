---
description: Re-orient me — summarize what's in-progress vs. stale across the repo
allowed-tools: Read, Glob, Bash(git log:*)
---

Re-orient the user in this repo. They've lost track of where they left off and want a fast, low-effort summary — not a re-read of every file.

Do this:

1. Read `progress-tracker.md` for the current Done / In Progress / Planned snapshot (Courses + Home Projects tables).
2. For each `in-progress` Home Project listed there, open its `README.md` (e.g. `personal-projects/active/<name>/README.md`) and pull the `Next Step:` line. If it has an `## Open items` section (e.g. `home-server`), pull those bullets too.
3. Glob `personal-projects/ideas/*.md` (excluding `README.md`). List each as uncommitted backlog — filename and its `## Why` line if present. This surfaces things captured but never promoted to `active/`.
4. For each active project path from step 2, run `git log -1 --format=%cr -- <path>` to get a rough recency ("3 days ago"). There's no repo-wide "Last Updated" field convention yet, so this is the staleness fallback.
5. Check whether `progress-tracker.md` looks out of sync with the source files you just read (e.g. a `Next Step:` in a README doesn't match what's in the tracker). If so, flag it and suggest running `scripts/update_progress_tracker.py`.
6. Respond using this repo's standard output format (from `ai/shared-prompts.md`):
   - One-sentence summary of overall state.
   - Up to 5 bullets, one per active item: name, status, next step, recency.
   - If there's backlog from step 3, a short "not yet started" line.
   - One concrete next step to resume work — pick the most actionable item, per `ai/instructions.md`'s operating style.

Use real paths and real field values from the files — never placeholders. If something referenced above is missing, say so plainly instead of guessing.
