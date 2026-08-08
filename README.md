# Carter Home Lab Index

Umbrella home-lab index for **agent development**, **learning courses**, and **personal projects**.

## Structure

| Folder | Purpose |
|---|---|
| `agents/` | Agent prompts, workflows, configs, and docs |
| `learning/` | Courses, notes, resources, and cert prep |
| `personal-projects/` | Personal builds and experiments |
| `ai/` | AI instructions and shared prompts for Copilot/agents |

## AI guidance

The `ai/` folder contains repo-specific instructions for Copilot and other agents.
See [`ai/instructions.md`](ai/instructions.md) for the operating rules.

## Progress tracking

- Repo-wide progress is tracked in [`progress-tracker.md`](progress-tracker.md).
- It auto-syncs via [`.github/workflows/sync-progress-tracker.yml`](.github/workflows/sync-progress-tracker.yml).

---

## 📌 Quick Start

1. Choose a workspace:
   - 🤖 [`agents/`](agents/)
   - 📚 [`learning/`](learning/)
   - 🛠️ [`personal-projects/`](personal-projects/)
2. Read that area's `README.md` for the subfolder layout.
3. Add or update the local README in that area.
4. Move active work into the correct subfolder (`active/`, `courses/`, etc.).
5. Commit changes with a clear message:
   - `feat(agents): ...`
   - `docs(learning): ...`
   - `chore(projects): ...`

---

## 🔗 Future Dedicated Repositories (Placeholders)

> Replace these with real repo links when you split work into standalone repositories.

- **Agents Hub:** `https://github.com/bra9n4don/<agents-repo>`
- **Learning Hub:** `https://github.com/bra9n4don/<learning-repo>`
- **Personal Projects Hub:** `https://github.com/bra9n4don/<personal-projects-repo>`

Optional extras:
- **Course Notes Repo:** `https://github.com/bra9n4don/<course-notes-repo>`
- **Project Portfolio Repo:** `https://github.com/bra9n4don/<portfolio-repo>`

---

## 🔭 Purpose

This repository is my single source of truth for organizing and navigating:

- 🤖 Agent work (build, iterate, document)
- 📚 Learning work (courses, notes, certifications)
- 🛠️ Personal projects (ideas, active builds, completed work)

---

## 🗂️ Workspace Map

### 🤖 Agents
- [`agents/`](agents/) — agent workspace home
- [`agents/active/`](agents/active/) — currently active agents
- [`agents/templates/`](agents/templates/) — reusable agent templates and scaffolds
- [`agents/archive/`](agents/archive/) — retired/deprecated agents
- [`agents/docs/`](agents/docs/) — runbooks, standards, design notes

### 📚 Learning
- [`learning/`](learning/) — learning workspace home
- [`learning/courses/`](learning/courses/) — course materials and tracks
- [`learning/notes/`](learning/notes/) — summaries, notes, takeaways
- [`learning/resources/`](learning/resources/) — references and links
- [`learning/certifications/`](learning/certifications/) — cert prep and completion artifacts

### 🛠️ Personal Projects
- [`personal-projects/`](personal-projects/) — personal projects workspace home
- [`personal-projects/ideas/`](personal-projects/ideas/) — brainstorms and proposals
- [`personal-projects/active/`](personal-projects/active/) — in-progress projects
- [`personal-projects/completed/`](personal-projects/completed/) — finished projects + retros
- [`personal-projects/assets/`](personal-projects/assets/) — shared files/assets

---

## ✅ Operating Rhythm (Simple)

- **Personal projects:** capture in `ideas/`, move work to `active/`, then to `completed/`
- **Agents:** build in `active/`, keep design notes in `docs/`, then move retired agents to `archive/`
- **Learning:** organize work under `courses/`, `notes/`, `resources/`, or `certifications/` as appropriate
- Document organizational changes in the relevant local README or docs

---

## 🚀 Next Up

- Add project boards or issue templates per workspace
- Add links to any dedicated repos for larger builds
- Add progress snapshots (weekly/monthly)

---

## 👤 Owner

Maintained by **Brandon Carter**.
