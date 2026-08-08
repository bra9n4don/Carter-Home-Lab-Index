#!/usr/bin/env python3
"""add_repo.py — interactively add a GitHub repo entry to the Carter Home Lab Index.

Usage:
    python scripts/add_repo.py https://github.com/owner/repo-name

The script fetches public repo metadata from the GitHub API, asks a few
clarifying questions, then writes the entry to the correct folder and file.
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
# GitHub API helpers
# ---------------------------------------------------------------------------

def fetch_repo_meta(owner: str, name: str) -> dict:
    """Fetch basic repo metadata from the GitHub REST API (no auth required for public repos)."""
    url = f"https://api.github.com/repos/{owner}/{name}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error {exc.code}: {exc.reason}")
        return {}
    except Exception as exc:  # noqa: BLE001
        print(f"Could not fetch repo metadata: {exc}")
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
# Interactive prompts
# ---------------------------------------------------------------------------

def prompt(question: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{question}{suffix}: ").strip()
    return answer if answer else default


def choose(question: str, options: list[str], default: str = "") -> str:
    print(f"\n{question}")
    for i, opt in enumerate(options, 1):
        marker = " (default)" if opt == default else ""
        print(f"  {i}. {opt}{marker}")
    while True:
        raw = input("Enter number or value: ").strip()
        if not raw and default:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        if raw in options:
            return raw
        print(f"  Please enter a number 1–{len(options)} or one of: {', '.join(options)}")


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_learning_entry(
    *,
    repo_url: str,
    name: str,
    description: str,
    status: str,
    topics: list[str],
    sub: str,  # "courses" or "resources"
) -> Path:
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


def write_project_entry(
    *,
    repo_url: str,
    name: str,
    description: str,
    status: str,
    language: str,
    next_step: str,
    sub: str,  # "ideas", "active", "completed"
) -> Path:
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


def write_agent_entry(
    *,
    repo_url: str,
    name: str,
    description: str,
    status: str,
    sub: str,  # "active", "archive"
) -> Path:
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
# Main flow
# ---------------------------------------------------------------------------

def parse_github_url(url: str) -> tuple[str, str] | None:
    match = re.search(r"github\.com/([^/]+)/([^/\s]+?)(?:\.git)?$", url.rstrip("/"))
    if match:
        return match.group(1), match.group(2)
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/add_repo.py <github-url>")
        sys.exit(1)

    repo_url = sys.argv[1].strip()
    parsed = parse_github_url(repo_url)
    if not parsed:
        print(f"Could not parse a GitHub owner/repo from: {repo_url}")
        sys.exit(1)

    owner, repo_name = parsed

    print(f"\n📦  Fetching metadata for {owner}/{repo_name} …")
    meta = fetch_repo_meta(owner, repo_name)
    topics = fetch_repo_topics(owner, repo_name) if meta else []

    github_description = meta.get("description") or ""
    github_language = meta.get("language") or ""
    display_name = meta.get("name") or repo_name

    print(f"\n  Name        : {display_name}")
    print(f"  Description : {github_description or '(none)'}")
    print(f"  Language    : {github_language or '(none)'}")
    print(f"  Topics      : {', '.join(topics) if topics else '(none)'}")

    # --- questions ---
    name = prompt("\n1. Display name for the index entry", default=display_name)
    description = prompt(
        "2. Short description (one sentence)", default=github_description
    )

    category = choose(
        "3. Category — where does this belong?",
        options=["agent", "learning / course", "learning / resource", "personal-project"],
    )

    status = choose(
        "4. Status",
        options=["planned", "in-progress", "done"],
        default="planned",
    )

    extra_topics_raw = input(
        "5. Extra tags/topics beyond GitHub's (comma-separated, or leave blank): "
    ).strip()
    if extra_topics_raw:
        extras = [t.strip() for t in extra_topics_raw.split(",") if t.strip()]
        topics = list(dict.fromkeys(topics + extras))

    # --- write ---
    out: Path

    if category == "agent":
        sub = "archive" if status == "done" else "active"
        out = write_agent_entry(
            repo_url=repo_url, name=name, description=description, status=status, sub=sub
        )

    elif category.startswith("learning"):
        sub = "resources" if "resource" in category else "courses"
        out = write_learning_entry(
            repo_url=repo_url,
            name=name,
            description=description,
            status=status,
            topics=topics,
            sub=sub,
        )

    else:  # personal-project
        if status == "done":
            sub = "completed"
        elif status == "in-progress":
            sub = "active"
        else:
            sub = "ideas"
        next_step = input("6. Next step (leave blank if not applicable): ").strip()
        out = write_project_entry(
            repo_url=repo_url,
            name=name,
            description=description,
            status=status,
            language=github_language,
            next_step=next_step,
            sub=sub,
        )

    rel = out.relative_to(ROOT)
    print(f"\n✅  Entry written to: {rel}")
    print(
        f"\nSuggested commit:\n  git add {rel}\n  git commit -m "
        f'"feat({category.split()[0]}): add {slugify(name)}"'
    )


if __name__ == "__main__":
    main()
