#!/usr/bin/env python3
"""Generate the three animated pixel-art gadget repo cards in assets/."""

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from pixel_lib import (  # noqa: E402
    FONT_MONO,
    PALETTE,
    escape_xml,
    render_pixel_text,
    render_sprite,
    render_terminal_frame,
)

CARD_WIDTH = 290
CARD_HEIGHT = 198
ASSETS_DIR = SCRIPT_DIR.parent / 'assets'

MINI_DORA_GRID = [
    '...CCCCC...',
    '.CCCCCCCCC.',
    '.CCWWWWWCC.',
    '.CWWBWBWWC.',
    '.CWWWNWWWC.',
    '.CWWWWWWWC.',
    '.CWWBBBWWC.',
    '..DWWWWWD..',
    '..RRRRRRR..',
    '....GGG....',
]

WEATHER_GRID = [
    '...O..O..O....',
    '....YYYYY.....',
    '.O.YYYYYYY.O..',
    '...YYYYYYY....',
    '.O.YYYYYWW....',
    '..WWWWWWWW.LLL',
    '.WWWWWWWWWW...',
    '.WBBBBBBBBWLLL',
    '..BBBBBBBB....',
    '....LLLLLLL...',
]

DORAYAKI_COIN_GRID = [
    '...DDDDDD...',
    '.DDBBBBBBDD.',
    '.DBWBBBBGBD.',
    'DBBBBBBBBBBD',
    'DCCCCCCCCCCD',
    'DYYYYYYYYYYD',
    'DBBBBBBBBBBD',
    '.DBBBBBBBBD.',
    '.DDBBBBBBDD.',
    '...DDDDDD...',
]

SPARKLE_GRID = [
    '.W.',
    'WGW',
    '.W.',
]

HYDROGEN_SQUARE_GRID = [
    'WWWWWWWWWWWW',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    'WWWWWWWWWWWW',
]

HYDROGEN_CIRCLE_GRID = [
    '....WWWW....',
    '..WW....WW..',
    '.W........W.',
    '.W........W.',
    'W..........W',
    'W..........W',
    'W..........W',
    'W..........W',
    '.W........W.',
    '.W........W.',
    '..WW....WW..',
    '....WWWW....',
]

HYDROGEN_TRIANGLE_GRID = [
    '......W......',
    '.....W.W.....',
    '.....W.W.....',
    '....W...W....',
    '....W...W....',
    '...W.....W...',
    '...W.....W...',
    '..W.......W..',
    '..W.......W..',
    '.W.........W.',
    '.W.........W.',
    'WWWWWWWWWWWWW',
]

SIGNAL_CORE_GRID = [
    '.R.',
    'RHR',
    '.R.',
]

SIGNAL_RING_GRID = [
    '.RRR.',
    'R...R',
    'R...R',
    'R...R',
    '.RRR.',
]


def _wrap_svg(aria_label: str, styles: str, body: str, defs: str = '') -> str:
    defs_block = f'  <defs>\n{defs}\n  </defs>\n' if defs else ''
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" '
        f'width="{CARD_WIDTH}" height="{CARD_HEIGHT}" '
        f'role="img" aria-label="{escape_xml(aria_label)}">\n'
        f'{defs_block}'
        f'  <style>\n{styles}\n  </style>\n'
        f'{body}\n'
        f'</svg>\n'
    )


def _render_stage_box(sub_label: str, accent: str) -> str:
    return '\n'.join([
        f'  <rect x="14" y="36" width="262" height="68" rx="3" '
        f'fill="{PALETTE["bg"]}" stroke="{PALETTE["border"]}" stroke-width="1"/>',
        f'  <rect x="15" y="37" width="260" height="1" fill="{accent}" opacity="0.25"/>',
        f'  <text x="268" y="48" text-anchor="end" '
        f'font-family="{FONT_MONO}" font-size="9" font-weight="600" '
        f'letter-spacing="0.6" fill="{PALETTE["muted"]}">{escape_xml(sub_label)}</text>',
    ])


def _render_text_block(title: str, title_color: str, line1: str, line2: str) -> str:
    pixel_title = render_pixel_text(title, x=16, y=114, px=3, fill=title_color)
    return '\n'.join([
        pixel_title,
        f'  <text x="16" y="149" font-family="{FONT_MONO}" font-size="11.5" '
        f'fill="#D8EFE0">{escape_xml(line1)}</text>',
        f'  <text x="16" y="164" font-family="{FONT_MONO}" font-size="11.5" '
        f'fill="#D8EFE0">{escape_xml(line2)}</text>',
    ])


def _render_pill_bar(tags: list[str], accent: str) -> str:
    parts: list[str] = []
    cursor_x = 16
    pill_y = 172
    pill_h = 18
    gap = 7

    for tag in tags:
        pill_w = max(38, int(len(tag) * 6.5) + 18)
        text_x = cursor_x + pill_w / 2
        parts.append(
            f'  <g>\n'
            f'    <rect x="{cursor_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" '
            f'rx="2" fill="{PALETTE["bg_header"]}" stroke="{accent}" '
            f'stroke-opacity="0.55" stroke-width="1"/>\n'
            f'    <text x="{text_x:.1f}" y="184" text-anchor="middle" '
            f'font-family="{FONT_MONO}" font-size="10" font-weight="600" '
            f'fill="{PALETTE["white"]}">{escape_xml(tag)}</text>\n'
            f'  </g>'
        )
        cursor_x += pill_w + gap

    return '\n'.join(parts)


def build_tivano_svg() -> str:
    accent = PALETTE['dora_blue']
    frame = render_terminal_frame(
        CARD_WIDTH,
        CARD_HEIGHT,
        'GADGET #01',
        right_tag='[PINNED]',
        accent=accent,
    )
    stage = _render_stage_box('MINI-DORA SWARM', accent)

    red_dora = render_sprite(
        MINI_DORA_GRID,
        {
            'C': PALETTE['dora_red'],
            'D': PALETTE['dora_red_dark'],
            'W': PALETTE['white'],
            'B': PALETTE['bg'],
            'N': PALETTE['dora_red'],
            'R': PALETTE['dora_red_dark'],
            'G': PALETTE['dora_gold'],
        },
        x=24,
        y=56,
        px=3,
    )
    blue_dora = render_sprite(
        MINI_DORA_GRID,
        {
            'C': PALETTE['dora_blue'],
            'D': PALETTE['dora_blue_dark'],
            'W': PALETTE['white'],
            'B': PALETTE['bg'],
            'N': PALETTE['dora_red'],
            'R': PALETTE['dora_red'],
            'G': PALETTE['dora_gold'],
        },
        x=82,
        y=46,
        px=3,
    )
    green_dora = render_sprite(
        MINI_DORA_GRID,
        {
            'C': PALETTE['green_mid'],
            'D': PALETTE['green_dim'],
            'W': PALETTE['white'],
            'B': PALETTE['bg'],
            'N': PALETTE['dora_red'],
            'R': PALETTE['dora_red'],
            'G': PALETTE['dora_gold'],
        },
        x=140,
        y=58,
        px=3,
    )

    weather_sprite = render_sprite(
        WEATHER_GRID,
        {
            'O': PALETTE['dora_gold_dark'],
            'Y': PALETTE['dora_gold'],
            'W': PALETTE['white'],
            'B': PALETTE['dora_blue'],
            'L': PALETTE['dora_blue_light'],
        },
        x=211,
        y=61,
        px=3,
    )

    connectors = '\n'.join([
        f'  <path class="tv-circuit" d="M 58 71 H 69 V 61 H 81" '
        f'fill="none" stroke="{PALETTE["green"]}" stroke-width="2" '
        f'stroke-dasharray="4 3" stroke-linecap="square"/>',
        f'  <path class="tv-circuit tv-circuit-b" d="M 116 61 H 128 V 73 H 139" '
        f'fill="none" stroke="{PALETTE["green"]}" stroke-width="2" '
        f'stroke-dasharray="4 3" stroke-linecap="square"/>',
        f'  <path class="tv-circuit tv-circuit-c" d="M 40 88 V 95 H 156 V 89" '
        f'fill="none" stroke="{PALETTE["green_soft"]}" stroke-width="1.5" '
        f'stroke-dasharray="3 3" stroke-linecap="square"/>',
        f'  <path class="tv-circuit tv-circuit-b" d="M 174 73 H 197" '
        f'fill="none" stroke="{PALETTE["green"]}" stroke-width="2" '
        f'stroke-dasharray="4 3" stroke-linecap="square"/>',
        f'  <rect x="67" y="59" width="4" height="4" fill="{PALETTE["green"]}" class="tv-node"/>',
        f'  <rect x="126" y="71" width="4" height="4" fill="{PALETTE["green"]}" class="tv-node"/>',
    ])

    weather_window = '\n'.join([
        f'  <rect x="198" y="54" width="68" height="44" rx="2" '
        f'fill="{PALETTE["bg_panel"]}" stroke="{PALETTE["dora_blue_light"]}" '
        f'stroke-opacity="0.5" stroke-width="1"/>',
        f'  <rect x="199" y="55" width="66" height="4" fill="{PALETTE["dora_blue_dark"]}" opacity="0.55"/>',
        f'  <g class="tv-weather">\n{weather_sprite}\n  </g>',
    ])

    text_block = _render_text_block(
        'TIVANO',
        PALETTE['dora_blue_light'],
        'Native macOS agent workspace',
        'Worktree sub-agents & Weather',
    )
    pills = _render_pill_bar(['Swift 87%', 'Python', 'macOS'], accent)

    styles = '\n'.join([
        '    @keyframes tv-circuit-pulse {',
        '      0% { stroke-dashoffset: 14; opacity: 0.55; }',
        '      50% { stroke-dashoffset: 7; opacity: 1; }',
        '      100% { stroke-dashoffset: 0; opacity: 0.55; }',
        '    }',
        '    @keyframes tv-bob {',
        '      0%, 100% { transform: translateY(0px); }',
        '      50% { transform: translateY(-2.5px); }',
        '    }',
        '    @keyframes tv-node-blink {',
        '      0%, 100% { opacity: 0.4; }',
        '      50% { opacity: 1; }',
        '    }',
        '    .tv-circuit { animation: tv-circuit-pulse 1.8s linear infinite; }',
        '    .tv-circuit-b { animation-delay: 0.45s; }',
        '    .tv-circuit-c { animation-delay: 0.9s; }',
        '    .tv-node { animation: tv-node-blink 1.4s ease-in-out infinite; }',
        '    .tv-dora-1 { animation: tv-bob 2.8s ease-in-out infinite; }',
        '    .tv-dora-2 { animation: tv-bob 2.8s ease-in-out 0.4s infinite; }',
        '    .tv-dora-3 { animation: tv-bob 2.8s ease-in-out 0.8s infinite; }',
        '    .tv-weather { animation: tv-bob 3.2s ease-in-out 0.2s infinite; }',
    ])

    body = '\n'.join([
        frame,
        stage,
        connectors,
        f'  <g class="tv-dora-1">\n{red_dora}\n  </g>',
        f'  <g class="tv-dora-2">\n{blue_dora}\n  </g>',
        f'  <g class="tv-dora-3">\n{green_dora}\n  </g>',
        weather_window,
        text_block,
        pills,
    ])
    return _wrap_svg('Tivano pinned repository gadget card', styles, body)


def build_token_taken_svg() -> str:
    accent = PALETTE['dora_gold']
    frame = render_terminal_frame(
        CARD_WIDTH,
        CARD_HEIGHT,
        'GADGET #02',
        right_tag='[PINNED]',
        accent=accent,
    )
    stage = _render_stage_box('LIQUID GLASS METER', accent)

    # Clip path slices the 7 animated bars into crisp 4px-tall pixel segments (y=59..93).
    segment_ys = [59, 65, 71, 77, 83, 89]
    clip_rects = '\n'.join(
        f'      <rect x="36" y="{sy}" width="146" height="4"/>'
        for sy in segment_ys
    )
    defs = (
        '    <clipPath id="tt-meter-clip">\n'
        f'{clip_rects}\n'
        '    </clipPath>\n'
        '    <linearGradient id="tt-bar-grad" x1="0" y1="1" x2="0" y2="0">\n'
        f'      <stop offset="0%" stop-color="{PALETTE["green"]}"/>\n'
        f'      <stop offset="65%" stop-color="{PALETTE["green_soft"]}"/>\n'
        f'      <stop offset="100%" stop-color="{PALETTE["dora_blue_light"]}"/>\n'
        '    </linearGradient>'
    )

    glass_frame = '\n'.join([
        f'  <rect x="24" y="52" width="170" height="46" rx="3" '
        f'fill="{PALETTE["dora_blue_light"]}" fill-opacity="0.08" '
        f'stroke="{PALETTE["dora_blue_light"]}" stroke-opacity="0.48" stroke-width="1"/>',
        f'  <rect x="26" y="53" width="166" height="1" fill="{PALETTE["white"]}" opacity="0.32"/>',
        f'  <polygon points="30,54 46,54 36,96 26,96" fill="{PALETTE["white"]}" opacity="0.06"/>',
        f'  <polygon points="154,54 164,54 154,96 144,96" fill="{PALETTE["white"]}" opacity="0.04"/>',
        f'  <rect x="24" y="52" width="5" height="2" fill="{PALETTE["dora_gold"]}"/>',
        f'  <rect x="24" y="52" width="2" height="5" fill="{PALETTE["dora_gold"]}"/>',
        f'  <rect x="189" y="96" width="5" height="2" fill="{PALETTE["dora_gold"]}"/>',
        f'  <rect x="192" y="93" width="2" height="5" fill="{PALETTE["dora_gold"]}"/>',
    ])

    bar_xs = [39 + idx * 21 for idx in range(7)]
    bg_tracks = '\n'.join(
        f'    <rect x="{bx}" y="59" width="14" height="34" fill="{PALETTE["green_dim"]}" opacity="0.35"/>'
        for bx in bar_xs
    )
    active_bars = '\n'.join(
        f'    <g transform="translate({bx}, 93)">\n'
        f'      <rect class="tt-bar tt-bar-{idx + 1}" x="0" y="-34" width="14" height="34" '
        f'fill="url(#tt-bar-grad)"/>\n'
        f'    </g>'
        for idx, bx in enumerate(bar_xs)
    )
    meter_bars = '\n'.join([
        '  <g clip-path="url(#tt-meter-clip)">',
        bg_tracks,
        active_bars,
        '  </g>',
    ])

    dorayaki_coin = render_sprite(
        DORAYAKI_COIN_GRID,
        {
            'D': PALETTE['dorayaki_dark'],
            'B': PALETTE['dorayaki_brown'],
            'C': PALETTE['dorayaki_cream'],
            'G': PALETTE['dora_gold'],
            'Y': PALETTE['dora_gold_dark'],
            'W': PALETTE['white'],
        },
        x=216,
        y=62,
        px=3,
    )
    sparkle_top = render_sprite(
        SPARKLE_GRID,
        {'W': PALETTE['white'], 'G': PALETTE['dora_gold']},
        x=252,
        y=55,
        px=2,
    )
    sparkle_bottom = render_sprite(
        SPARKLE_GRID,
        {'W': PALETTE['dora_gold'], 'G': PALETTE['white']},
        x=204,
        y=88,
        px=2,
    )
    dorayaki_group = '\n'.join([
        f'  <g class="tt-coin">\n{dorayaki_coin}\n  </g>',
        f'  <g class="tt-gleam-a">\n{sparkle_top}\n  </g>',
        f'  <g class="tt-gleam-b">\n{sparkle_bottom}\n  </g>',
    ])

    text_block = _render_text_block(
        'TOKEN TAKEN',
        PALETTE['dora_gold'],
        'Local-first token dashboard',
        'macOS, CLI & 16+ harnesses',
    )
    pills = _render_pill_bar(['Swift', 'CLI', 'Liquid Glass'], accent)

    styles = '\n'.join([
        '    @keyframes tt-meter-wave {',
        '      0%, 100% { transform: scaleY(0.32); }',
        '      50% { transform: scaleY(1.0); }',
        '    }',
        '    @keyframes tt-coin-bob {',
        '      0%, 100% { transform: translateY(0px); }',
        '      50% { transform: translateY(-3px); }',
        '    }',
        '    @keyframes tt-gleam {',
        '      0%, 100% { opacity: 0.25; }',
        '      50% { opacity: 1; }',
        '    }',
        '    .tt-bar { animation: tt-meter-wave 1.9s ease-in-out infinite; }',
        '    .tt-bar-1 { animation-delay: 0.00s; }',
        '    .tt-bar-2 { animation-delay: 0.22s; }',
        '    .tt-bar-3 { animation-delay: 0.44s; }',
        '    .tt-bar-4 { animation-delay: 0.66s; }',
        '    .tt-bar-5 { animation-delay: 0.88s; }',
        '    .tt-bar-6 { animation-delay: 1.10s; }',
        '    .tt-bar-7 { animation-delay: 1.32s; }',
        '    .tt-coin { animation: tt-coin-bob 2.6s ease-in-out infinite; }',
        '    .tt-gleam-a { animation: tt-gleam 1.6s ease-in-out infinite; }',
        '    .tt-gleam-b { animation: tt-gleam 1.6s ease-in-out 0.8s infinite; }',
    ])

    body = '\n'.join([
        frame,
        stage,
        glass_frame,
        meter_bars,
        dorayaki_group,
        text_block,
        pills,
    ])
    return _wrap_svg('Token Taken pinned repository gadget card', styles, body, defs=defs)


def build_h2os_svg() -> str:
    accent = PALETTE['dora_red']
    frame = render_terminal_frame(
        CARD_WIDTH,
        CARD_HEIGHT,
        'GADGET #03',
        right_tag='[PINNED]',
        accent=accent,
    )
    stage = _render_stage_box('HYDROGEN MARK', accent)

    v_grid = '\n'.join(
        f'    <line x1="{gx}" y1="37" x2="{gx}" y2="103"/>'
        for gx in range(26, 276, 16)
    )
    h_grid = '\n'.join(
        f'    <line x1="15" y1="{gy}" x2="275" y2="{gy}"/>'
        for gy in range(44, 104, 12)
    )
    grid_lines = '\n'.join([
        f'  <g stroke="{PALETTE["border"]}" stroke-width="1" opacity="0.42">',
        v_grid,
        h_grid,
        '  </g>',
        f'  <rect x="24" y="52" width="242" height="46" rx="2" '
        f'fill="none" stroke="{PALETTE["border_bright"]}" stroke-opacity="0.5" stroke-width="1"/>',
        f'  <rect x="24" y="52" width="3" height="46" fill="{PALETTE["dora_red"]}" opacity="0.85"/>',
        f'  <rect x="24" y="52" width="8" height="2" fill="{PALETTE["door_pink"]}" opacity="0.7"/>',
        f'  <rect x="258" y="96" width="8" height="2" fill="{PALETTE["door_pink"]}" opacity="0.7"/>',
    ])

    square = render_sprite(
        HYDROGEN_SQUARE_GRID,
        {'W': PALETTE['white']},
        x=38,
        y=57,
        px=3,
    )
    circle = render_sprite(
        HYDROGEN_CIRCLE_GRID,
        {'W': PALETTE['white']},
        x=96,
        y=57,
        px=3,
    )
    triangle = render_sprite(
        HYDROGEN_TRIANGLE_GRID,
        {'W': PALETTE['white']},
        x=154,
        y=57,
        px=3,
    )

    signal_core = render_sprite(
        SIGNAL_CORE_GRID,
        {'R': PALETTE['dora_red'], 'H': PALETTE['white']},
        x=229,
        y=70,
        px=3,
    )
    signal_ring = render_sprite(
        SIGNAL_RING_GRID,
        {'R': PALETTE['dora_red']},
        x=226,
        y=67,
        px=3,
    )

    guide_ticks = '\n'.join([
        f'  <rect x="54" y="95" width="4" height="2" fill="{PALETTE["muted"]}"/>',
        f'  <rect x="112" y="95" width="4" height="2" fill="{PALETTE["muted"]}"/>',
        f'  <rect x="171" y="95" width="4" height="2" fill="{PALETTE["muted"]}"/>',
        f'  <line x1="208" y1="58" x2="208" y2="92" stroke="{PALETTE["border_bright"]}" '
        f'stroke-width="1" stroke-dasharray="2 2"/>',
    ])

    text_block = _render_text_block(
        'H2 OS',
        PALETTE['white'],
        'Geometric light Obsidian theme',
        'HydrogenOS writing discipline',
    )
    pills = _render_pill_bar(['CSS', 'Obsidian', 'Design'], accent)

    styles = '\n'.join([
        '    @keyframes h2-geo-float {',
        '      0%, 100% { transform: translateY(0px); opacity: 0.78; }',
        '      50% { transform: translateY(-2px); opacity: 1; }',
        '    }',
        '    @keyframes h2-signal-pulse {',
        '      0%, 100% { opacity: 0.35; }',
        '      50% { opacity: 1; }',
        '    }',
        '    @keyframes h2-ring-pulse {',
        '      0%, 100% { opacity: 0.15; }',
        '      50% { opacity: 0.85; }',
        '    }',
        '    .h2-geo-1 { animation: h2-geo-float 3.4s ease-in-out infinite; }',
        '    .h2-geo-2 { animation: h2-geo-float 3.4s ease-in-out 0.55s infinite; }',
        '    .h2-geo-3 { animation: h2-geo-float 3.4s ease-in-out 1.1s infinite; }',
        '    .h2-signal-core { animation: h2-signal-pulse 1.8s ease-in-out infinite; }',
        '    .h2-signal-ring { animation: h2-ring-pulse 1.8s ease-in-out 0.25s infinite; }',
    ])

    body = '\n'.join([
        frame,
        stage,
        grid_lines,
        guide_ticks,
        f'  <g class="h2-geo-1">\n{square}\n  </g>',
        f'  <g class="h2-geo-2">\n{circle}\n  </g>',
        f'  <g class="h2-geo-3">\n{triangle}\n  </g>',
        f'  <g class="h2-signal-ring">\n{signal_ring}\n  </g>',
        f'  <g class="h2-signal-core">\n{signal_core}\n  </g>',
        text_block,
        pills,
    ])
    return _wrap_svg('H2OS pinned repository gadget card', styles, body)


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        'gadget-tivano.svg': build_tivano_svg(),
        'gadget-token-taken.svg': build_token_taken_svg(),
        'gadget-h2os.svg': build_h2os_svg(),
    }
    for filename, svg in outputs.items():
        (ASSETS_DIR / filename).write_text(svg, encoding='utf-8')


if __name__ == '__main__':
    main()
