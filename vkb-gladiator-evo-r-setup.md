# VKBsim Gladiator EVO R — Linux Setup Guide

## Device Info
- **Model:** VKBsim Gladiator EVO R
- **Vendor/Product ID:** 231d:0200
- **Device node:** `/dev/input/js0`
- **Stable path:** `/dev/input/by-id/usb-VKB-Sim__C__Alex_Oz_2023_VKBsim_Gladiator_EVO_R-joystick`
- **Event device:** `/dev/input/by-id/usb-VKB-Sim__C__Alex_Oz_2023_VKBsim_Gladiator_EVO_R-event-joystick`
- **OS:** Zorin OS (Linux)
- **Date configured:** 2026-05-01

## Installed Packages
```bash
sudo apt install joystick jstest-gtk evtest
```
- `joystick` — provides `jscal` for calibration
- `jstest-gtk` — GUI for visually testing axes and buttons
- `evtest` — low-level input event debugging

## Axes Layout (10 axes, 80 buttons)
| Axis   | Function   | Range    | Resting Value |
|--------|------------|----------|---------------|
| ABS_X  | Roll       | 0–4095   | 2048          |
| ABS_Y  | Pitch      | 0–4095   | 2048          |
| ABS_Z  | Twist      | 0–2047   | 933           |
| ABS_RX | Mini-X     | 0–4095   | 2048          |
| ABS_RY | Mini-Y     | 0–4095   | 2048          |
| ABS_RZ | Dial       | 0–2047   | 1122          |
| THROT  | Throttle   | 0–2047   | 1024          |
| RUDDER | Rudder     | 0–2047   | 1024          |
| HAT0X  | Hat X      | -1–1     | 0             |
| HAT0Y  | Hat Y      | -1–1     | 0             |

## Calibration

### Run calibration
```bash
jscal -c /dev/input/js0
```
Follow the interactive prompts to move each axis to its minimum, center, and maximum positions.

### View current calibration
```bash
jscal -p /dev/input/js0
```

### Current calibration string
```
jscal -s 10,1,3553,2037,2037,-2147483648,-264460,1,4075,0,0,-2147483648,-2147483648,1,0,933,933,-2147483648,-2147483648,1,0,2057,2057,-2147483648,-2147483648,1,0,2042,2042,-2147483648,-2147483648,1,50,1123,1124,-536854528,-536854528,1,0,1024,1024,-2147483648,-2147483648,1,0,1024,1024,-2147483648,-2147483648,1,0,0,0,-2147483648,-2147483648,1,0,0,0,-2147483648,-2147483648 /dev/input/js0
```

## Persistent Configuration

### Calibration script
**Location:** `/usr/local/bin/vkb-gladiator-cal.sh`

Applies the saved calibration. To update after recalibrating:
```bash
jscal -c /dev/input/js0          # recalibrate
NEW_CAL=$(jscal -p /dev/input/js0)
sudo tee /usr/local/bin/vkb-gladiator-cal.sh > /dev/null <<EOF
#!/bin/bash
$NEW_CAL
EOF
sudo chmod +x /usr/local/bin/vkb-gladiator-cal.sh
```

### udev rule
**Location:** `/etc/udev/rules.d/99-vkb-gladiator-cal.rules`

```
ACTION=="add", ATTRS{idVendor}=="231d", ATTRS{idProduct}=="0200", RUN+="/usr/local/bin/vkb-gladiator-cal.sh"
```

Automatically applies calibration when the joystick is plugged in. After editing, reload with:
```bash
sudo udevadm control --reload-rules
```

## Testing & Troubleshooting

### GUI test
```bash
jstest-gtk
```
Select the device → Properties → verify axes and buttons live.

### CLI event test (check for drift/jitter)
```bash
evtest /dev/input/by-id/usb-VKB-Sim__C__Alex_Oz_2023_VKBsim_Gladiator_EVO_R-event-joystick
```
Leave the stick untouched — no events should fire if stable.

### Verify device is detected
```bash
lsusb | grep 231d
cat /proc/bus/input/devices | grep -A5 "VKB"
```

### Reset calibration to defaults
```bash
jscal -s 10,0,0,0,0,0,0,0,0,0,0 /dev/input/js0
```

## Notes
- VKB firmware configuration (profiles, curves, deadzones) requires **VKBDevCfg** (Windows only). Settings persist on the device hardware.
- Compatible games on this system: DCS World, War Thunder (via Steam/Proton).
