"""Validated color palettes and chrome tokens for chartcn.

The categorical palette is eight hues in a **fixed, colorblind-safe order** — the
order is the safety mechanism (adjacent-pair separation under simulated
protanopia/deuteranopia) and is never re-cycled or re-ranked. Beyond eight series
the tail is folded into "Other" rather than generating a ninth hue.

Each palette is keyed by mode ("light" / "dark"). The dark column is the same hues
re-stepped for the dark surface, not a separate palette.
"""

from __future__ import annotations

# --- Categorical: eight hues, fixed order --------------------------------------
CATEGORICAL: dict[str, tuple[str, ...]] = {
    "light": (
        "#2a78d6",  # 1 blue
        "#eb6834",  # 2 orange
        "#1baf7a",  # 3 aqua
        "#eda100",  # 4 yellow
        "#e87ba4",  # 5 magenta
        "#008300",  # 6 green
        "#4a3aa7",  # 7 violet
        "#e34948",  # 8 red
    ),
    "dark": (
        "#3987e5",  # 1 blue
        "#d95926",  # 2 orange
        "#199e70",  # 3 aqua
        "#c98500",  # 4 yellow
        "#d55181",  # 5 magenta
        "#008300",  # 6 green
        "#9085e9",  # 7 violet
        "#e66767",  # 8 red
    ),
}

# --- Sequential: single hue (blue), light -> dark ------------------------------
SEQUENTIAL: dict[str, tuple[str, ...]] = {
    "light": (
        "#cde2fb",
        "#b7d3f6",
        "#9ec5f4",
        "#86b6ef",
        "#6da7ec",
        "#5598e7",
        "#3987e5",
        "#2a78d6",
        "#256abf",
        "#1c5cab",
        "#184f95",
        "#104281",
        "#0d366b",
    ),
    # Dark sequential anchors dark -> light (near-zero recedes toward the surface).
    "dark": (
        "#0d366b",
        "#104281",
        "#184f95",
        "#1c5cab",
        "#256abf",
        "#2a78d6",
        "#3987e5",
        "#5598e7",
        "#6da7ec",
        "#86b6ef",
        "#9ec5f4",
        "#b7d3f6",
        "#cde2fb",
    ),
}

# --- Diverging: blue <-> red poles, neutral gray midpoint ----------------------
DIVERGING: dict[str, tuple[str, str, str]] = {
    # (low pole, neutral midpoint, high pole)
    "light": ("#2a78d6", "#f0efec", "#e34948"),
    "dark": ("#3987e5", "#383835", "#e66767"),
}

# --- Emphasis: highlighted -> slot-1 accent; rest -> muted gray ----------------
EMPHASIS: dict[str, str] = {"light": "#2a78d6", "dark": "#3987e5"}
DEEMPHASIS: dict[str, str] = {"light": "#898781", "dark": "#898781"}

# --- Chrome & ink tokens -------------------------------------------------------
# The default "light"/"dark" modes wear the shadcn look — pure-white / near-black
# card surfaces and zinc neutrals (see legacy/shadcnStyle.md). The categorical palette above
# stays chartcn's validated colorblind-safe set.
SURFACE: dict[str, str] = {"light": "#ffffff", "dark": "#101010"}
PRIMARY_INK: dict[str, str] = {"light": "#0a0a0a", "dark": "#fafafa"}
SECONDARY_INK: dict[str, str] = {"light": "#71717a", "dark": "#a1a1aa"}
MUTED: dict[str, str] = {"light": "#a1a1aa", "dark": "#71717a"}
GRIDLINE: dict[str, str] = {"light": "#e4e4e7", "dark": "#181818"}
BASELINE: dict[str, str] = {"light": "#e4e4e7", "dark": "#181818"}

# Optional per-mode typeface override; modes not listed fall back to sans-serif.
# shadcn uses Inter/Geist; Liberation Sans is the installed Arial-metric match.
# (No "Arial" in the list — it isn't installed here and spams findfont warnings.)
_SHADCN_FONT = ("Liberation Sans", "DejaVu Sans", "sans-serif")
FONT_FAMILY: dict[str, tuple[str, ...]] = {
    "light": _SHADCN_FONT,
    "dark": _SHADCN_FONT,
}

# --- "classic" modes: the original chartcn look (validated palette + classic chrome:
# hairline spines, a visible value axis, square bars, the default sans). Same
# categorical/sequential/diverging as light/dark; only the neutrals differ.
for _m, _base in (("classic", "light"), ("classic-dark", "dark")):
    CATEGORICAL[_m] = CATEGORICAL[_base]
    SEQUENTIAL[_m] = SEQUENTIAL[_base]
    DIVERGING[_m] = DIVERGING[_base]
    EMPHASIS[_m] = EMPHASIS[_base]
DEEMPHASIS["classic"] = "#898781"
DEEMPHASIS["classic-dark"] = "#898781"
SURFACE["classic"] = "#fcfcfb"
SURFACE["classic-dark"] = "#1a1a19"
PRIMARY_INK["classic"] = "#0b0b0b"
PRIMARY_INK["classic-dark"] = "#ffffff"
SECONDARY_INK["classic"] = "#52514e"
SECONDARY_INK["classic-dark"] = "#c3c2b7"
MUTED["classic"] = "#898781"
MUTED["classic-dark"] = "#898781"
GRIDLINE["classic"] = "#e1e0d9"
GRIDLINE["classic-dark"] = "#2c2c2a"
BASELINE["classic"] = "#c3c2b7"
BASELINE["classic-dark"] = "#383835"
