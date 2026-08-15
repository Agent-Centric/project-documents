#!/usr/bin/env python3
"""Print-ready field record of the Portmaster ARM64 install on orangepi5plus."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Flowable,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(TTFont("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-Bold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-Italic", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-BoldItalic", "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Italic", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibMono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibMono-Bold", "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"))

NAVY = colors.HexColor("#1B2A4A")
TEAL = colors.HexColor("#1F6B5A")
TEAL_SOFT = colors.HexColor("#E6F1ED")
SLATE = colors.HexColor("#334155")
INK = colors.HexColor("#1E293B")
MUTED = colors.HexColor("#64748B")
RULE = colors.HexColor("#CBD5E1")
ROW_ALT = colors.HexColor("#F8FAFC")
HEADER_BG = colors.HexColor("#1B2A4A")
AMBER_BG = colors.HexColor("#FFF7ED")
AMBER = colors.HexColor("#9A3412")
PAPER = colors.white

PAGE_W, PAGE_H = letter
LEFT = 0.7 * inch
RIGHT = 0.7 * inch
TOP = 0.85 * inch
BOTTOM = 0.7 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

OUT = "/home/orangepi/Documents/Portmaster-ARM64-Install-Record.pdf"


class AccentBar(Flowable):
    def __init__(self, width, height=5, color=TEAL):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 1.5, stroke=0, fill=1)


class ColorBand(Flowable):
    def __init__(self, width, height, fill, text="", text_color=colors.white, font="LibSans-Bold", size=8.5):
        super().__init__()
        self.width = width
        self.height = height
        self.fill = fill
        self.text = text
        self.text_color = text_color
        self.font = font
        self.size = size

    def draw(self):
        self.canv.setFillColor(self.fill)
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont(self.font, self.size)
            self.canv.drawString(10, (self.height - self.size) / 2 + 0.5, self.text)


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["kicker"] = ParagraphStyle(
        "kicker",
        fontName="LibSans-Bold",
        fontSize=8.5,
        leading=11,
        textColor=TEAL,
        letterSpacing=1.2,
        spaceAfter=4,
    )
    s["title"] = ParagraphStyle(
        "title",
        fontName="LibSerif-Bold",
        fontSize=22,
        leading=26,
        textColor=NAVY,
        spaceAfter=6,
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle",
        fontName="LibSerif-Italic",
        fontSize=11,
        leading=15,
        textColor=SLATE,
        spaceAfter=10,
    )
    s["meta"] = ParagraphStyle(
        "meta",
        fontName="LibSans",
        fontSize=8.5,
        leading=12,
        textColor=MUTED,
        spaceAfter=2,
    )
    s["h1"] = ParagraphStyle(
        "h1",
        fontName="LibSans-Bold",
        fontSize=12.5,
        leading=16,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        fontName="LibSans-Bold",
        fontSize=10.5,
        leading=14,
        textColor=TEAL,
        spaceBefore=10,
        spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body",
        fontName="LibSerif",
        fontSize=10,
        leading=14,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=7,
    )
    s["bodyleft"] = ParagraphStyle(
        "bodyleft",
        parent=s["body"],
        alignment=TA_LEFT,
    )
    s["note"] = ParagraphStyle(
        "note",
        fontName="LibSerif-Italic",
        fontSize=9.5,
        leading=13,
        textColor=AMBER,
        spaceAfter=8,
    )
    s["th"] = ParagraphStyle(
        "th",
        fontName="LibSans-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.white,
    )
    s["td"] = ParagraphStyle(
        "td",
        fontName="LibSans",
        fontSize=8.5,
        leading=11.5,
        textColor=INK,
    )
    s["tdmono"] = ParagraphStyle(
        "tdmono",
        fontName="LibMono",
        fontSize=7.4,
        leading=10.5,
        textColor=NAVY,
    )
    s["tdbold"] = ParagraphStyle(
        "tdbold",
        fontName="LibSans-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=NAVY,
    )
    s["cmd"] = ParagraphStyle(
        "cmd",
        fontName="LibMono",
        fontSize=7.6,
        leading=11,
        textColor=NAVY,
        backColor=TEAL_SOFT,
        leftIndent=6,
        rightIndent=6,
        spaceBefore=2,
        spaceAfter=2,
        borderPadding=4,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        fontName="LibSerif",
        fontSize=10,
        leading=13.5,
        textColor=INK,
        leftIndent=12,
        spaceAfter=3,
    )
    s["footer"] = ParagraphStyle(
        "footer",
        fontName="LibSans",
        fontSize=8,
        leading=10,
        textColor=MUTED,
    )
    s["caption"] = ParagraphStyle(
        "caption",
        fontName="LibSans-Italic",
        fontSize=8,
        leading=11,
        textColor=MUTED,
        spaceAfter=8,
        spaceBefore=2,
    )
    return s


def kv_table(rows, col1=1.7 * inch, col2=None, s=None):
    if col2 is None:
        col2 = CONTENT_W - col1
    data = []
    for k, v, mono in rows:
        data.append(
            [
                Paragraph(k, s["tdbold"]),
                Paragraph(v, s["tdmono"] if mono else s["td"]),
            ]
        )
    t = Table(data, colWidths=[col1, col2], hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("BACKGROUND", (0, 0), (0, -1), TEAL_SOFT),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
    ]
    for i in range(len(data)):
        if i % 2 == 1:
            cmds.append(("BACKGROUND", (1, i), (1, i), ROW_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def grid(headers, rows, widths, s):
    head = [Paragraph(h, s["th"]) for h in headers]
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            style = s["tdmono"] if i == len(row) - 1 or i == 1 else s["td"]
            if i == 0:
                style = s["tdbold"]
            cells.append(Paragraph(cell, style))
        body.append(cells)
    t = Table([head] + body, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body, s):
    inner = [
        [
            Paragraph(f"<b>{title}</b>", ParagraphStyle("ct", parent=s["tdbold"], textColor=AMBER)),
        ],
        [Paragraph(body, ParagraphStyle("cb", parent=s["td"], textColor=INK, leading=12))],
    ]
    t = Table(inner, colWidths=[CONTENT_W], hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#FDBA74")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 8),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    # top rule
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 0.32 * inch, PAGE_W, 0.32 * inch, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 0.38 * inch, PAGE_W, 0.06 * inch, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("LibSans", 8)
    canvas.drawString(LEFT, PAGE_H - 0.22 * inch, "SAFING PORTMASTER  ·  ARM64 FIELD RECORD")
    canvas.setFont("LibSans", 8)
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 0.22 * inch, "orangepi5plus  ·  15 August 2026")

    # footer
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 0.38 * inch, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0.38 * inch, PAGE_W, 0.045 * inch, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#E2E8F0"))
    canvas.setFont("LibSans", 8)
    canvas.drawString(LEFT, 0.16 * inch, "Internal operations record  ·  not a Safing official document")
    canvas.setFont("LibSans-Bold", 8)
    canvas.drawRightString(PAGE_W - RIGHT, 0.16 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    story = []

    story.append(Paragraph("OPERATIONS RECORD  ·  PRIVACY SUITE", s["kicker"]))
    story.append(Paragraph("Getting Portmaster Working on Orange Pi 5 Plus", s["title"]))
    story.append(
        Paragraph(
            "How the official x86 installer failed on this ARM board, and how Safing’s published linux_arm64 v1 stack was installed, started, and verified.",
            s["subtitle"],
        )
    )
    story.append(AccentBar(CONTENT_W, 4))
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Prepared 15 August 2026 on host <b>orangepi5plus</b>. Portmaster is a free, open-source application firewall from Safing "
            "(safing.io). The paid Safing Privacy Network (SPN) logs in after the core is running. This record is written so the work "
            "can be reprinted, handed to another operator, or used to rebuild the install.",
            s["body"],
        )
    )

    story.append(Paragraph("1.  Machine as found", s["h1"]))
    story.append(
        Paragraph(
            "Before any install, the box was checked for packages, binaries, systemd units, and leftover downloads. "
            "Portmaster was not installed. A discarded official v2 Debian package was already in the user Trash — "
            "evidence of an earlier attempt with the wrong CPU architecture.",
            s["body"],
        )
    )
    story.append(
        kv_table(
            [
                ("Host", "orangepi5plus", True),
                ("Board", "Orange Pi 5 Plus  ·  Rockchip RK3588", False),
                ("OS", "Orange Pi 1.2.0 Jammy  ·  Ubuntu 22.04.5 LTS", False),
                ("Kernel", "6.1.43-rockchip-rk3588  (Linux 5.7+ required; this kernel qualifies)", True),
                ("CPU / dpkg arch", "aarch64  ·  arm64", True),
                ("Desktop", "XFCE on DISPLAY=:0.0", False),
                ("Network stack", "NetworkManager active  ·  systemd-resolved active", False),
                ("Sudo", "User orangepi is in group sudo  (password required)", False),
            ],
            s=s,
        )
    )
    story.append(Paragraph("Table 1. Host identity at the time of install.", s["caption"]))

    story.append(Paragraph("2.  Why the official download would not install", s["h1"]))
    story.append(
        Paragraph(
            "Safing’s current desktop product is Portmaster v2. The public download page only ships 64-bit Intel/AMD packages. "
            "On this board, <font face='LibMono'>uname -m</font> is <font face='LibMono'>aarch64</font>. An amd64 .deb cannot execute here.",
            s["body"],
        )
    )
    story.append(
        grid(
            ["What we tried", "Result", "Why"],
            [
                [
                    "Official v2 Ubuntu package<br/>Portmaster_2.2.1_amd64.deb",
                    "HTTP 200, but wrong CPU",
                    "Architecture: amd64. Will not install on arm64.",
                ],
                [
                    "Leftover local file in Trash<br/>Portmaster_2.1.19_amd64.deb",
                    "Present, unused",
                    "Same architecture mismatch from an earlier download.",
                ],
                [
                    "v2 ARM URL<br/>linux_arm64/packages/…arm64.deb",
                    "HTTP 404",
                    "Safing does not publish a v2 .deb for ARM.",
                ],
                [
                    "GitHub issue #2038<br/>ARM64 / AARCH64 (v1 and v2)",
                    "Closed as not planned",
                    "Confirms official ARM desktop v2 is not on the roadmap.",
                ],
                [
                    "install.sh auto-detect",
                    "Would reject this board",
                    "Script matches uname -m to x86_64 or arm64. Linux reports aarch64.",
                ],
            ],
            [2.35 * inch, 1.7 * inch, CONTENT_W - 4.05 * inch],
            s,
        )
    )
    story.append(Paragraph("Table 2. Dead ends on the official v2 path.", s["caption"]))
    story.append(
        Paragraph(
            "The installer script does contain an <font face='LibMono'>arm64</font> case, but it never sees it on Linux ARM because "
            "the kernel reports <font face='LibMono'>aarch64</font>, not <font face='LibMono'>arm64</font>. Passing "
            "<font face='LibMono'>--arch arm64</font> is required.",
            s["body"],
        )
    )

    story.append(Paragraph("3.  What actually exists for ARM64", s["h1"]))
    story.append(
        Paragraph(
            "Safing’s update index still publishes a complete <b>Portmaster v1</b> linux_arm64 set. Those binaries were downloaded "
            "and checked with <font face='LibMono'>file</font> before install: they are real AArch64 ELF executables, not x86 "
            "binaries in disguise. Desktop libraries needed by the Electron UI were already on the board "
            "(GTK 3, WebKitGTK, Ayatana AppIndicator).",
            s["body"],
        )
    )
    story.append(
        grid(
            ["Component", "Version", "Verified as"],
            [
                ["portmaster-start", "1.6.0", "ELF 64-bit LSB, ARM aarch64, Go 1.21.2"],
                ["portmaster-core", "1.6.10", "ELF 64-bit LSB, ARM aarch64, statically linked"],
                ["portmaster-app", "0.2.8", "ELF 64-bit LSB pie, ARM aarch64 (Electron)"],
                ["portmaster-notifier", "0.3.6", "linux_arm64 signed update"],
                ["Filter / GeoIP intel", "2025–2026 lists", "Downloaded during first update"],
            ],
            [2.1 * inch, 1.4 * inch, CONTENT_W - 3.5 * inch],
            s,
        )
    )
    story.append(Paragraph("Table 3. ARM64 artifacts that were installed.", s["caption"]))

    story.append(Paragraph("4.  Install that worked", s["h1"]))
    story.append(
        Paragraph(
            "The official Safing installer script was used — not a third-party package and not a from-source build. "
            "Root was obtained with <font face='LibMono'>pkexec</font> so a desktop password dialog could appear on XFCE. "
            "Architecture was forced because auto-detect would have failed.",
            s["body"],
        )
    )
    story.append(Paragraph("Official installer, ARM override:", s["h2"]))
    story.append(
        Paragraph(
            "curl -fsSL https://updates.safing.io/latest/linux_all/packages/install.sh -o /tmp/portmaster-install.sh",
            s["cmd"],
        )
    )
    story.append(
        Paragraph(
            "pkexec bash /tmp/portmaster-install.sh --arch arm64",
            s["cmd"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        Paragraph(
            "The script wrote files to <font face='LibMono'>/opt/safing/portmaster</font>, installed icons, added desktop launchers, "
            "and enabled <font face='LibMono'>portmaster.service</font> for boot. It then pulled every signed module "
            "(core, app, notifier, intel lists). That download ran several minutes and finished with:",
            s["body"],
        )
    )
    story.append(Paragraph("Portmaster is now installed.  Please restart your device to start Portmaster", s["cmd"]))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "A full reboot was not required to bring the core up. The service was started immediately so SPN login could happen the same afternoon:",
            s["body"],
        )
    )
    story.append(Paragraph("pkexec systemctl daemon-reload &amp;&amp; pkexec systemctl start portmaster.service", s["cmd"]))
    story.append(
        Paragraph(
            "/opt/safing/portmaster/portmaster-start app --data=/opt/safing/portmaster",
            s["cmd"],
        )
    )

    state_block = [
        Paragraph("5.  State after install  (verified 15 Aug 2026, 14:43 MST)", s["h1"]),
        kv_table(
            [
                ("Service", "portmaster.service  ·  active (running)  ·  enabled at boot", True),
                ("Core PID", "root  ·  /opt/safing/portmaster/updates/linux_arm64/core/portmaster-core_v1-6-10", True),
                ("App", "User orangepi  ·  Portmaster UI running on XFCE", False),
                ("Notifier", "User session notifier running", False),
                ("Local API", "127.0.0.1:817  (UI talks to the core here)", True),
                ("Install root", "/opt/safing/portmaster", True),
                ("Launchers", "/usr/share/applications/portmaster.desktop", True),
                ("Network check", "DNS and ping 1.1.1.1 succeeded after start", False),
            ],
            s=s,
        ),
        Paragraph("Table 4. Live state after the first successful start.", s["caption"]),
    ]
    story.append(KeepTogether(state_block))

    story.append(Paragraph("6.  What did not come along for the ride", s["h1"]))
    story.append(
        Paragraph(
            "Two limitations are real on this board. Neither stopped the firewall from starting. Both should be expected if someone "
            "reads the journal and thinks the install failed.",
            s["body"],
        )
    )
    story.append(
        grid(
            ["Limitation", "What the log says", "Practical effect"],
            [
                [
                    "No Portmaster v2 on ARM",
                    "linux_arm64 v2 .deb is 404; stable.v3.json lists linux_amd64 only",
                    "This install is v1. SPN login still happens in the app. UI is the older Electron shell.",
                ],
                [
                    "Vendor kernel has no BTF",
                    "no BTF found for kernel version 6.1.43-rockchip-rk3588: not supported",
                    "eBPF extras (bandwidth stats, CO-RE probes) give up. Interception falls back to nfqueue, which is the classic Linux path and is enough for the firewall.",
                ],
                [
                    "Filter lists load slowly",
                    "intel/filterlists: not searching … because filterlists not loaded",
                    "Normal on first start while lists unpack. Domain blocklists become accurate after a few minutes.",
                ],
                [
                    "Installer wants a reboot",
                    "a reboot may be required  (unit file upgraded on disk)",
                    "Service was started without reboot and stayed healthy. A later reboot still settles DNS integration cleanly.",
                ],
            ],
            [1.75 * inch, 2.35 * inch, CONTENT_W - 4.1 * inch],
            s,
        )
    )
    story.append(Paragraph("Table 5. Known caveats on this Rockchip kernel.", s["caption"]))

    story.append(
        callout(
            "Do not paste Safing account passwords into chat.",
            "Portmaster itself is free and needed no login to install. SPN (the paid privacy network) is unlocked inside the "
            "running app: open Portmaster → SPN / Privacy Network → sign in with the Safing account. Credentials stay on this machine.",
            s,
        )
    )

    story.append(Paragraph("7.  How to use it from here", s["h1"]))
    story.append(Paragraph("Open the app", s["h2"]))
    story.append(
        Paragraph(
            "Applications menu → <b>Portmaster</b>, or run the command above. The notifier sits in the tray and asks about new connections.",
            s["bodyleft"],
        )
    )
    story.append(Paragraph("Sign in to SPN", s["h2"]))
    story.append(
        Paragraph(
            "In the app, open the SPN panel and enter the Safing account. The install is already done; login only turns on the privacy network.",
            s["bodyleft"],
        )
    )
    listeners = [
        Paragraph("Watch this box’s listeners", s["h2"]),
        Paragraph(
            "This Orange Pi was already serving SSH and several other sockets when Portmaster came up. If something suddenly cannot connect, "
            "open the app and allow that process or port rather than assuming the service died.",
            s["body"],
        ),
        grid(
            ["Port", "Notes"],
            [
                ["22", "SSH on all interfaces. Do not leave this blocked."],
                ["817", "Portmaster core API, localhost only. Used by the UI."],
                ["5050, 30001–30005, 30104", "Already listening before install. Prompt/allow in the app if they break."],
                ["53 (127.0.0.53)", "systemd-resolved. Portmaster may take over DNS after a reboot."],
            ],
            [2.4 * inch, CONTENT_W - 2.4 * inch],
            s,
        ),
        Paragraph("Table 6. Local listeners that matter after the firewall is live.", s["caption"]),
    ]
    story.append(KeepTogether(listeners))

    cheat = [
        Paragraph("8.  Operator cheat sheet", s["h1"]),
        grid(
            ["Task", "Command"],
            [
                ["Is the core up?", "systemctl status portmaster.service"],
                ["Start / stop / restart", "sudo systemctl start|stop|restart portmaster.service"],
                ["Follow the log", "journalctl -u portmaster.service -f"],
                ["Open the UI", "/opt/safing/portmaster/portmaster-start app --data=/opt/safing/portmaster"],
                ["Manual update", "sudo /opt/safing/portmaster/portmaster-start update --data=/opt/safing/portmaster"],
                ["Clean leftover iptables after a crash", "sudo /opt/safing/portmaster/portmaster-start recover-iptables"],
                ["Uninstall (official script)", "sudo bash /tmp/portmaster-install.sh --uninstall"],
                ["Uninstall and wipe config", "sudo bash /tmp/portmaster-install.sh --uninstall --purge"],
            ],
            [2.3 * inch, CONTENT_W - 2.3 * inch],
            s,
        ),
        Paragraph("Table 7. Day-to-day commands on this host.", s["caption"]),
    ]
    story.append(KeepTogether(cheat))

    story.append(Paragraph("9.  Why this counts as a win", s["h1"]))
    story.append(
        Paragraph(
            "The obvious path — download the Ubuntu button on safing.io — is a trap on Orange Pi. The package is beautiful, "
            "signed, and completely the wrong ISA. The working path was still official Safing infrastructure: their installer, "
            "their linux_arm64 update tree, their signatures. No qemu, no box64, no rebuilt kernel, no source compile.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "At verification time the core had been running under systemd, the UI and notifier were up on the local desktop, "
            "the API was listening on localhost:817, and the machine still had working DNS and outbound ICMP. That is a complete, "
            "boot-persistent Portmaster install on RK3588 ARM64.",
            s["body"],
        )
    )

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=8))
    story.append(
        Paragraph(
            "Sources used during the work: safing.io/download, wiki.safing.io Portmaster Linux install, "
            "updates.safing.io stable.json and stable.v3.json, GitHub safing/portmaster issues #758 and #2038, "
            "and live inspection of this host on 15 August 2026.",
            s["caption"],
        )
    )
    story.append(
        Paragraph(
            "Printed for the operator of orangepi5plus. Rebuild by re-running the two installer commands in section 4 with "
            "<font face='LibMono'>--arch arm64</font>. Do not install the amd64 .deb from the website on this board.",
            s["caption"],
        )
    )

    doc = SimpleDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Portmaster ARM64 Install Record — orangepi5plus",
        author="orangepi5plus operations",
        subject="Field record of installing Safing Portmaster v1 on Orange Pi 5 Plus (aarch64)",
        creator="reportlab  ·  Portmaster ARM64 field record",
        keywords="Portmaster,Safing,ARM64,Orange Pi 5 Plus,SPN,nfqueue",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    build()
