# VoceChat v0.9.3 — Installation Session Log
**Date:** 2026-05-04
**System:** Zorin OS 18 (x86_64)

## Summary
Installed VoceChat desktop client v0.9.3 from the official GitHub release page.

## Steps Performed

### 1. Download
Downloaded the `.deb` package from the GitHub release:
```
https://github.com/Privoce/vocechat-desktop/releases/tag/v0.9.3
```
File: `VoceChat_0.9.3_amd64.deb` (~75 MB)

### 2. Installation
Installed via `apt`:
```bash
sudo apt install -y /tmp/VoceChat_0.9.3_amd64.deb
```
Deployed to `/opt/VoceChat/`, binary symlinked at `/usr/bin/vocechat`.

### 3. Desktop Shortcut
Copied the system `.desktop` file to the user desktop:
```
~/Desktop/VoceChat.desktop
```

### 4. Autostart Configuration
Copied `.desktop` entry to autostart directory:
```
~/.config/autostart/vocechat.desktop
```
Validated with `desktop-file-validate` — no errors.

### 5. Verification
- Process confirmed running (main PID: 182837) with all Electron sub-processes healthy
- User data directory populated: `~/.config/VoceChat/`
- Autostart entry validated and confirmed

### 6. Cleanup
Removed temporary files:
- `/tmp/VoceChat_0.9.3_amd64.deb`
- `/tmp/vocechat.log`

## Result
VoceChat v0.9.3 is fully installed, stable, and configured to autostart on login.
