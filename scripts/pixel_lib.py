"""Shared pixel-art SVG engine for the Matrix x Doraemon GitHub profile."""

from __future__ import annotations

import random

DARK_PALETTE: dict[str, str] = {
    "bg": "#070D09",
    "bg_panel": "#0D1B12",
    "bg_header": "#122619",
    "border": "#1E4D2B",
    "border_bright": "#22C55E",
    "green": "#39FF14",
    "green_mid": "#22C55E",
    "green_soft": "#86EFAC",
    "green_dim": "#2F6B43",
    "dora_blue": "#0088E0",
    "dora_blue_dark": "#005FA3",
    "dora_blue_light": "#38BDF8",
    "dora_red": "#E53935",
    "dora_red_dark": "#991B1B",
    "dora_gold": "#FACC15",
    "dora_gold_dark": "#CA8A04",
    "door_pink": "#FF5C93",
    "door_pink_dark": "#BE185D",
    "dorayaki_brown": "#C27834",
    "dorayaki_dark": "#7C3F13",
    "dorayaki_cream": "#FDE68A",
    "coat": "#181C20",
    "coat_light": "#2D333B",
    "white": "#F0F6FC",
    "muted": "#8BA894",
    "text_primary": "#E2F5E8",
    "text_secondary": "#9BC4A8",
    "text_card": "#D8EFE0",
    "text_footer": "#A7D7B7",
    "chip_text": "#F0F6FC",
    "pill_text": "#F0F6FC",
    "stage_bg": "#070D09",
    "tile_bg": "#0B160F",
    "unlit_block": "#162E1E",
    "scanline_color": "#000000",
    "scanline_opacity": "0.16",
    "rain_color": "#39FF14",
    "h2_geo_stroke": "#F0F6FC",
    "h2_title": "#F0F6FC",
    "tivano_title": "#38BDF8",
    "token_title": "#FACC15",
    "hero_title_main": "#39FF14",
    "hero_title_shadow": "#0088E0",
    "telemetry_value": "#39FF14",
    "telemetry_glow": "1",
    "bell_gold": "#FACC15",
    "bell_gold_dark": "#CA8A04",
    "hud_green": "#39FF14",
    "hud_green_mid": "#22C55E",
    "portal_bg": "#070D09",
    "portal_bg_alt": "#122619",
    "shadow_green": "#22C55E",
    "shadow_green_dim": "#2F6B43",
}

LIGHT_PALETTE: dict[str, str] = {
    "bg": "#F7FBF8",
    "bg_panel": "#EEF7F1",
    "bg_header": "#E1F2E7",
    "border": "#9ED0B0",
    "border_bright": "#16A34A",
    "green": "#16A34A",
    "green_mid": "#15803D",
    "green_soft": "#166534",
    "green_dim": "#86C79D",
    "dora_blue": "#0088E0",
    "dora_blue_dark": "#005FA3",
    "dora_blue_light": "#0284C7",
    "dora_red": "#DC2626",
    "dora_red_dark": "#991B1B",
    "dora_gold": "#D97706",
    "dora_gold_dark": "#92400E",
    "door_pink": "#EC4899",
    "door_pink_dark": "#BE185D",
    "dorayaki_brown": "#C27834",
    "dorayaki_dark": "#7C3F13",
    "dorayaki_cream": "#FDE68A",
    "coat": "#181C20",
    "coat_light": "#374151",
    "white": "#FFFFFF",
    "muted": "#3D6850",
    "text_primary": "#0F291A",
    "text_secondary": "#2D593E",
    "text_card": "#1E3A2B",
    "text_footer": "#1D4D32",
    "chip_text": "#0F291A",
    "pill_text": "#133020",
    "stage_bg": "#ECF7F0",
    "tile_bg": "#FFFFFF",
    "unlit_block": "#D4EADF",
    "scanline_color": "#0F3D22",
    "scanline_opacity": "0.035",
    "rain_color": "#16A34A",
    "h2_geo_stroke": "#0F291A",
    "h2_title": "#0F291A",
    "tivano_title": "#026AA7",
    "token_title": "#B45309",
    "hero_title_main": "#15803D",
    "hero_title_shadow": "#38BDF8",
    "telemetry_value": "#15803D",
    "telemetry_glow": "0",
    "bell_gold": "#FACC15",
    "bell_gold_dark": "#CA8A04",
    "hud_green": "#39FF14",
    "hud_green_mid": "#22C55E",
    "portal_bg": "#07130C",
    "portal_bg_alt": "#122B1B",
    "shadow_green": "#16A34A",
    "shadow_green_dim": "#86C79D",
}

PALETTE: dict[str, str] = DARK_PALETTE


def get_palette(theme: str = "dark") -> dict[str, str]:
    """Return a copy of the palette for the requested theme ('dark' or 'light')."""
    if theme == "dark":
        return DARK_PALETTE.copy()
    if theme == "light":
        return LIGHT_PALETTE.copy()
    raise ValueError(f"Unknown theme: {theme!r}. Expected 'dark' or 'light'.")

FONT_MONO = "'SF Mono', 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, Consolas, monospace"

# Crisp 5x7 uppercase pixel bitmap font.
_FONT_5X7: dict[str, tuple[str, ...]] = {
    "A": (
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "B": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#...#",
        "#...#",
        "####.",
    ),
    "C": (
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
    ),
    "D": (
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "####.",
    ),
    "E": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ),
    "F": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "G": (
        ".####",
        "#....",
        "#....",
        "#.###",
        "#...#",
        "#...#",
        ".####",
    ),
    "H": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "I": (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "#####",
    ),
    "J": (
        "..###",
        "...#.",
        "...#.",
        "...#.",
        "#..#.",
        "#..#.",
        ".##..",
    ),
    "K": (
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "L": (
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
    ),
    "M": (
        "#...#",
        "##.##",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
    ),
    "N": (
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
    ),
    "O": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "P": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "Q": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    "R": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "S": (
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "T": (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "U": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "V": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
    ),
    "W": (
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        "##.##",
        "#...#",
    ),
    "X": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
    ),
    "Y": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "Z": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
    ),
    "0": (
        ".###.",
        "#..##",
        "#.#.#",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
    ),
    "1": (
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ),
    "2": (
        ".###.",
        "#...#",
        "....#",
        "..##.",
        ".#...",
        "#....",
        "#####",
    ),
    "3": (
        "####.",
        "....#",
        "....#",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "4": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "....#",
        "....#",
        "....#",
    ),
    "5": (
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "#...#",
        ".###.",
    ),
    "6": (
        ".###.",
        "#....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "7": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        ".#...",
        ".#...",
    ),
    "8": (
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
    ),
    "9": (
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "....#",
        ".###.",
    ),
    " ": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    "-": (
        ".....",
        ".....",
        ".....",
        "#####",
        ".....",
        ".....",
        ".....",
    ),
    "_": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        "#####",
    ),
    ".": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
    ),
    ":": (
        ".....",
        ".##..",
        ".##..",
        ".....",
        ".##..",
        ".##..",
        ".....",
    ),
    "/": (
        "....#",
        "...#.",
        "...#.",
        "..#..",
        ".#...",
        ".#...",
        "#....",
    ),
    "#": (
        ".#.#.",
        "#####",
        ".#.#.",
        ".#.#.",
        "#####",
        ".#.#.",
        ".....",
    ),
    "+": (
        ".....",
        "..#..",
        "..#..",
        "#####",
        "..#..",
        "..#..",
        ".....",
    ),
    "[": (
        ".###.",
        ".#...",
        ".#...",
        ".#...",
        ".#...",
        ".#...",
        ".###.",
    ),
    "]": (
        ".###.",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        ".###.",
    ),
    ">": (
        "#....",
        ".#...",
        "..#..",
        "...#.",
        "..#..",
        ".#...",
        "#....",
    ),
    "<": (
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "..#..",
        "...#.",
        "....#",
    ),
    "!": (
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
        "..#..",
    ),
    "?": (
        ".###.",
        "#...#",
        "....#",
        "..##.",
        "..#..",
        ".....",
        "..#..",
    ),
    "&": (
        ".##..",
        "#..#.",
        "#.#..",
        ".#...",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    "|": (
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "'": (
        "..#..",
        "..#..",
        ".#...",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    '"': (
        ".#.#.",
        ".#.#.",
        ".#.#.",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
}

_MATRIX_GLYPHS = (
    "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
    "0123456789ABCDEF0101$+-*/=%"
)


def escape_xml(s: str) -> str:
    """Escape XML special characters for safe SVG text and attributes."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _format_extra_attrs(extra_attrs: str) -> str:
    stripped = extra_attrs.strip()
    return f" {stripped}" if stripped else ""


def render_sprite(
    grid: list[str],
    color_map: dict[str, str],
    x: int,
    y: int,
    px: int = 4,
    extra_attrs: str = "",
) -> str:
    """Render an ASCII pixel grid as run-length-encoded SVG <rect> elements."""
    rects: list[str] = []
    for row_idx, row in enumerate(grid):
        col = 0
        row_len = len(row)
        ry = y + row_idx * px
        while col < row_len:
            ch = row[col]
            if ch in (".", " ") or ch not in color_map:
                col += 1
                continue
            run_end = col + 1
            while run_end < row_len and row[run_end] == ch:
                run_end += 1
            rx = x + col * px
            rw = (run_end - col) * px
            fill = escape_xml(color_map[ch])
            rects.append(
                f'<rect x="{rx}" y="{ry}" width="{rw}" height="{px}" fill="{fill}"/>'
            )
            col = run_end

    attrs = _format_extra_attrs(extra_attrs)
    body = "".join(rects)
    return f'<g shape-rendering="crispEdges"{attrs}>{body}</g>'


def render_pixel_text(
    text: str,
    x: int,
    y: int,
    px: int = 3,
    fill: str = "#39FF14",
    letter_spacing: int = 1,
    extra_attrs: str = "",
) -> str:
    """Render uppercase 5x7 bitmap text as run-length-encoded SVG <rect> pixels."""
    upper = text.upper()
    if not upper:
        attrs = _format_extra_attrs(extra_attrs)
        return f'<g shape-rendering="crispEdges"{attrs}></g>'

    # Build combined 7-row pixel buffer so letter_spacing=0 also RLE-merges cleanly.
    spacer = "." * max(0, letter_spacing)
    rows: list[str] = []
    for r in range(7):
        parts: list[str] = []
        for idx, ch in enumerate(upper):
            glyph = _FONT_5X7.get(ch, _FONT_5X7[" "])
            parts.append(glyph[r])
            if idx < len(upper) - 1 and spacer:
                parts.append(spacer)
        rows.append("".join(parts))

    return render_sprite(
        rows,
        {"#": fill},
        x=x,
        y=y,
        px=px,
        extra_attrs=extra_attrs,
    )


def matrix_rain_css(height: int) -> str:
    """Return CSS @keyframes and classes for falling Matrix rain columns."""
    travel_end = height + 24
    return (
        f"@keyframes matrix-fall {{ "
        f"0% {{ transform: translateY(-210px); }} "
        f"100% {{ transform: translateY({travel_end}px); }} "
        f"}}\n"
        ".rain-slow { animation: matrix-fall 13s linear infinite; }\n"
        ".rain-med { animation: matrix-fall 9s linear infinite; }\n"
        ".rain-fast { animation: matrix-fall 6s linear infinite; }"
    )


def render_matrix_rain(
    width: int,
    height: int,
    cols: int = 24,
    seed: int = 42,
    opacity: float = 0.20,
    y_start: int = 28,
    theme: str = "dark",
) -> str:
    """Generate deterministic falling Matrix green code columns clipped to the canvas."""
    p = get_palette(theme)
    rng = random.Random(seed)
    clip_id = f"matrix-rain-clip-{width}x{height}-{seed}-{theme}"
    clip_h = max(0, height - y_start - 2)
    clip_w = max(0, width - 4)

    classes = (
        ("rain-slow", 13.0),
        ("rain-med", 9.0),
        ("rain-fast", 6.0),
    )

    col_step = (width - 24) / max(1, cols)
    elements: list[str] = []
    for idx in range(cols):
        cx = int(round(14 + idx * col_step + rng.uniform(-3.0, 3.0)))
        cls_name, duration = rng.choice(classes)
        delay = -round(rng.uniform(0.0, duration), 2)
        chain_len = rng.randint(10, 15)
        font_size = rng.choice((10, 11, 12))
        line_dy = font_size + 2

        tspans: list[str] = []
        for g_idx in range(chain_len):
            ch = escape_xml(rng.choice(_MATRIX_GLYPHS))
            if g_idx == chain_len - 1:
                g_fill = p["green_soft"] if theme == "dark" else p["rain_color"]
                t_op = "0.95"
            elif g_idx >= chain_len - 3:
                g_fill = p["rain_color"]
                t_op = "0.80"
            elif g_idx < 3:
                g_fill = p["green_dim"]
                t_op = "0.45"
            else:
                g_fill = p["green_mid"] if theme == "dark" else p["rain_color"]
                t_op = "0.65"

            dy_attr = ' y="0"' if g_idx == 0 else f' dy="{line_dy}"'
            tspans.append(
                f'<tspan x="{cx}"{dy_attr} fill="{g_fill}" fill-opacity="{t_op}">{ch}</tspan>'
            )

        elements.append(
            f'<text x="{cx}" y="0" class="{cls_name}" '
            f'style="animation-delay:{delay}s" '
            f'font-family="{escape_xml(FONT_MONO)}" font-size="{font_size}" '
            f'font-weight="600">{"".join(tspans)}</text>'
        )

    return (
        f'<defs><clipPath id="{clip_id}">'
        f'<rect x="2" y="{y_start}" width="{clip_w}" height="{clip_h}"/>'
        f"</clipPath></defs>"
        f'<g clip-path="url(#{clip_id})" opacity="{opacity:.2f}">'
        f'{"".join(elements)}'
        f"</g>"
    )


def render_terminal_frame(
    width: int,
    height: int,
    title: str,
    right_tag: str = "",
    accent: str | None = None,
    header_height: int = 28,
    theme: str = "dark",
) -> str:
    """Render a pixel-crisp terminal frame with scanlines, corner pixels, and header."""
    p = get_palette(theme)
    resolved_accent = p["green_mid"] if accent is None else accent
    pattern_id = f"crt-scanlines-{width}x{height}-{theme}"
    accent_esc = escape_xml(resolved_accent)
    title_esc = escape_xml(title)
    right_esc = escape_xml(right_tag)
    font_esc = escape_xml(FONT_MONO)

    header_inner_h = max(0, header_height - 2)
    divider_y = max(2, header_height - 2)
    dot_y = 2 + max(0, (header_inner_h - 6) // 2)
    text_y = 2 + max(12, header_inner_h // 2 + 4)

    parts: list[str] = [
        f'<defs><pattern id="{pattern_id}" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect x="0" y="0" width="4" height="2" fill="{p["scanline_color"]}" fill-opacity="{p["scanline_opacity"]}"/>'
        f"</pattern></defs>",
        '<g shape-rendering="crispEdges">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="{p["bg"]}"/>',
        f'<rect x="2" y="{header_height}" width="{width - 4}" height="{max(0, height - header_height - 2)}" fill="url(#{pattern_id})"/>',
        f'<rect x="2" y="2" width="{width - 4}" height="{header_inner_h}" fill="{p["bg_header"]}"/>',
        f'<rect x="2" y="{divider_y}" width="{width - 4}" height="2" fill="{p["border"]}"/>',
        # Outer 2px border.
        f'<rect x="0" y="0" width="{width}" height="2" fill="{p["border"]}"/>',
        f'<rect x="0" y="{height - 2}" width="{width}" height="2" fill="{p["border"]}"/>',
        f'<rect x="0" y="0" width="2" height="{height}" fill="{p["border"]}"/>',
        f'<rect x="{width - 2}" y="0" width="2" height="{height}" fill="{p["border"]}"/>',
        # Bright pixel corner brackets.
        f'<rect x="0" y="0" width="8" height="2" fill="{accent_esc}"/>',
        f'<rect x="0" y="0" width="2" height="8" fill="{accent_esc}"/>',
        f'<rect x="2" y="2" width="2" height="2" fill="{p["green"]}"/>',
        f'<rect x="{width - 8}" y="0" width="8" height="2" fill="{accent_esc}"/>',
        f'<rect x="{width - 2}" y="0" width="2" height="8" fill="{accent_esc}"/>',
        f'<rect x="{width - 4}" y="2" width="2" height="2" fill="{p["green"]}"/>',
        f'<rect x="0" y="{height - 2}" width="8" height="2" fill="{accent_esc}"/>',
        f'<rect x="0" y="{height - 8}" width="2" height="8" fill="{accent_esc}"/>',
        f'<rect x="2" y="{height - 4}" width="2" height="2" fill="{p["green"]}"/>',
        f'<rect x="{width - 8}" y="{height - 2}" width="8" height="2" fill="{accent_esc}"/>',
        f'<rect x="{width - 2}" y="{height - 8}" width="2" height="8" fill="{accent_esc}"/>',
        f'<rect x="{width - 4}" y="{height - 4}" width="2" height="2" fill="{p["green"]}"/>',
        # 6x6 pixel window status squares (kept bright in both themes).
        f'<rect x="12" y="{dot_y}" width="6" height="6" fill="#E53935"/>',
        f'<rect x="22" y="{dot_y}" width="6" height="6" fill="#FACC15"/>',
        f'<rect x="32" y="{dot_y}" width="6" height="6" fill="#22C55E"/>',
        "</g>",
        f'<text x="48" y="{text_y}" font-family="{font_esc}" font-size="11" '
        f'font-weight="600" fill="{p["green_soft"]}">{title_esc}</text>',
    ]

    if right_tag:
        parts.append(
            f'<text x="{width - 12}" y="{text_y}" text-anchor="end" '
            f'font-family="{font_esc}" font-size="11" font-weight="600" '
            f'fill="{accent_esc}">{right_esc}</text>'
        )

    return "".join(parts)
