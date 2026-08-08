#!/usr/bin/env python3
"""add_repo_from_issue.py — parses a GitHub issue created by the add-repo issue form
and writes the correct index entry.

Called by the `add-repo-from-issue.yml` GitHub Actions workflow.
Environment variables consumed:
  ISSUE_BODY   — raw issue body (set by the workflow from github.event.issue.body)
  GITHUB_TOKEN — optional, used to authenticate GitHub API calls
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Issue body parser
# ---------------------------------------------------------------------------

def extract_field(body: str, label: str) -> str:
    """Extract the value after a markdown heading that matches *label* (case-insensitive)."""
    pattern = rf"###\s+{re.escape(label)}\s*\n+(.*?)(?=\n###|\Z)"
    match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# GitHub API helpers (duplicated from add_repo.py to keep scripts independent)
# ---------------------------------------------------------------------------

def fetch_repo_meta(owner: str, name: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{name}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: could not fetch repo metadata: {exc}")
        return {}


def fetch_repo_topics(owner: str, name: str) -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{name}/topics"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode()).get("names", [])
    except Exception:  # noqa: BLE001
        return []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_github_url(url: str) -> tuple[str, str] | None:
    match = re.search(r"github\.com/([^/]+)/([^/\s]+?)(?:\.git)?$", url.rstrip("/"))
    if match:
        return match.group(1), match.group(2)
    return None


# ---------------------------------------------------------------------------
# File writers (same format as add_repo.py)
# ---------------------------------------------------------------------------

def write_learning_entry(*, repo_url, name, description, status, topics, sub) -> Path:
    slug = slugify(name)
    target_dir = ROOT / "learning" / sub
    ensure_dir(target_dir)
    out = target_dir / f"{slug}.md"
    topics_lines = "\n".join(f"- {t}" for t in topics) if topics else "- (none)"
    out.write_text(
        dedent(f"""\
            # {name}

            Status: {status}
            Progress: 0%

            ## Source

            {repo_url}

            ## Description

            {description}

            ## Topics

            {topics_lines}

            ## Notes

            """),
        encoding="utf-8",
    )
    return out


def write_project_entry(*, repo_url, name, description, status, language, next_step, sub) -> Path:
    slug = slugify(name)
    if sub in ("active", "completed"):
        target_dir = ROOT / "personal-projects" / sub / slug
        ensure_dir(target_dir)
        out = target_dir / "README.md"
    else:
        target_dir = ROOT / "personal-projects" / sub
        ensure_dir(target_dir)
        out = target_dir / f"{slug}.md"
    progress = "100%" if status == "done" else "0%"
    out.write_text(
        dedent(f"""\
            # {name}

            Status: {status}
            Progress: {progress}

            ## Source

            {repo_url}

            ## Description

            {description}

            ## Stack

            - {language or "unknown"}

            ## Next Step

            {next_step or "TBD"}

            ## Notes

            """),
        encoding="utf-8",
    )
    return out


def write_agent_entry(*, repo_url, name, description, status, sub) -> Path:
    slug = slugify(name)
    target_dir = ROOT / "agents" / sub / slug
    ensure_dir(target_dir)
    out = target_dir / "README.md"
    out.write_text(
        dedent(f"""\
            # {name}

            Status: {status}

            ## Source

            {repo_url}

            ## Goal

            {description}

            ## Inputs / Outputs

            **Input:**
            **Output:**

            ## Run Command

            ```bash

            ```

            ## Notes

            """),
        encoding="utf-8",
    )
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    body = os.environ.get("ISSUE_BODY", "")
    if not body:
        print("ERROR: ISSUE_BODY environment variable is empty.")
        sys.exit(1)

    repo_url = extract_field(body, "Repository URL")
    category = extract_field(body, "Category")
    status = extract_field(body, "Status")
    description_override = extract_field(body, "Short Description")
    tags_raw = extract_field(body, "Tags / Topics")
    next_step = extract_field(body, "Next Step")

    if not repo_url:
        print("ERROR: Could not find 'Repository URL' in issue body.")
        sys.exit(1)

    parsed = parse_github_url(repo_url)
    if not parsed:
        print(f"ERROR: Could not parse GitHub URL: {repo_url}")
        sys.exit(1)

    owner, repo_name = parsed
    print(f"Fetching metadata for {owner}/{repo_name} …")
    meta = fetch_repo_meta(owner, repo_name)
    topics = fetch_repo_topics(owner, repo_name) if meta else []

    name = meta.get("name") or repo_name
    description = description_override or meta.get("description") or ""
    language = meta.get("language") or ""

    # Merge extra tags from the issue
    if tags_raw:
        extras = [t.strip() for t in re.split(r"[\n,]+", tags_raw) if t.strip()]
        topics = list(dict.fromkeys(topics + extras))

    # Normalize status
    status_map = {
        "planned": "planned",
        "in-progress": "in-progress",
        "in progress": "in-progress",
        "done": "done",
        "completed": "done",
    }
    status = status_map.get(status.lower(), "planned")

    # Write entry
    out: Path

    if "agent" in category.lower():
        sub = "archive" if status == "done" else "active"
        out = write_agent_entry(repo_url=repo_url, name=name, description=description, status=status, sub=sub)

    elif "learning" in category.lower() or "course" in category.lower() or "resource" in category.lower():
        sub = "resources" if "resource" in category.lower() else "courses"
        out = write_learning_entry(repo_url=repo_url, name=name, description=description, status=status, topics=topics, sub=sub)

    else:  # personal-project
        if status == "done":
            sub = "completed"
        elif status == "in-progress":
            sub = "active"
        else:
            sub = "ideas"
        out = write_project_entry(
            repo_url=repo_url, name=name, description=description, status=status,
            language=language, next_step=next_step, sub=sub,
        )

    rel = out.relative_to(ROOT)
    print(f"Entry written to: {rel}")

    # Write outputs for the workflow steps
    category_short = category.split("/")[0].strip().split()[0]
    commit_msg = f"feat({category_short}): add {slugify(name)}"
    Path("/tmp/add_repo_commit_msg.txt").write_text(commit_msg, encoding="utf-8")
    Path("/tmp/add_repo_entry_path.txt").write_text(str(rel), encoding="utf-8")


if __name__ == "__main__":
    main()
