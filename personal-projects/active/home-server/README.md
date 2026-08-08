# Home Server

## Goal

Manage and document the home lab: network, Raspberry Pi fleet, and the Docker-based service stack.

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

- **Network**: ASUS GT-AXE11000 router, flat `192.168.50.0/24` LAN, Bad-/BED- naming convention
- **BED-Pi** (Raspberry Pi 5, `192.168.50.201`): main server — Docker, Dockge, Caddy reverse proxy (`*.carterworkspace.com` via Cloudflare DNS-01), media automation (Prowlarr/Radarr/Sonarr/qBittorrent+Gluetun/Jellyfin), Wallos, Home Assistant OS (KVM/QEMU VM with Z-Wave passthrough)
- **BED-Zero** (Raspberry Pi Zero 2 W, `192.168.50.203`): whole-house Pi-hole DNS + Tailscale subnet router
- Tailscale (tailnet `100.64.0.0/10`), UFW + fail2ban on both Pis

## Context

Full technical context (device inventory, network topology, SSH architecture, per-service configs, hardening details) lives in [`context/`](context/):

- [`context/home-lab-hq-context.md`](context/home-lab-hq-context.md) — quick-reference summary (owner, network, naming, status)
- [`context/network-setup-export.md`](context/network-setup-export.md) — full export: device inventory, router config, SSH access, BED-Pi/BED-Zero builds, service stack, HAOS VM, open items

## Projects

Add a subfolder per application (e.g., `nginx/`, `plex/`, `portainer/`) with its own `docker-compose.yml` and notes.

When ready, copy `personal-projects/assets/docker-compose-base.yml` as a starting point.

## Open items

- Resolve the BadDragon/Azuera hostname collision before automating on hostnames
- Confirm the HAOS VM's final DHCP-assigned IP/reservation
- Confirm the 1Password → Termius SSH ID migration on both Pis
- Formalize a backup strategy (Wallos SQLite, Pi-hole Teleporter export, *arr-stack configs)
