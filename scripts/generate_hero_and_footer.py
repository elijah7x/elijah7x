"""Generate animated Matrix x Doraemon hero and footer SVGs."""

from __future__ import annotations

from pathlib import Path

try:
    from . import pixel_lib
except ImportError:
    import pixel_lib

P = pixel_lib.PALETTE
FONT_ESC = pixel_lib.escape_xml(pixel_lib.FONT_MONO)

# 26x28 Matrix Doraemon body (Take-copter rotor blades rendered separately for spinning).
_DORAEMON_BODY: list[str] = [
    "..........................",
    "............yy............",
    "...........YYYY...........",
    ".......DDDDDDDDDDDD.......",
    ".....DDLLBBBBBBBBBBDD.....",
    "....DBLLBBBBBBBBBBBBBD....",
    "...DBBBWWWWKWWKWWWWBBBD...",
    "..DBCKKKKKKKKKKKKKKKKCBD..",
    "..DBKKKKKKKKKKKKKKKKKKBD..",
    "..DBWWKKKKKKRRKKKKKKWWBD..",
    "..DBWKWWKWWWRRWWWKWWKWBD..",
    "..DBWWWWWKWWWWWWKWWWWWBD..",
    "...DBWKWWKKKKKKKKWWKWBD...",
    "..CCDBWWWWWWWWWWWWWWBDCC..",
    ".CCCKKKRRRRYYYYRRRRKKKCCC.",
    ".CCKKKKrrrrYyyYrrrrKKKKCC.",
    ".CKKKKKKCCKKKKKKCCKKKKKKC.",
    ".CKKKKKCCKKKKKKKKCCKKKKKC.",
    ".CKKKKKKCKKKKKKKKCKKKKKKC.",
    "CCKKKKKKCKKKKKKKKCKKKKKKCC",
    "WWKKKKKKCKKKCCKKKCKKKKKKWW",
    "WWKKKKKKCKKKCCKKKCKKKKKKWW",
    ".CKKKKKKCKKKCCKKKCKKKKKKC.",
    ".CKKKKKKCKKKKKKKKCKKKKKKC.",
    "..CKKKKKCKKKKKKKKCKKKKKC..",
    "..CKKKKCC..CCCC..CCKKKKC..",
    ".....WWWW........WWWW.....",
    "....WWWWW........WWWWW....",
]

_COPTER_FRAME_A: list[str] = [
    "......YYyYYYYYYYYyYY......",
]

_COPTER_FRAME_B: list[str] = [
    ".........y.YYYY.y.........",
]

_DORAEMON_HUD_READOUT: list[str] = [
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "......g............g......",
    "......GGgGG....gGGGG......",
]

_DORAEMON_COLORS: dict[str, str] = {
    "B": P["dora_blue"],
    "D": P["dora_blue_dark"],
    "L": P["dora_blue_light"],
    "W": P["white"],
    "R": P["dora_red"],
    "r": P["dora_red_dark"],
    "Y": P["dora_gold"],
    "y": P["dora_gold_dark"],
    "K": P["coat"],
    "C": P["coat_light"],
    "G": P["green"],
    "g": P["green_mid"],
}

# 18x26 Anywhere Door slightly ajar revealing a glowing Matrix portal.
_ANYWHERE_DOOR: list[str] = [
    "pppppppppppppppppp",
    "pPPPPPPPPPPPPPPPPp",
    "pPpPPPPPPppgMMmMPp",
    "pPpPppppPppgMmMMPp",
    "pPpPpPPpPppgMMMmPp",
    "pPpPpPPpPppgMmMMPp",
    "pPpPpPPpPppgMMmMPp",
    "pPpPpPPpPppgMmMMPp",
    "pPpPpPPpPppgMMMmPp",
    "pPpPpPPpPppgMmMMPp",
    "pPpPppppPppgMMmMPp",
    "pPpPPPPPPppgMmMMPp",
    "pPpPPPPYYppgMMMmPp",
    "pPpPPPPYyppgMmMMPp",
    "pPpPPPPPPppgMMmMPp",
    "pPpPppppPppgMmMMPp",
    "pPpPpPPpPppgMMMmPp",
    "pPpPpPPpPppgMmMMPp",
    "pPpPpPPpPppgMMmMPp",
    "pPpPpPPpPppgMmMMPp",
    "pPpPpPPpPppgMMMmPp",
    "pPpPppppPppgMmMMPp",
    "pPpPPPPPPppgMMmMPp",
    "pPpPPPPPPppgMmMMPp",
    "pPpPPPPPPppgMMMmPp",
    "pppppppppppppppppp",
]

_DOOR_COLORS: dict[str, str] = {
    "P": P["door_pink"],
    "p": P["door_pink_dark"],
    "Y": P["dora_gold"],
    "y": P["dora_gold_dark"],
    "M": P["bg"],
    "m": P["bg_header"],
    "g": P["green_mid"],
}

# 12x8 Floating Dorayaki sprite.
_DORAYAKI: list[str] = [
    "...DDDDDD...",
    ".DDBBBBBBDD.",
    "DBBBBBBBBBBD",
    "DBBBBBBBBBBD",
    "DCCCCCCCCCCD",
    "DDDDDDDDDDDD",
    ".DBBBBBBBBD.",
    "..DDDDDDDD..",
]

_DORAYAKI_COLORS: dict[str, str] = {
    "D": P["dorayaki_dark"],
    "B": P["dorayaki_brown"],
    "C": P["dorayaki_cream"],
}

# 22x12 Retro pixel Time Machine gliding left-to-right.
_TIME_MACHINE: list[str] = [
    ".............W........",
    "............YY........",
    "...........yK.........",
    "..........BBBB........",
    "..........BGLB........",
    "....RRRR..BKKB........",
    "....RRRR..BBBB..YY....",
    "..GGYYYYYYYYYYYYYYYY..",
    "gGggBBBBBBBBBBBBBBBBYY",
    "..GGDDDDDDDDDDDDDDDDy.",
    "....yy....yy....yy....",
    "....g.....G.....g.....",
]

_TIME_MACHINE_COLORS: dict[str, str] = {
    "Y": P["dora_gold"],
    "y": P["dora_gold_dark"],
    "B": P["dora_blue"],
    "D": P["dora_blue_dark"],
    "L": P["dora_blue_light"],
    "R": P["dora_red"],
    "W": P["white"],
    "G": P["green"],
    "g": P["green_mid"],
    "K": P["coat"],
}


def _render_chip(x: int, y: int, width: int, height: int, label: str, accent: str) -> str:
    label_esc = pixel_lib.escape_xml(label)
    accent_esc = pixel_lib.escape_xml(accent)
    cx = x + width // 2
    cy = y + 16
    return (
        f'<g shape-rendering="crispEdges">'
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{P["bg_panel"]}"/>'
        f'<rect x="{x}" y="{y}" width="{width}" height="2" fill="{accent_esc}"/>'
        f'<rect x="{x}" y="{y + height - 2}" width="{width}" height="2" fill="{accent_esc}"/>'
        f'<rect x="{x}" y="{y}" width="2" height="{height}" fill="{accent_esc}"/>'
        f'<rect x="{x + width - 2}" y="{y}" width="2" height="{height}" fill="{accent_esc}"/>'
        f'<rect x="{x + 2}" y="{y + 2}" width="2" height="2" fill="{accent_esc}"/>'
        f'<rect x="{x + width - 4}" y="{y + height - 4}" width="2" height="2" fill="{accent_esc}"/>'
        f"</g>"
        f'<text x="{cx}" y="{cy}" text-anchor="middle" font-family="{FONT_ESC}" '
        f'font-size="9.5" font-weight="600" fill="{P["white"]}">{label_esc}</text>'
    )


def build_hero_svg() -> str:
    """Build the 900x260 animated Matrix x Doraemon hero SVG."""
    w, h = 900, 260
    rain_css = pixel_lib.matrix_rain_css(h)
    hero_css = (
        f"{rain_css}\n"
        "@keyframes dora-hover {\n"
        "  0%, 100% { transform: translateY(-4px); }\n"
        "  50% { transform: translateY(4px); }\n"
        "}\n"
        "@keyframes shadow-pulse {\n"
        "  0%, 100% { opacity: 0.48; transform: scaleX(0.94); }\n"
        "  50% { opacity: 0.80; transform: scaleX(1.04); }\n"
        "}\n"
        "@keyframes spin-a {\n"
        "  0%, 49.9% { opacity: 1; }\n"
        "  50%, 100% { opacity: 0; }\n"
        "}\n"
        "@keyframes spin-b {\n"
        "  0%, 49.9% { opacity: 0; }\n"
        "  50%, 100% { opacity: 1; }\n"
        "}\n"
        "@keyframes hud-flicker {\n"
        "  0%, 100% { opacity: 1; }\n"
        "  42% { opacity: 0.88; }\n"
        "  44% { opacity: 0.42; }\n"
        "  46% { opacity: 0.96; }\n"
        "  78% { opacity: 0.72; }\n"
        "  80% { opacity: 1; }\n"
        "}\n"
        "@keyframes cursor-blink {\n"
        "  0%, 49% { opacity: 1; }\n"
        "  50%, 100% { opacity: 0; }\n"
        "}\n"
        "@keyframes mote-rise {\n"
        "  0% { transform: translateY(22px); opacity: 0; }\n"
        "  20% { opacity: 0.95; }\n"
        "  80% { opacity: 0.85; }\n"
        "  100% { transform: translateY(-28px); opacity: 0; }\n"
        "}\n"
        "@keyframes dorayaki-bob {\n"
        "  0%, 100% { transform: translateY(0px); }\n"
        "  50% { transform: translateY(-5px); }\n"
        "}\n"
        ".dora-hover { animation: dora-hover 3.2s ease-in-out infinite; }\n"
        ".dora-shadow { transform-origin: 103px 206px; animation: shadow-pulse 3.2s ease-in-out infinite; }\n"
        ".copter-a { animation: spin-a 0.24s steps(1, end) infinite; }\n"
        ".copter-b { animation: spin-b 0.24s steps(1, end) infinite; }\n"
        ".hud-flicker { animation: hud-flicker 2.8s linear infinite; }\n"
        ".cursor-blink { animation: cursor-blink 1s steps(1, end) infinite; }\n"
        ".dorayaki-bob { animation: dorayaki-bob 2.6s ease-in-out infinite; }\n"
        ".mote-1 { animation: mote-rise 2.4s linear infinite; }\n"
        ".mote-2 { animation: mote-rise 2.9s linear infinite -1.1s; }\n"
        ".mote-3 { animation: mote-rise 2.1s linear infinite -0.6s; }\n"
        ".mote-4 { animation: mote-rise 3.2s linear infinite -2.0s; }\n"
    )

    frame = pixel_lib.render_terminal_frame(
        w,
        h,
        title="elijah7x@4d-pocket:~/matrix",
        right_tag="[NEO-2112 // ONLINE]",
    )
    rain = pixel_lib.render_matrix_rain(w, h, cols=24, seed=42, opacity=0.18, y_start=28)

    # Holographic pixel shadow under Doraemon (centered at x=103, y=202..210).
    dora_shadow = (
        '<g class="dora-shadow" shape-rendering="crispEdges">'
        f'<rect x="58" y="204" width="90" height="4" fill="{P["green_dim"]}" fill-opacity="0.55"/>'
        f'<rect x="70" y="202" width="66" height="8" fill="{P["green_mid"]}" fill-opacity="0.40"/>'
        f'<rect x="84" y="204" width="38" height="4" fill="{P["green"]}" fill-opacity="0.65"/>'
        "</g>"
    )

    dora_x, dora_y, dora_px = 38, 48, 5
    dora_body = pixel_lib.render_sprite(_DORAEMON_BODY, _DORAEMON_COLORS, dora_x, dora_y, px=dora_px)
    copter_a = pixel_lib.render_sprite(
        _COPTER_FRAME_A, _DORAEMON_COLORS, dora_x, dora_y, px=dora_px, extra_attrs='class="copter-a"'
    )
    copter_b = pixel_lib.render_sprite(
        _COPTER_FRAME_B, _DORAEMON_COLORS, dora_x, dora_y, px=dora_px, extra_attrs='class="copter-b"'
    )
    hud_lines = pixel_lib.render_sprite(
        _DORAEMON_HUD_READOUT,
        _DORAEMON_COLORS,
        dora_x,
        dora_y,
        px=dora_px,
        extra_attrs='class="hud-flicker"',
    )
    dora_group = f'<g class="dora-hover">{dora_body}{copter_a}{copter_b}{hud_lines}</g>'

    # Center typography (x=218..675).
    prompt_line = (
        f'<text x="218" y="68" font-family="{FONT_ESC}" font-size="11" '
        f'font-weight="600" fill="{P["green_mid"]}">'
        f"{pixel_lib.escape_xml('// ACCESS GRANTED · 22ND CENTURY GADGET LAB')}</text>"
    )
    title_shadow = pixel_lib.render_pixel_text("ELIJAH7X", 220, 84, px=6, fill=P["dora_blue"])
    title_main = pixel_lib.render_pixel_text("ELIJAH7X", 218, 82, px=6, fill=P["green"])

    bio1 = (
        f'<text x="218" y="148" font-family="{FONT_ESC}" font-size="13" fill="#E2F5E8">'
        f"{pixel_lib.escape_xml('> Native macOS coding-agent workspaces & minimalist systems')}</text>"
    )
    bio2 = (
        f'<text x="218" y="170" font-family="{FONT_ESC}" font-size="13" fill="#9BC4A8">'
        f"{pixel_lib.escape_xml('> Swift · Python · CSS · TypeScript · Obsidian')}</text>"
        f'<rect x="594" y="159" width="8" height="13" fill="{P["green"]}" '
        f'shape-rendering="crispEdges" class="cursor-blink"/>'
    )

    chips = "".join(
        [
            _render_chip(218, 198, 142, 26, "[ 4D-POCKET: MOUNTED ]", P["dora_blue"]),
            _render_chip(368, 198, 148, 26, "[ FUEL: DORAYAKI 100% ]", P["dora_gold"]),
            _render_chip(524, 198, 136, 26, "[ PINNED: 3 GADGETS ]", P["green_mid"]),
        ]
    )

    # Right Doraemon scene: Anywhere Door + portal motes + floating Dorayaki.
    door_x, door_y, door_px = 742, 82, 5
    door_sprite = pixel_lib.render_sprite(_ANYWHERE_DOOR, _DOOR_COLORS, door_x, door_y, px=door_px)
    portal_x = door_x + 11 * door_px
    portal_y = door_y + 2 * door_px
    portal_w = 5 * door_px
    portal_h = 23 * door_px
    portal_motes = (
        f'<defs><clipPath id="door-portal-clip">'
        f'<rect x="{portal_x}" y="{portal_y}" width="{portal_w}" height="{portal_h}"/>'
        f"</clipPath></defs>"
        f'<g clip-path="url(#door-portal-clip)" shape-rendering="crispEdges">'
        f'<rect x="{portal_x + 3}" y="{portal_y + 24}" width="3" height="4" fill="{P["green"]}" class="mote-1"/>'
        f'<rect x="{portal_x + 11}" y="{portal_y + 52}" width="3" height="5" fill="{P["green_soft"]}" class="mote-2"/>'
        f'<rect x="{portal_x + 17}" y="{portal_y + 78}" width="3" height="3" fill="{P["green"]}" class="mote-3"/>'
        f'<rect x="{portal_x + 7}" y="{portal_y + 96}" width="2" height="4" fill="{P["green_mid"]}" class="mote-4"/>'
        "</g>"
    )

    dorayaki_sprite = pixel_lib.render_sprite(
        _DORAYAKI,
        _DORAYAKI_COLORS,
        678,
        184,
        px=4,
        extra_attrs='class="dorayaki-bob"',
    )
    door_caption = (
        f'<text x="{door_x + 45}" y="236" text-anchor="middle" font-family="{FONT_ESC}" '
        f'font-size="10" font-weight="600" fill="{P["green_soft"]}">ANYWHERE_DOOR.exe</text>'
    )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" '
        'aria-label="elijah7x Matrix Doraemon Hero Banner">\n'
        f"<style>\n{hero_css}</style>\n"
        f"{frame}\n"
        f"{rain}\n"
        f"{dora_shadow}\n"
        f"{dora_group}\n"
        f"{prompt_line}\n"
        f"{title_shadow}\n"
        f"{title_main}\n"
        f"{bio1}\n"
        f"{bio2}\n"
        f"{chips}\n"
        f"{door_sprite}\n"
        f"{portal_motes}\n"
        f"{dorayaki_sprite}\n"
        f"{door_caption}\n"
        "</svg>\n"
    )


def build_footer_svg() -> str:
    """Build the 900x84 animated Matrix time-tunnel footer SVG."""
    w, h = 900, 84
    footer_css = (
        "@keyframes speed-scroll {\n"
        "  0% { transform: translateX(0px); }\n"
        "  100% { transform: translateX(-300px); }\n"
        "}\n"
        "@keyframes tm-glide {\n"
        "  0% { transform: translateX(-80px); }\n"
        "  100% { transform: translateX(920px); }\n"
        "}\n"
        "@keyframes tm-bob {\n"
        "  0%, 100% { transform: translateY(-2px); }\n"
        "  50% { transform: translateY(2px); }\n"
        "}\n"
        ".speed-fast { animation: speed-scroll 1.8s linear infinite; }\n"
        ".speed-slow { animation: speed-scroll 3.1s linear infinite; }\n"
        ".tm-glide { animation: tm-glide 12s linear infinite -4.2s; }\n"
        ".tm-bob { animation: tm-bob 1.4s ease-in-out infinite; }\n"
    )

    # Speed lines repeated over 1200px width so -300px translation loops seamlessly.
    fast_lines: list[str] = []
    slow_lines: list[str] = []
    for base_x in range(0, 1200, 300):
        fast_lines.extend(
            [
                f'<rect x="{base_x + 18}" y="12" width="54" height="2" fill="{P["green_mid"]}" fill-opacity="0.45"/>',
                f'<rect x="{base_x + 140}" y="22" width="76" height="2" fill="{P["green"]}" fill-opacity="0.32"/>',
                f'<rect x="{base_x + 235}" y="38" width="42" height="2" fill="{P["green_mid"]}" fill-opacity="0.40"/>',
            ]
        )
        slow_lines.extend(
            [
                f'<rect x="{base_x + 45}" y="30" width="90" height="2" fill="{P["green_dim"]}" fill-opacity="0.60"/>',
                f'<rect x="{base_x + 185}" y="16" width="64" height="2" fill="{P["green_dim"]}" fill-opacity="0.50"/>',
                f'<rect x="{base_x + 260}" y="44" width="32" height="2" fill="{P["green_dim"]}" fill-opacity="0.55"/>',
            ]
        )

    time_machine = pixel_lib.render_sprite(_TIME_MACHINE, _TIME_MACHINE_COLORS, 0, 11, px=3)
    quote = '// 4D-POCKET ONLINE · "Every great tool feels like a gadget from 2112." · github.com/elijah7x'
    quote_esc = pixel_lib.escape_xml(quote)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" '
        'aria-label="elijah7x Matrix Time Machine Footer">\n'
        f"<style>\n{footer_css}</style>\n"
        "<defs>\n"
        '  <clipPath id="footer-tunnel-clip"><rect x="2" y="2" width="896" height="80"/></clipPath>\n'
        '  <pattern id="footer-scanlines" width="4" height="4" patternUnits="userSpaceOnUse">\n'
        '    <rect x="0" y="0" width="4" height="2" fill="#000000" fill-opacity="0.16"/>\n'
        "  </pattern>\n"
        "</defs>\n"
        '<g shape-rendering="crispEdges">\n'
        f'  <rect x="0" y="0" width="{w}" height="{h}" fill="{P["bg"]}"/>\n'
        f'  <rect x="2" y="4" width="{w - 4}" height="{h - 8}" fill="{P["bg_panel"]}" fill-opacity="0.55"/>\n'
        f'  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#footer-scanlines)"/>\n'
        f'  <rect x="0" y="0" width="{w}" height="2" fill="{P["border"]}"/>\n'
        f'  <rect x="0" y="{h - 2}" width="{w}" height="2" fill="{P["border"]}"/>\n'
        f'  <rect x="0" y="0" width="2" height="{h}" fill="{P["border"]}"/>\n'
        f'  <rect x="{w - 2}" y="0" width="2" height="{h}" fill="{P["border"]}"/>\n'
        f'  <rect x="0" y="0" width="14" height="2" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="0" y="0" width="2" height="10" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="2" y="2" width="2" height="2" fill="{P["green"]}"/>\n'
        f'  <rect x="{w - 14}" y="0" width="14" height="2" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="{w - 2}" y="0" width="2" height="10" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="{w - 4}" y="2" width="2" height="2" fill="{P["green"]}"/>\n'
        f'  <rect x="0" y="{h - 2}" width="14" height="2" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="0" y="{h - 10}" width="2" height="10" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="2" y="{h - 4}" width="2" height="2" fill="{P["green"]}"/>\n'
        f'  <rect x="{w - 14}" y="{h - 2}" width="14" height="2" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="{w - 2}" y="{h - 10}" width="2" height="10" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="{w - 4}" y="{h - 4}" width="2" height="2" fill="{P["green"]}"/>\n'
        "</g>\n"
        '<g clip-path="url(#footer-tunnel-clip)">\n'
        f'  <g class="speed-slow" shape-rendering="crispEdges">{"".join(slow_lines)}</g>\n'
        f'  <g class="speed-fast" shape-rendering="crispEdges">{"".join(fast_lines)}</g>\n'
        '  <g class="tm-glide">\n'
        f'    <g class="tm-bob">{time_machine}</g>\n'
        "  </g>\n"
        "</g>\n"
        '<g shape-rendering="crispEdges">\n'
        f'  <rect x="116" y="53" width="668" height="22" fill="{P["bg"]}" fill-opacity="0.92"/>\n'
        f'  <rect x="116" y="53" width="668" height="1" fill="{P["border"]}"/>\n'
        f'  <rect x="116" y="74" width="668" height="1" fill="{P["border"]}"/>\n'
        f'  <rect x="116" y="53" width="1" height="22" fill="{P["border"]}"/>\n'
        f'  <rect x="783" y="53" width="1" height="22" fill="{P["border"]}"/>\n'
        f'  <rect x="118" y="55" width="2" height="2" fill="{P["green_mid"]}"/>\n'
        f'  <rect x="780" y="71" width="2" height="2" fill="{P["green_mid"]}"/>\n'
        "</g>\n"
        f'<text x="450" y="68" text-anchor="middle" font-family="{FONT_ESC}" '
        f'font-size="11.5" font-weight="500" fill="#A7D7B7">{quote_esc}</text>\n'
        "</svg>\n"
    )


def main() -> None:
    """Write hero-matrix-doraemon.svg and footer-time-machine.svg into assets/."""
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "hero-matrix-doraemon.svg").write_text(build_hero_svg(), encoding="utf-8")
    (assets_dir / "footer-time-machine.svg").write_text(build_footer_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
