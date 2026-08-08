# Brandon Carter — Home Lab Network & Raspberry Pi Setup Export

**Purpose**: Full technical context export for import into another AI assistant (Claude). Compiled from Perplexity project history (project: "Learn Raspberry Pi") as of 2026-08-07.

**Location**: Holly Springs, NC. **Domain**: `carterworkspace.com` (Cloudflare-managed).

---

## 1. Device Inventory

| Device | Role | Hostname | Static IP | OS | Storage |
|---|---|---|---|---|---|
| Raspberry Pi 5 (8GB RAM) | Main home server | `BED-Pi` | `192.168.50.201` | Raspberry Pi OS Trixie (Debian 13) 64-bit, kernel `6.18.33+rpt-rpi-2712` | 256GB microSD (fallback/recovery) + 2× 512GB Micron 2400 NVMe (boot: `nvme0n1`, data: `nvme1n1` mounted at `/mnt/data`) |
| Raspberry Pi Zero 2 W | Network appliance (DNS + subnet router) | `BED-Zero` | `192.168.50.203` | Raspberry Pi OS Lite (Debian 13 Trixie) 64-bit | 64GB microSD, USB Ethernet (wired primary), Wi-Fi backup only |
| Windows PC | Controlled jump host for Perplexity Computer SSH access | `BadDragon` (Micro-Star International MS-7D33) | `.40` Ethernet / `.7` Wi-Fi on `192.168.50.0/24` (see §7 caveat) | Windows | — |
| Windows PC (secondary) | — | `Azuera` (Alienware Area-51 AAT2250) | Reported `192.168.50.16` in one session — **naming collision with BadDragon, see §7** | Windows | — |
| ASUS Router | Gateway / LAN | `GT-AXE11000` | `192.168.50.1` | Firmware `3.0.0.4.388_23969-g30dbb27` | — |

**Case/hardware note (BED-Pi)**: Argon ONE V5 **Dual M.2 NVMe** case. Both NVMe slots route through an **ASMedia ASM1182e Gen 2 PCIe packet switch** — PCIe is Gen 2 only, never enable `dtparam=pciex1_gen=3`. Argon PWR GaN 27W supply, Argon OLED module.

Both Pi hostnames were originally named by the user: `BED-Pi` and `BED-Zero`, with `admin` as the shared username on both (chosen knowingly despite it being a common attacker-guessed username — compensated with key-only SSH and strong hardening).

---

## 2. Network Topology & Addressing

- **LAN subnet**: `192.168.50.0/24`, gateway/router at `192.168.50.1`
- **Tailscale tailnet range**: `100.64.0.0/10` (standard CGNAT range — used in firewall rules instead of pinning specific tailnet IPs, since those can change)
- **BED-Pi**: `192.168.50.201`
- **BED-Zero**: `192.168.50.203` (serves DNS for the whole LAN)
- **DNS resolution flow**: Router hands out BED-Zero (`192.168.50.203`) as primary DNS via DHCP → Pi-hole (on BED-Zero) forwards upstream to Cloudflare `1.1.1.1` / Quad9 `9.9.9.9`
- **Reverse proxy domain**: `*.carterworkspace.com` — Caddy on BED-Pi issues real, publicly-trusted certificates via Cloudflare DNS-01, but records resolve only to LAN/Tailscale IPs (split-horizon DNS with public PKI — no inbound 80/443 exposure to the WAN)
- A known discrepancy exists between whether a stale forward was for port `433` or `443` (see §6) — worth re-verifying directly on the router.

---

## 3. ASUS GT-AXE11000 Router Configuration

### SSH access (operational since 2026-07-29)
- Endpoint: `192.168.50.1:2222` (LAN-only, not WAN-exposed)
- Username: `CarterRouter`
- Auth: key-only (password login disabled), dedicated **RSA** key (ED25519 was rejected by the router) with comment `perplexity-computer-router@baddragon`
- Settings: SSH LAN-only, port 2222, password login **No**, idle timeout 20 min, Telnet **No**
- Host key strictly pinned (fingerprint not retained in notes — re-verify and record it)
- WAN web admin intentionally **kept enabled** on **TCP 8443** (not disabled during hardening)

### 2026-07-29 optimization pass — changes applied
1. Removed stale WAN port forwards (TCP 80 and a second port — recorded inconsistently as either 433 or 443 in different notes) that pointed at `192.168.50.177` (a Deako smart-home device, not a Pi)
2. Disabled WPS
3. Changed 2.4GHz Wi-Fi from channel 2 (overlapping) to channel 1 at 20MHz
4. Verified afterward: BED-Pi, BED-Zero, Pi-hole DNS all operational; 58 DHCP clients seen; both AiMesh nodes re-synced to channel 1

### Explicitly preserved during optimization
SSIDs/passwords, Smart Connect, AiMesh, DHCP, Pi-hole, IPv6, VPN, SSH, QoS, hardware acceleration, all 5GHz/6GHz settings.

A rollback snapshot was saved locally at `C:\Perplexity-Pi-Control\router-preoptimization-2026-07-29.txt`.

---

## 4. SSH Access Architecture

### Two parallel SSH identities exist — worth reconciling
**A. User's own access (since June, via 1Password)**
- 1Password SSH Agent, ED25519 key titled **"Homelab Pis"** in the **Homelab** vault (a separate `Personal` vault holds an unrelated Zoho key)
- Agent config: `%LOCALAPPDATA%\1Password\config\ssh\agent.toml`; named pipe `\\.\pipe\openssh-ssh-agent`; Windows built-in ssh-agent service disabled to avoid conflicts
- Working SSH config at `C:\Users\Brandon\.ssh\config`:
  ```
  Host bedpi
      HostName 192.168.50.201
      User admin

  Host bedzero
      HostName 192.168.50.203
      User admin
  ```
  (Relies on the `SSH_AUTH_SOCK` env var rather than an `IdentityAgent` directive — the latter failed to resolve the named pipe through config and was removed.)
- Password SSH disabled via `/etc/ssh/sshd_config.d/99-hardening.conf` on both Pis; `admin` has non-interactive passwordless sudo on both.
- A migration from 1Password to **Termius SSH ID** was started 2026-07-29/08-02 but is **not confirmed complete** on either Pi — treat as in progress.

**B. Perplexity Computer's dedicated access (since 2026-07-27)**
- Local key/state folder: `C:\Perplexity-Pi-Control` on BadDragon (deliberately moved out of OneDrive-synced Documents so the private key never leaves the local disk)
- Dedicated **ED25519** key, comment `perplexity-computer@baddragon`, added to `~/.ssh/authorized_keys` on both Pis (`.ssh` mode 700, `authorized_keys` mode 600)
- BED-Pi's pinned host-key fingerprint: `SHA256:t1lrW/NH0IupWGSNd72gpv6QAEMBW733ij50MM2JE1k` (BED-Zero's fingerprint wasn't retained — worth re-capturing)
- Verified targets: `admin@192.168.50.201` (BED-Pi) and `admin@192.168.50.203` (BED-Zero), full passwordless sudo, no public exposure
- **Important**: despite being described as a "jump host" arrangement, there is **no `ProxyJump`/`ProxyCommand`/`HostKeyAlias` config anywhere** — Perplexity Computer operates BadDragon directly and makes direct SSH connections from it to each Pi. If you want a true SSH jump-host chain, that still needs to be built.

### Known issue: duplicate "Azuera" hostname
Two machines were both observed as `Azuera` in different sessions — one Perplexity-connected host at `192.168.50.16` (Realtek NIC), and the user's actual MSI/Killer-NIC desktop (the real `BadDragon`) at `192.168.50.40` (Ethernet) / `192.168.50.7` (Wi-Fi). This naming collision can break DHCP/MagicDNS assumptions and should be resolved (rename one device, or fix DHCP reservations) before building further automation on top of hostnames. Recommended DHCP reservation for BadDragon's real NIC: MAC `AC:B4:80:FE:19:2F` → `.40`. On the real BadDragon, OpenSSH listens on TCP 22, account `bra9n`, authorized keys at `C:\ProgramData\ssh\administrators_authorized_keys` (ACL restricted to Administrators + SYSTEM).

---

## 5. BED-Pi (Raspberry Pi 5) — Foundation Build

*(Phase 0 completed 2026-06-05, Phase 1 completed/revised 2026-06-06)*

- **EEPROM**: updated to `2026-05-26`; `BOOT_ORDER=0xf416` (NVMe → SD → USB) after migration
- **Time sync**: chrony (replaces systemd-timesyncd), timezone `America/New_York`
- **Firewall (UFW)**: deny-by-default incoming, allow outgoing. Final state: SSH restricted to LAN (`192.168.50.0/24`) + tailnet (`100.64.0.0/10`) only — the initial open `22/tcp` rule was removed after Tailscale came up. Additional ports opened over time: `443/tcp+udp` (Caddy, LAN+tailnet only), `41641/udp` (Tailscale), `7359/udp` + `1900/udp` (Jellyfin discovery/DLNA, LAN only). Port 53/80 are on BED-Zero, not BED-Pi.
- **fail2ban**: `jail.local` — bantime 24h, findtime 10m, maxretry 3, ignoreip includes LAN, backend systemd, sshd jail aggressive mode
- **unattended-upgrades**: Debian + Debian-Security + Raspberry Pi Foundation origins, auto-reboot at 04:00 daily (temporarily disabled during NVMe migrations, then re-enabled)
- **Argon ONE V5 case**: installed via `download.argon40.com/argonforty.sh` (also referenced elsewhere as `argon1v5.sh`), configured via `argonone-config` / `argon-config`. Fan curve settings: quiet-idle (55°C→10%, 60°C→55%, 65°C→100%) vs cooler (55°C→30%). OLED at I2C `0x3c` — **critical conflict**: a custom `bedpi-oled.service` and Argon's daemon cannot both drive `0x3c` simultaneously (blanks/garbles screen); only one may own it. Power button: single press = graceful shutdown, double = reboot, hold 3s = hard cut.

### NVMe (critical fixes — mandatory, not optional)
- The dual-NVMe board's ASMedia switch causes **write corruption on DRAM-less QLC drives** unless two fixes are applied:
  1. `nvme_core.default_ps_max_latency_us=0` appended to `/boot/firmware/cmdline.txt` (must remain a single line)
  2. `dtparam=pciex1_aspm=off` added to `/boot/firmware/config.txt`
- Without these, FAT/ext4 corruption and `TX stall` errors on eth0 occur and the OS will not survive on NVMe.
- `rpi-clone` does **not** work on this hardware (fails post-`mkfs` mount) — a manual `rsync` clone procedure was used instead (root via `rsync -axHAXv`, then boot firmware copied separately since `-x` skips the separately-mounted `/boot/firmware`).
- An 8GB write-integrity test (`dd` + `sha256sum` before/after cache drop) passed at ~290 MB/s after fixes.
- PCIe only initializes on a **cold boot** (full power removal) — a warm reboot won't enumerate a newly installed drive.

### Docker
- Installed from Docker's official repo (Trixie natively supported as of 2026-06)
- Data root relocated from `/var/lib/docker` to `/mnt/data/docker` (on the data NVMe) via `daemon.json` `data-root` override
- `admin` added to `docker` group

### Tailscale
- Installed, brought up as `bed-pi` in the existing tailnet
- UFW tightened afterward to LAN+tailnet-only SSH

---

## 6. BED-Zero (Raspberry Pi Zero 2 W) — DNS + Subnet Router

*(Drafted 2026-06-06, designed to run natively for RAM efficiency on 512MB)*

**Role**: whole-house DNS sinkhole (Pi-hole) + Tailscale subnet router. Deliberately kept separate from BED-Pi so DNS never goes down when BED-Pi is rebuilt.

- **Design decisions**: wired via USB Ethernet (not Wi-Fi, for DNS reliability); Pi-hole runs **natively** (not Docker) due to the 512MB RAM ceiling; Raspberry Pi OS Lite (headless); Wi-Fi kept only as an auto-connect-priority-lowered backup profile
- **Static IP**: `192.168.50.203/24` via NetworkManager (`nmcli`), gateway `192.168.50.1`, DNS `1.1.1.1`/`9.9.9.9`
- **UFW**: deny-by-default; SSH (22), DNS (53 tcp+udp), Pi-hole web UI (80) all restricted to LAN+tailnet only — **never** expose port 53 publicly (DDoS amplification risk)
- **fail2ban / unattended-upgrades**: same pattern as BED-Pi, but reboot time offset to 04:30 (30 min after BED-Pi's 04:00) so both boxes never reboot simultaneously
- **Tailscale**: brought up as `bed-zero` with `--advertise-routes=192.168.50.0/24 --accept-dns=false` (subnet router advertising the whole LAN to the tailnet; `--accept-dns=false` avoids DNS loop since BED-Zero is itself the DNS server). Route must be manually approved in the Tailscale admin console.
- **Pi-hole**: installed via official installer, admin password set via `pihole setpassword`, web UI at `http://192.168.50.203/admin`
- **DHCP cutover**: router's primary DNS set to `192.168.50.203` (BED-Zero) — deliberately **no** secondary public DNS configured, to avoid clients bypassing Pi-hole
- Single point of failure acknowledged: if BED-Zero goes down, house-wide DNS stops. Mitigation ideas noted but not yet implemented: router fallback DNS, or a second Pi-hole on BED-Pi (Docker) synced via Gravity Sync.

---

## 7. BED-Pi Service Stack (Phase 3, drafted 2026-07-27)

Built in this dependency order — filesystem layout, then Dockge, then Caddy, then Watchtower, then the media stack, then Wallos.

### A. Filesystem layout (single-root principle)
- `/mnt/data/appdata/{dockge,caddy,prowlarr,radarr,sonarr,gluetun,qbittorrent,jellyfin,wallos}` — per-service config/state
- `/mnt/data/stacks/{dockge,caddy,watchtower,media,wallos}` — Compose project files
- `/mnt/data/media/downloads/torrents/{movies,tv}`, `/mnt/data/media/movies`, `/mnt/data/media/tv` — **shared media root, mounted whole (never a subpath) into every container that touches it**, so Radarr/Sonarr can hardlink completed downloads into the library without duplicating bytes on disk. Mounting different subpaths per container silently breaks hardlinking and doubles disk usage during imports — this is the single most common *arr-stack misconfiguration.

### B. Dockge (orchestration UI)
- Port `5001` (corrects an earlier plan that assumed port 8080)
- Management-plane only — doesn't intercept traffic; stacks keep running if Dockge is removed
- Mounts the Docker socket (accepted trade-off for single-operator home lab behind UFW+Tailscale, not appropriate for multi-tenant/internet-exposed hosts)

### C. Caddy reverse proxy + Cloudflare DNS-01
- Custom-built Caddy image (via `xcaddy` + `caddy-dns/cloudflare` plugin) since the official image ships without DNS provider plugins
- DNS-01 challenge chosen over HTTP-01 specifically because it requires **no inbound port 80/443 exposure** and is the only type that supports wildcard certs
- Cloudflare API token scoped to `Zone.DNS:Edit` on `carterworkspace.com` only (not the Global API Key)
- All backends join a shared Docker bridge network `proxynet` (`docker network create proxynet`), so Caddy resolves them by container name
- Subdomains configured: `dockge`, `prowlarr`, `radarr`, `sonarr`, `qbittorrent` (→ `gluetun:8080`), `jellyfin`, `wallos`
- UFW: only `443/tcp` + `443/udp` (HTTP/3) opened, LAN+tailnet — this is the entire payoff of the reverse-proxy design (one firewall rule set instead of one per service)

### D. Watchtower (bounded auto-updates)
- Allow-list model: `WATCHTOWER_LABEL_ENABLE=true`, only containers labeled `com.centurylinklabs.watchtower.enable=true` get updated
- Runs nightly at 03:00 (offset from BED-Zero's 04:00/04:30 unattended-upgrades)
- Dockge is explicitly excluded (`enable=false`) so it's never mid-update during a deployment

### E. Media automation stack
Pipeline: **Prowlarr** (indexer aggregation) → **Radarr**/**Sonarr** → **qBittorrent** (inside **Gluetun** VPN network namespace) → completed downloads hardlinked into `/data/media/{movies,tv}` → **Jellyfin** indexes and streams.

- qBittorrent uses `network_mode: "service:gluetun"` — it shares Gluetun's network namespace entirely (no `eth0` of its own), guaranteeing zero non-VPN egress at the kernel level, not just a firewall rule
- Gluetun's `FIREWALL_OUTBOUND_SUBNETS` must include both the `proxynet` Docker bridge subnet and the LAN subnet, or Radarr/Sonarr callbacks to qBittorrent silently fail
- **Kill-switch verification is mandatory before use**: `docker exec qbittorrent wget -qO- https://ipinfo.io/ip` must return the VPN exit IP, never the home WAN IP
- **Known Raspberry Pi 5 hardware limitation**: no hardware video encoder exists on the Pi 5, and Jellyfin has deprecated V4L2 hardware acceleration for this reason with no planned fix. Direct Play/Direct Stream are fine; actual transcoding runs on CPU only and struggles above one concurrent 1080p transcode. Plan library formats (prefer H.264) around this.
- UFW: only Jellyfin's two non-proxyable UDP discovery ports (`7359` LAN discovery, `1900` DLNA) are opened directly — everything else routes through Caddy's `443`
- Legal/acceptable-use note baked into the runbook: this stack is content-source-agnostic; the user is responsible for using legal indexer sources.

### F. Wallos (subscription-fee tracker)
- Standalone PHP/SQLite app tracking recurring payments (Netflix, Disney+, Hulu, Spotify, etc.) — chosen specifically to give cost visibility now that Jellyfin provides a self-hosted alternative
- State lives entirely in `/mnt/data/appdata/wallos/db` (SQLite) — flagged as backup-critical, and backup strategy is **not yet formalized** across this whole project

---

## 8. Home Assistant OS on BED-Pi (KVM/QEMU/libvirt) — Completed

- **Hypervisor setup**: `libvirt-daemon-system libvirt-clients bridge-utils virtinst` installed; `admin` added to `libvirt` + `kvm` groups; default libvirt network started and set to autostart
- **HAOS image**: generic AArch64 QCOW2 release 15.2 (`haos_generic-aarch64-15.2.qcow2`), stored at `/mnt/data/haos/` on the data NVMe, disk expanded +32G via `qemu-img resize`
- **VM definition** (`virt-install`): name `haos`, 2 vCPUs, 2048 MiB RAM, disk imported as SCSI behind `virtio-scsi`, UEFI boot (secure boot disabled), no graphical console, autostart enabled (`virsh autostart haos`)
- **Networking**: two vNICs — one on the libvirt `default` NAT network, one direct-attached to `eth0` in bridge mode (macvtap-style), MAC `52:54:00:4a:19:02`. A DHCP reservation for that MAC was recommended but not confirmed as completed — the VM's actual LAN IP was never recorded (use `virsh domifaddr haos` or `homeassistant.local:8123` to find it).
- **Z-Wave passthrough**: Nabu Casa **Connect ZWA-2** USB stick (VID:PID `303a:4001`) passed through via persistent hostdev XML at `/mnt/data/haos/zwa2-usb.xml`; confirmed present in `virsh dumpxml haos`. HA onboarding completed and the Z-Wave network is reported set up.
- **Not yet confirmed**: HA's Google-Drive backup add-on installation/configuration, and the VM's final DHCP-assigned IP/reservation.

---

## 9. Open Items / Things Worth Re-Verifying

- **Router forwarded port discrepancy**: notes disagree on whether the stale forward removed on 2026-07-29 was TCP `433` or `443` (target was `192.168.50.177`, a Deako device) — check the router's current port-forwarding page directly.
- **BadDragon/Azuera naming collision**: two Windows machines were both observed under the name "Azuera" in different sessions; resolve which is the real jump host (`192.168.50.40`/`.7`, Killer NIC, user `bra9n`) before building further automation on hostnames.
- **No true SSH ProxyJump chain exists** — the "jump host" pattern is currently just Perplexity Computer operating BadDragon directly and SSHing from there; if a real jump-host chain (e.g., external → BadDragon → Pi) is wanted, it still needs to be configured.
- **1Password → Termius SSH ID migration** (started 2026-07-29/08-02) is not confirmed complete on either Pi.
- **BED-Zero's SSH host-key fingerprint** for the Perplexity Computer key was never captured (BED-Pi's was: `SHA256:t1lrW/NH0IupWGSNd72gpv6QAEMBW733ij50MM2JE1k`).
- **HAOS VM's final IP/DHCP reservation** and Google Drive backup add-on status are unconfirmed.
- **No unified backup strategy** exists yet across Wallos's SQLite DB, Pi-hole's Teleporter export, or the *arr-stack configs — flagged in multiple runbooks as not yet formalized.
- **Second Pi-hole for DNS redundancy** (e.g., Dockerized on BED-Pi, synced via Gravity Sync) is only a documented idea, not implemented.

---

*Compiled from Perplexity Computer project history ("Learn Raspberry Pi" project), covering sessions from 2026-06-01 through 2026-08-07.*
