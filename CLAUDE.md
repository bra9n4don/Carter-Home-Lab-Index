# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not an application — it's Brandon Carter's umbrella index/documentation repo for his home lab: agent prompts, learning notes, and personal projects, organized as plain Markdown plus a handful of stdlib-only Python automation scripts (no dependencies to install, no build step, no test suite, no linter).

Read [`ai/instructions.md`](ai/instructions.md) first — it's the operating-rules doc this repo itself defines for AI agents (Copilot and others) working here: lead with the next action, keep responses short, use real paths, don't invent files. Follow it as this repo's house style. [`ai/profile.md`](ai/profile.md) has Brandon's background and working preferences (Linux beginner, wants step-by-step instructions, Fahrenheit, manual runbooks over automation scripts for admin-console work like M365/Exchange/Cloudflare).

## Commands

```bash
# Regenerate progress-tracker.md from Status:/Progress:/Next Step: fields
python scripts/update_progress_tracker.py

# Interactively add a GitHub repo to the index (fetches metadata, asks category/status/etc.)
python scripts/add_repo.py https://github.com/owner/repo-name
```

There's no local way to run `scripts/add_repo_from_issue.py` standalone — it reads `ISSUE_BODY`/`ISSUE_NUMBER` env vars and is only meant to run inside `.github/workflows/add-repo-from-issue.yml`.

## Structure and the Status:/Progress:/Next Step: convention

Four top-level workspaces, each with its own README describing subfolder layout: `agents/` (active/templates/archive/docs), `learning/` (courses/notes/resources/certifications), `personal-projects/` (ideas/active/completed/assets), `ai/` (these instructions + shared prompts + profile).

Every course file (`learning/courses/**/*.md`, excluding `README.md`) and every project folder (`personal-projects/active/*/README.md`, `personal-projects/completed/*/README.md`) is expected to carry `Status:`, `Progress:`, and (projects only) `Next Step:` lines in the `Field: value` format matched by regex in `scripts/update_progress_tracker.py`. This is load-bearing — `progress-tracker.md` at the repo root is entirely auto-generated from these fields via `.github/workflows/sync-progress-tracker.yml` (on push to `learning/**`, `personal-projects/**`, or the script itself, plus a daily 06:00 UTC cron) and should never be hand-edited.

Entry templates for new agents/courses/projects are documented in `ai/instructions.md` and, for the add-repo flow specifically, in `agents/templates/add-repo.md`.

## The add-repo automation

Two parallel entry points write repo entries into the correct folder, and both duplicate the same core logic (`fetch_repo_meta`, `fetch_repo_topics`, `slugify`, `parse_github_url`, and the three `write_*_entry` functions — ~250 lines shared verbatim):

- `scripts/add_repo.py` — interactive CLI, run locally.
- `scripts/add_repo_from_issue.py` — parses a GitHub issue body (created from the `.github/ISSUE_TEMPLATE/add-repo.yml` form) and is invoked by `.github/workflows/add-repo-from-issue.yml` whenever an issue opens with the `add-repo` label; it writes the entry, and the workflow commits/pushes it and closes the issue.

Because the logic is duplicated rather than shared, the two copies have already drifted: `add_repo_from_issue.py`'s field lookup for "Next Step" doesn't match the issue template's actual label (`Next Step (projects only)`), so issue-driven project entries always get a `TBD` next step regardless of what's typed in the form. Keep this in mind when touching either script — a fix to one does not apply to the other.

## Other workflows

- `.github/workflows/sync-labels.yml` — syncs `.github/labels.yml` to repo labels on push to that file.
- `.github/workflows/weekly-digest.yml` — every Monday, opens a new issue summarizing `progress-tracker.md`.
