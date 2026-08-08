# Home Server

## Goal

Manage and document the home lab: network, Raspberry Pi fleet, and the Docker-based service stack.

Status: in-progress

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

## Open items

- Resolve the BadDragon/Azuera hostname collision before automating on hostnames
- Confirm the HAOS VM's final DHCP-assigned IP/reservation
- Confirm the 1Password → Termius SSH ID migration on both Pis
- Formalize a backup strategy (Wallos SQLite, Pi-hole Teleporter export, *arr-stack configs)

Next Step: SSH into BED-Pi and BED-Zero to confirm/capture full hardware specs, and resolve the BadDragon/Azuera naming collision.
