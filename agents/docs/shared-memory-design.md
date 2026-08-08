# Shared Memory Design

## Goal

Give multiple AI assistants shared memory/storage about Brandon's homelab and projects, instead of each assistant holding its own disconnected context.

## Current pieces (outside this repo)

- **SharePoint site "CarterHomLab"** — shared file/document storage.
- **Notion workspace "Home Lab HQ"** — the source Brandon currently keeps profile/context notes in; this is where the memory summary folded into [`ai/profile.md`](../../ai/profile.md) came from (2026-08-08).

## In-repo equivalent

- [`agents/active/second-brain/`](../active/second-brain/) — research and notes assistants that capture and organize information into this repo.
- [`ai/profile.md`](../../ai/profile.md) — durable, versioned copy of Brandon's background and preferences, meant to be updated here going forward.

## Direction

This repo (`Carter-Home-Lab-Index`) is a candidate to become the durable, versioned layer of the shared-memory setup described above — per its own stated purpose as Brandon's "single source of truth." SharePoint/Notion can stay as authoring surfaces, but changes worth keeping long-term should land here.
