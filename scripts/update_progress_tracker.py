from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TRACKER_PATH = ROOT / "progress-tracker.md"
COURSE_BASES = [ROOT / "learning" / "courses", ROOT / "learning" / "education"]


@dataclass
class Item:
    name: str
    rel_path: str
    status: str
    progress: int | None
    next_step: str | None = None


@dataclass
class Summary:
    total: int
    done: int
    in_progress: int
    planned: int
    unknown: int
    completion: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_field(text: str, field: str) -> str | None:
    pattern = rf"(?im)^{re.escape(field)}:\s*(.+)\s*$"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+)$", text)
    return match.group(1).strip() if match else fallback


def normalize_status(status: str | None) -> str:
    if not status:
        return "unknown"
    value = status.strip().lower()
    mapping = {
        "done": "done",
        "completed": "done",
        "complete": "done",
        "in-progress": "in-progress",
        "in progress": "in-progress",
        "active": "in-progress",
        "planned": "planned",
        "todo": "planned",
    }
    return mapping.get(value, value)


def parse_progress(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"(\d{1,3})\s*%", value)
    if not match:
        return None
    percent = int(match.group(1))
    return max(0, min(percent, 100))


def collect_courses() -> list[Item]:
    items: list[Item] = []
    for base in COURSE_BASES:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            text = read_text(path)
            items.append(
                Item(
                    name=extract_title(text, path.stem),
                    rel_path=path.relative_to(ROOT).as_posix(),
                    status=normalize_status(extract_field(text, "Status")),
                    progress=parse_progress(extract_field(text, "Progress")),
                )
            )
    return items


def collect_projects() -> list[Item]:
    items: list[Item] = []
    project_bases = [
        (ROOT / "personal-projects" / "active", "in-progress"),
        (ROOT / "personal-projects" / "completed", "done"),
    ]
    for base, default_status in project_bases:
        if not base.exists():
            continue
        for project_dir in sorted(p for p in base.iterdir() if p.is_dir()):
            readme = project_dir / "README.md"
            text = read_text(readme) if readme.exists() else ""
            items.append(
                Item(
                    name=extract_title(text, project_dir.name) if text else project_dir.name,
                    rel_path=project_dir.relative_to(ROOT).as_posix(),
                    status=normalize_status(extract_field(text, "Status") or default_status) if text else default_status,
                    progress=parse_progress(extract_field(text, "Progress")) if text else None,
                    next_step=extract_field(text, "Next Step") if text else None,
                )
            )
    return items


def summarize(items: list[Item]) -> Summary:
    total = len(items)
    done = sum(1 for i in items if i.status == "done")
    in_progress = sum(1 for i in items if i.status == "in-progress")
    planned = sum(1 for i in items if i.status == "planned")
    unknown = total - done - in_progress - planned
    completion = int(round((done / total) * 100)) if total else 0
    return Summary(total, done, in_progress, planned, unknown, completion)


def format_progress(progress: int | None) -> str:
    return f"{progress}%" if progress is not None else "n/a"


def render_table(items: list[Item], include_next_step: bool = False) -> str:
    if include_next_step:
        header = "| Item | Status | Progress | Next Step | Path |\n|---|---|---:|---|---|"
        rows = [
            f"| {i.name} | {i.status} | {format_progress(i.progress)} | {i.next_step or 'n/a'} | `{i.rel_path}` |"
            for i in items
        ]
    else:
        header = "| Item | Status | Progress | Path |\n|---|---|---:|---|"
        rows = [
            f"| {i.name} | {i.status} | {format_progress(i.progress)} | `{i.rel_path}` |"
            for i in items
        ]
    if not rows:
        rows = ["| _No entries yet_ | n/a | n/a | n/a | n/a |" if include_next_step else "| _No entries yet_ | n/a | n/a | n/a |"]
    return "\n".join([header, *rows])


def main() -> None:
    courses = collect_courses()
    projects = collect_projects()

    course_summary = summarize(courses)
    project_summary = summarize(projects)

    content = "\n".join(
        [
            "# Progress Tracker",
            "",
            "_Auto-generated by `scripts/update_progress_tracker.py`._",
            "",
            "## Summary",
            "",
            "| Area | Total | Done | In Progress | Planned | Unknown | Completion |",
            "|---|---:|---:|---:|---:|---:|---:|",
            f"| Courses | {course_summary.total} | {course_summary.done} | {course_summary.in_progress} | {course_summary.planned} | {course_summary.unknown} | {course_summary.completion}% |",
            f"| Home Projects | {project_summary.total} | {project_summary.done} | {project_summary.in_progress} | {project_summary.planned} | {project_summary.unknown} | {project_summary.completion}% |",
            "",
            "## Courses",
            "",
            render_table(courses),
            "",
            "## Home Projects",
            "",
            render_table(projects, include_next_step=True),
            "",
            "> Update `Status:` and `Progress:` in course/project files to keep this tracker accurate.",
        ]
    )

    TRACKER_PATH.write_text(content + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
