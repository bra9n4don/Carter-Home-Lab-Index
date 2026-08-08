# Scripts

## update_progress_tracker.py

Scans course and project files and regenerates `progress-tracker.md` at the repo root.

**Run locally:**

```bash
python scripts/update_progress_tracker.py
```

**What it scans:**

| Source | Files picked up |
|---|---|
| `learning/courses/**/*.md` | Any `.md` file that is not `README.md` |
| `personal-projects/active/*/` | Every immediate project folder under `active` |
| `personal-projects/completed/*/` | Every immediate project folder under `completed` |

**Fields read from each file:**

- `Status:` — `in-progress`, `done`, `planned` (or aliases like `active`, `completed`, `todo`)
- `Progress:` — a percentage, e.g. `Progress: 40%`
- `Next Step:` — one-line description (projects only)

**Automation:**

The workflow [`.github/workflows/sync-progress-tracker.yml`](../.github/workflows/sync-progress-tracker.yml) runs this script automatically on every push to `main` that touches `learning/`, `personal-projects/`, or `scripts/update_progress_tracker.py`, and also on a daily schedule at 06:00 UTC.
