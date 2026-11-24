#!/usr/bin/env python3
"""Generate the 4D Pocket Matrix Telemetry SVG for a GitHub profile."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from pixel_lib import (  # noqa: E402
    FONT_MONO,
    escape_xml,
    get_palette,
    render_pixel_text,
    render_sprite,
    render_terminal_frame,
)

SVG_WIDTH = 900
SVG_HEIGHT = 196
GRAPHQL_ENDPOINT = "https://api.github.com/graphql"

FALLBACK_STATS: dict[str, Any] = {
    "contributions": 777,
    "total_stars": 43,
    "public_repos": 12,
    "languages": [
        ("Swift", 54.0, "#F05138"),
        ("Python", 19.0, "#39FF14"),
        ("CSS", 14.0, "#FF5C93"),
        ("TypeScript", 9.0, "#38BDF8"),
        ("Rust", 4.0, "#FACC15"),
    ],
}

LANGUAGE_COLOR_OVERRIDES: dict[str, str] = {
    "Python": "#39FF14",
    "Swift": "#F05138",
    "CSS": "#FF5C93",
    "TypeScript": "#38BDF8",
    "Rust": "#FACC15",
    "JavaScript": "#F7DF1E",
    "Shell": "#4ADE80",
    "HTML": "#FB923C",
    "Go": "#00ADD8",
}

LIGHT_LANGUAGE_COLOR_OVERRIDES: dict[str, str] = {
    "Python": "#16A34A",
    "JavaScript": "#CA8A04",
    "CSS": "#DB2777",
    "TypeScript": "#0284C7",
    "Swift": "#EA580C",
    "Rust": "#B45309",
    "Shell": "#15803D",
    "HTML": "#EA580C",
    "Go": "#0369A1",
}

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
    publicRepos: repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
}
""".strip()

# 24x20 pixel sprite: Doraemon blue belly torso slice + red collar + gold bell + white 4D pocket
POCKET_SPRITE: list[str] = [
    "......KKKKKKKKKKKK......",
    ".....KRRRRRRRRRRRRK.....",
    ".....KRRRRGGGGGRRRK.....",
    "....KBBBBBGGGGGBBBBK....",
    "...KBBBBBBGKKKGBBBBBK...",
    "..KBBBBBBBBGGGBBBBBBBK..",
    "..KBBBBBWWWWWWWWBBBBBK..",
    ".KBBBBWWWWWWWWWWWWBBBBK.",
    ".KBBBWWWWWWWWWWWWWWBBBK.",
    ".KBBBWWKKKKKKKKKKWWBBBK.",
    ".KBBBWWKDDDDDDDDKWWBBBK.",
    ".KBBBWWKWWWWWWWWKWWBBBK.",
    ".KBBBWWWKWWWWWWKWWWBBBK.",
    ".KBBBWWWWKKKKKKWWWWBBBK.",
    "..KBBBWWWWWWWWWWWWBBBK..",
    "..KBBBBWWWWWWWWWWBBBBK..",
    "...KBBBBBWWWWWWBBBBBK...",
    "...KBBBBBBBBBBBBBBBBK...",
    "....KKKKKKKKKKKKKKKK....",
    "........................",
]

def _build_sprite_color_map(p: dict[str, str]) -> dict[str, str]:
    """Build the 4D Pocket sprite color map from a theme palette."""
    return {
        "K": "#07131D",
        "B": p["dora_blue"],
        "R": p["dora_red"],
        "G": p["bell_gold"],
        "W": p["white"],
        "S": "#CBD5E1",
        "D": p["portal_bg"],
    }


def _resolve_token(offline: bool) -> str | None:
    """Obtain a GitHub token from GITHUB_TOKEN or `gh auth token` unless offline."""
    if offline:
        return None
    env_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if env_token:
        return env_token
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        token = proc.stdout.strip()
        return token or None
    except (OSError, subprocess.SubprocessError):
        return None


def fetch_github_stats(user: str, offline: bool = False) -> dict[str, Any]:
    """Fetch GitHub GraphQL stats or gracefully fall back to the snapshot."""
    token = _resolve_token(offline)
    if not token:
        return dict(FALLBACK_STATS)

    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": user}}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "elijah7x-telemetry-generator/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return dict(FALLBACK_STATS)

    user_data = (data.get("data") or {}).get("user")
    if not user_data:
        return dict(FALLBACK_STATS)

    contributions = int(
        (((user_data.get("contributionsCollection") or {}).get("contributionCalendar") or {}).get("totalContributions"))
        or 0
    )

    repos_block = user_data.get("repositories") or {}
    nodes = repos_block.get("nodes") or []
    public_repos_block = user_data.get("publicRepos") or {}
    public_repos = int(public_repos_block.get("totalCount") or repos_block.get("totalCount") or len(nodes))

    total_stars = sum(int(node.get("stargazerCount") or 0) for node in nodes if isinstance(node, dict))

    lang_totals: dict[str, int] = {}
    lang_colors: dict[str, str] = {}
    for node in nodes:
        if not isinstance(node, dict):
            continue
        edges = ((node.get("languages") or {}).get("edges")) or []
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            size = int(edge.get("size") or 0)
            lang_node = edge.get("node") or {}
            name = str(lang_node.get("name") or "").strip()
            if not name or size <= 0:
                continue
            lang_totals[name] = lang_totals.get(name, 0) + size
            if name not in lang_colors:
                raw_color = str(lang_node.get("color") or "").strip()
                lang_colors[name] = LANGUAGE_COLOR_OVERRIDES.get(name) or raw_color or "#39FF14"

    total_bytes = sum(lang_totals.values())
    if total_bytes <= 0:
        languages = list(FALLBACK_STATS["languages"])
    else:
        sorted_langs = sorted(lang_totals.items(), key=lambda item: item[1], reverse=True)[:5]
        languages = [
            (name, round((byte_count / total_bytes) * 100.0, 1), lang_colors.get(name, "#39FF14"))
            for name, byte_count in sorted_langs
        ]

    return {
        "contributions": contributions,
        "total_stars": total_stars,
        "public_repos": public_repos,
        "languages": languages,
    }


def _resolve_language_color(lang_name: str, raw_color: str, p: dict[str, str], theme: str) -> str:
    """Resolve a high-contrast language accent color for the requested theme."""
    if theme == "light":
        if lang_name in LIGHT_LANGUAGE_COLOR_OVERRIDES:
            return LIGHT_LANGUAGE_COLOR_OVERRIDES[lang_name]
        if raw_color.upper() == "#39FF14":
            return p["telemetry_value"]
        return raw_color
    return LANGUAGE_COLOR_OVERRIDES.get(lang_name) or raw_color or p["green"]


def _render_panel_box(x: int, y: int, width: int, height: int, p: dict[str, str]) -> str:
    """Render a themed Matrix sub-panel with crisp pixel corner ticks."""
    corner = p["border_bright"]
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="4" '
            f'fill="{p["tile_bg"]}" stroke="{p["border"]}" stroke-width="1"/>',
            '<g shape-rendering="crispEdges">',
            f'<rect x="{x}" y="{y}" width="3" height="3" fill="{corner}"/>',
            f'<rect x="{x + width - 3}" y="{y}" width="3" height="3" fill="{corner}"/>',
            f'<rect x="{x}" y="{y + height - 3}" width="3" height="3" fill="{corner}"/>',
            f'<rect x="{x + width - 3}" y="{y + height - 3}" width="3" height="3" fill="{corner}"/>',
            "</g>",
        ]
    )


def _render_pocket_section(p: dict[str, str], use_glow: bool) -> str:
    """Render left section (x=20..215): 4D Pocket sprite, rising Matrix particles, caption."""
    font = escape_xml(FONT_MONO)
    sprite_colors = _build_sprite_color_map(p)

    parts: list[str] = [
        '<g id="section-pocket">',
        _render_panel_box(20, 40, 195, 140, p),
        render_sprite(POCKET_SPRITE, sprite_colors, x=69, y=72, px=4),
    ]

    # Small 3x3 Matrix pixels rising well-spaced vertically above the pocket opening (y=108..116)
    particles = [
        (100, 98, 3, p["green"], "0s", "2.4s"),
        (122, 90, 3, p["green"], "-0.6s", "2.6s"),
        (108, 80, 3, p["green"], "-1.2s", "2.2s"),
        (127, 72, 3, p["green"], "-1.8s", "2.5s"),
        (114, 62, 3, p["green"], "-0.9s", "2.3s"),
    ]
    particle_attr = 'filter="url(#matrix-glow)"' if use_glow else 'shape-rendering="crispEdges"'
    for px_x, px_y, size, color, delay, dur in particles:
        parts.append(
            f'<rect x="{px_x}" y="{px_y}" width="{size}" height="{size}" '
            f'fill="{color}" style="animation: pocket-rise {dur} linear {delay} infinite;" '
            f'{particle_attr}/>'
        )

    parts.append(
        f'<text x="117" y="168" text-anchor="middle" fill="{p["telemetry_value"]}" '
        f'font-family="{font}" font-size="10.5" font-weight="700" '
        f'letter-spacing="1.2">4D-POCKET // LIVE</text>'
    )
    parts.append("</g>")
    return "\n".join(parts)


def _render_metric_tiles(stats: dict[str, Any], p: dict[str, str], use_glow: bool) -> str:
    """Render middle section (x=232..516): 2x2 pixel metric tiles."""
    font = escape_xml(FONT_MONO)

    top_lang = stats["languages"][0][0] if stats.get("languages") else "Swift"
    if len(top_lang) > 11:
        top_lang = top_lang[:10] + "…"

    tiles = [
        (232, 40, "CONTRIBUTIONS (1Y)", f"{int(stats['contributions']):,}"),
        (379, 40, "TOTAL STARS", f"{int(stats['total_stars']):,}"),
        (232, 114, "PUBLIC REPOS", f"{int(stats['public_repos']):,}"),
        (379, 114, "TOP LANGUAGE", top_lang),
    ]

    parts: list[str] = ['<g id="section-metrics">']
    tile_w = 137
    tile_h = 66
    glow_attr = 'filter="url(#matrix-glow)" ' if use_glow else ""
    for idx, (tx, ty, label, value) in enumerate(tiles):
        cx = tx + tile_w // 2
        val_size = 21 if len(value) <= 6 else (17 if len(value) <= 9 else 14.5)
        delay = f"{idx * 0.35:.2f}s"

        parts.append(_render_panel_box(tx, ty, tile_w, tile_h, p))
        parts.append(
            f'<text x="{cx}" y="{ty + 20}" text-anchor="middle" fill="{p["text_secondary"]}" '
            f'font-family="{font}" font-size="9" font-weight="600" '
            f'letter-spacing="0.6">{escape_xml(label)}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{ty + 49}" text-anchor="middle" fill="{p["telemetry_value"]}" '
            f'font-family="{font}" font-size="{val_size}" font-weight="800" '
            f'{glow_attr}style="animation: pulse-glow 3.2s ease-in-out {delay} infinite;">'
            f'{escape_xml(value)}</text>'
        )

    parts.append("</g>")
    return "\n".join(parts)


def _render_language_matrix(
    languages: list[tuple[str, float, str]],
    p: dict[str, str],
    theme: str,
) -> str:
    """Render right section (x=538..878): LANGUAGE MATRIX header + 5 discrete 16-block bars."""
    font = escape_xml(FONT_MONO)

    parts: list[str] = [
        '<g id="section-languages">',
        _render_panel_box(538, 40, 340, 140, p),
        render_pixel_text("LANGUAGE MATRIX", x=550, y=47, px=2, fill=p["telemetry_value"], letter_spacing=1),
        f'<text x="866" y="58" text-anchor="end" fill="{p["text_secondary"]}" '
        f'font-family="{font}" font-size="9" opacity="0.8">TOP 5</text>',
        f'<line x1="550" y1="65" x2="866" y2="65" stroke="{p["border"]}" stroke-width="1"/>',
    ]

    segments = 16
    seg_w = 8
    seg_h = 10
    seg_gap = 3
    bar_x = 644
    unlit_color = p["unlit_block"]

    for row_idx, (lang_name, pct, raw_color) in enumerate(languages[:5]):
        row_y = 76 + row_idx * 20
        display_name = lang_name if len(lang_name) <= 11 else lang_name[:10] + "…"
        lit_count = max(1, min(segments, round((pct / 100.0) * segments))) if pct > 0 else 0
        color = _resolve_language_color(lang_name, raw_color, p, theme)

        parts.append(
            f'<text x="550" y="{row_y + 9}" fill="{p["text_primary"]}" font-family="{font}" '
            f'font-size="10.5" font-weight="600">{escape_xml(display_name)}</text>'
        )

        for seg_idx in range(segments):
            sx = bar_x + seg_idx * (seg_w + seg_gap)
            is_lit = seg_idx < lit_count
            if is_lit:
                shimmer_delay = f"{(row_idx * 0.18 + seg_idx * 0.05):.2f}s"
                parts.append(
                    f'<rect x="{sx}" y="{row_y}" width="{seg_w}" height="{seg_h}" rx="1" '
                    f'fill="{escape_xml(color)}" '
                    f'style="animation: seg-shimmer 2.8s ease-in-out {shimmer_delay} infinite;"/>'
                )
            else:
                parts.append(
                    f'<rect x="{sx}" y="{row_y}" width="{seg_w}" height="{seg_h}" rx="1" fill="{unlit_color}"/>'
                )

        parts.append(
            f'<text x="866" y="{row_y + 9}" text-anchor="end" fill="{escape_xml(color)}" '
            f'font-family="{font}" font-size="10" font-weight="700">{pct:.1f}%</text>'
        )

    parts.append("</g>")
    return "\n".join(parts)


def build_telemetry_svg(
    user: str,
    stats: dict[str, Any],
    sync_date: str | None = None,
    theme: str = "dark",
) -> str:
    """Build the complete 900x196 Matrix Telemetry SVG string for the given theme."""
    if sync_date is None:
        sync_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    p = get_palette(theme)
    use_glow = p["telemetry_glow"] != "0"

    title = f"{user}@4d-pocket:~/telemetry"
    right_tag = f"SYNC: {sync_date} UTC"

    defs_block = (
        """<defs>
  <filter id="matrix-glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2.0" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
"""
        if use_glow
        else ""
    )

    defs_and_styles = f"""{defs_block}<style>
  @keyframes pocket-rise {{
    0% {{ transform: translateY(4px); opacity: 0; }}
    20% {{ opacity: 0.95; }}
    80% {{ opacity: 0.75; }}
    100% {{ transform: translateY(-18px); opacity: 0; }}
  }}
  @keyframes pulse-glow {{
    0%, 100% {{ opacity: 0.92; }}
    50% {{ opacity: 1; }}
  }}
  @keyframes seg-shimmer {{
    0%, 100% {{ opacity: 0.85; }}
    50% {{ opacity: 1; }}
  }}
</style>"""

    frame = render_terminal_frame(
        SVG_WIDTH,
        SVG_HEIGHT,
        title=title,
        right_tag=right_tag,
        accent=p["green_mid"],
        theme=theme,
    )

    body = "\n".join(
        [
            _render_pocket_section(p, use_glow),
            _render_metric_tiles(stats, p, use_glow),
            _render_language_matrix(stats["languages"], p, theme),
        ]
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" role="img" '
        f'aria-label="{escape_xml(title)}">\n'
        f"{defs_and_styles}\n"
        f"{frame}\n"
        f"{body}\n"
        f"</svg>\n"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    default_output = SCRIPT_DIR.parent / "assets" / "matrix-telemetry.svg"
    default_output_light = SCRIPT_DIR.parent / "assets" / "matrix-telemetry-light.svg"
    parser = argparse.ArgumentParser(description="Generate Matrix x Doraemon 4D Pocket telemetry SVGs.")
    parser.add_argument("--user", default="elijah7x", help="GitHub username to query (default: elijah7x)")
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help=f"Output dark-theme SVG path (default: {default_output})",
    )
    parser.add_argument(
        "--output-light",
        type=Path,
        default=default_output_light,
        help=f"Output light-theme SVG path (default: {default_output_light})",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip GitHub GraphQL API and use realistic fallback snapshot stats",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    args = parse_args(argv)
    stats = fetch_github_stats(args.user, offline=args.offline)
    sync_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    dark_svg = build_telemetry_svg(args.user, stats, sync_date=sync_date, theme="dark")
    light_svg = build_telemetry_svg(args.user, stats, sync_date=sync_date, theme="light")

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dark_svg, encoding="utf-8")

    light_output_path: Path = args.output_light
    light_output_path.parent.mkdir(parents=True, exist_ok=True)
    light_output_path.write_text(light_svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
