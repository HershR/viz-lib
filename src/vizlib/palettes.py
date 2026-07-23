"""Validated color palettes and chrome tokens for vizlib.

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
        "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
        "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281",
        "#0d366b",
    ),
    # Dark sequential anchors dark -> light (near-zero recedes toward the surface).
    "dark": (
        "#0d366b", "#104281", "#184f95", "#1c5cab", "#256abf", "#2a78d6",
        "#3987e5", "#5598e7", "#6da7ec", "#86b6ef", "#9ec5f4", "#b7d3f6",
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
SURFACE: dict[str, str] = {"light": "#fcfcfb", "dark": "#1a1a19"}
PRIMARY_INK: dict[str, str] = {"light": "#0b0b0b", "dark": "#ffffff"}
SECONDARY_INK: dict[str, str] = {"light": "#52514e", "dark": "#c3c2b7"}
MUTED: dict[str, str] = {"light": "#898781", "dark": "#898781"}
GRIDLINE: dict[str, str] = {"light": "#e1e0d9", "dark": "#2c2c2a"}
BASELINE: dict[str, str] = {"light": "#c3c2b7", "dark": "#383835"}
