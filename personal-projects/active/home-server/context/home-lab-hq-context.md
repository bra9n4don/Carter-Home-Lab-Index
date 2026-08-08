# Home Lab HQ — Quick Context for Claude

Brandon T Carter, Holly Springs NC. Intermediate Linux, advancing. Wants step-by-step instructions (one step at a time, wait for confirmation), runbooks/checklists over prose, reasoning behind commands, destructive ops flagged first, one change at a time with rollback awareness. Secrets live in 1Password only, never in chat/notes. SSH by key only.

**Network:**
- Router: ASUS GT-AXE11000 "CarterRouter". WAN: dynamic ISP IP, no port forwarding, firewall on.
- LAN: `192.168.50.0/24`, flat, no VLANs. DHCP `.2–.254`. Gateway/DNS fallback `192.168.50.1`; primary DNS `192.168.50.203` (BED-Zero).
- Wi-Fi: main SSID "The B.E.D. House" (2.4/5/6GHz); guest SSID "Carter 2.4 GHz" (isolated).
- Naming convention: "Bad-"/"BED-" prefix, "- Wifi" suffix for wireless interfaces (e.g. BadDragon / BadDragon - WiFi).
- Known hosts: CarterRouter `.1`, BED-Zero `.203` (LAN DNS, likely Pi Zero, unconfirmed), BED-Pi `.201` (role unconfirmed), BadDragon `.6` (Brandon's Windows desktop), BadCarterPrinter `.250`. 37 total DHCP reservations, only 8 named.
- Remote access: Termius (SSH, keys in 1Password) + Tailscale — but Tailscale isn't installed on BadDragon and its footprint elsewhere is unverified.

**Hardware/systems status:** Mostly undocumented still — no confirmed specs for the Pi fleet, the "repurposed laptop" home server, storage/TrueNAS, Home Assistant/Z-Wave, media server, or power/UPS. Don't assume detail exists beyond what's listed here.

**Done so far:**
- Decoded the router config export to document the network layout above (no secrets captured).
- Fixed BadDragon's stale DHCP reservation (MAC corrected).
- Formalized the Bad-/BED- naming convention.
- Opened an "Automation Host" project (blocking) to pick one always-on machine for future scheduled jobs — next step is SSHing into the laptop server and BED-Pi to capture specs.
- Decided API access (Anthropic/OpenAI/Perplexity) is for automation only, additive to existing chat subscriptions.

**Open next steps:** SSH into laptop server + BED-Pi for specs; confirm Tailscale footprint; identify remaining unnamed DHCP reservations; document Home Assistant/Z-Wave, storage, media, and power/UPS; confirm ISP/modem details.
