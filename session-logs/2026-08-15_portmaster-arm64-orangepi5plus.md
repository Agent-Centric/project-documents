# Safing Portmaster v1 — ARM64 Install Session Log
**Date:** 2026-08-15
**System:** Orange Pi 5 Plus (`orangepi5plus`) · Orange Pi 1.2.0 Jammy · Ubuntu 22.04.5 LTS · aarch64
**Print record:** [Portmaster-ARM64-Install-Record.pdf](../Portmaster-ARM64-Install-Record.pdf)

## Summary
Portmaster was not installed. The official Portmaster v2 Ubuntu `.deb` is amd64-only and cannot run on this Rockchip RK3588 board. Installed Safing’s published **linux_arm64 Portmaster v1** stack with the official installer, started the core service, and launched the desktop UI.

## What was already on the box
- No `portmaster` package, binary, or systemd unit
- Leftover `Portmaster_2.1.19_amd64.deb` in user Trash (wrong architecture)
- Kernel `6.1.43-rockchip-rk3588` (meets Safing’s 5.7+ recommendation)
- NetworkManager and systemd-resolved active
- XFCE on `DISPLAY=:0.0`
- GTK 3 / WebKitGTK / Ayatana AppIndicator already present

## Why official v2 failed
| Attempt | Result |
|---|---|
| `Portmaster_2.2.1_amd64.deb` | HTTP 200, architecture amd64 — will not install |
| `linux_arm64/packages/…arm64.deb` | HTTP 404 — no v2 ARM package |
| GitHub issue `#2038` | Closed as not planned |
| `install.sh` auto-detect | Matches `uname -m` to `x86_64` or `arm64`; Linux reports `aarch64` |

ARM64 v1 binaries **do** exist on `updates.safing.io` (`portmaster-start` 1.6.0, `portmaster-core` 1.6.10, app 0.2.8, notifier 0.3.6). Confirmed with `file` as AArch64 ELF.

## Install that worked
```bash
curl -fsSL https://updates.safing.io/latest/linux_all/packages/install.sh \
  -o /tmp/portmaster-install.sh

pkexec bash /tmp/portmaster-install.sh --arch arm64
pkexec systemctl daemon-reload
pkexec systemctl start portmaster.service

/opt/safing/portmaster/portmaster-start app --data=/opt/safing/portmaster
```

`--arch arm64` is required. Without it the official script rejects `aarch64`.

## Verification (15 Aug 2026, 14:43 MST)
- `portmaster.service` — **active (running)** and **enabled** at boot
- Core: `/opt/safing/portmaster/updates/linux_arm64/core/portmaster-core_v1-6-10`
- UI and notifier running as user `orangepi`
- Local API listening on `127.0.0.1:817`
- Launchers: `/usr/share/applications/portmaster.desktop`
- DNS and ping to `1.1.1.1` still worked after start

## Known caveats
- This is Portmaster **v1**, not v2. SPN login is still in the app.
- Vendor kernel has **no BTF**. eBPF extras fail with `no BTF found for kernel version 6.1.43-rockchip-rk3588`. Interception falls back to nfqueue.
- Filter lists take a few minutes to load on first start.
- Safing’s installer recommends a reboot; the service started cleanly without one.

## SPN login
Portmaster itself needs no account. Sign in to the paid Safing Privacy Network inside the running app (SPN panel). Do not put account passwords in this repo.

## Day-to-day
```bash
systemctl status portmaster.service
sudo systemctl start|stop|restart portmaster.service
journalctl -u portmaster.service -f
/opt/safing/portmaster/portmaster-start app --data=/opt/safing/portmaster
sudo /opt/safing/portmaster/portmaster-start update --data=/opt/safing/portmaster
sudo /opt/safing/portmaster/portmaster-start recover-iptables
```

Watch existing listeners when prompts appear: SSH `:22`, plus `5050`, `30001–30005`, `30104`.

## Result
Boot-persistent Portmaster v1 on RK3588 ARM64, using official Safing ARM binaries. Printable field record regenerated with `build_portmaster_record.py`.
