# Home Server

## Goal

Manage and document home server application projects, primarily Docker-based services.

Status: in-progress
Progress: 20%
Next Step: Finish migrating SSH key management from 1Password to Termius, then document each Pi's docker-compose stack.

## Hardware

| Device | Role |
|---|---|
| BED-Pi (Raspberry Pi 5) | General-purpose home server |
| BED-Zero (Pi Zero 2 W) | Pi-hole (DNS/ad-blocking) |
| Home Assistant Pi (separate Raspberry Pi) | Home Assistant |

## Network

- Router: ASUS GT-AXE11000, nicknamed "CarterRouter"
- Wi-Fi SSID: "The B.E.D. House"

## Access architecture

- `Azuera` (the "BadDragon" Windows desktop) is used as an SSH jump host into the homelab devices.
- Tailscale provides remote access outside the LAN.
- SSH key management is migrating from 1Password to Termius.

## Stack

- Docker / Docker Compose
- Linux (home server host)

## Projects

Add a subfolder per application (e.g., `nginx/`, `plex/`, `portainer/`) with its own `docker-compose.yml` and notes.
When ready, copy `personal-projects/assets/docker-compose-base.yml` as a starting point.
