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
SURFACE: dict[str, str] = {"light": "#fcfcfb", "dark": "#1a1a19"}
PRIMARY_INK: dict[str, str] = {"light": "#0b0b0b", "dark": "#ffffff"}
SECONDARY_INK: dict[str, str] = {"light": "#52514e", "dark": "#c3c2b7"}
MUTED: dict[str, str] = {"light": "#898781", "dark": "#898781"}
GRIDLINE: dict[str, str] = {"light": "#e1e0d9", "dark": "#2c2c2a"}
BASELINE: dict[str, str] = {"light": "#c3c2b7", "dark": "#383835"}

# Optional per-mode typeface override; modes not listed fall back to sans-serif.
FONT_FAMILY: dict[str, tuple[str, ...]] = {}

# --- "Lime Green" custom theme (ported from a shadcn theme) --------------------
# Signature: the lime `#aff33e` primary drives the accent/emphasis and the leading
# categorical slot. Per request only the primary must be green; the remaining
# categorical hues are a curated, mutually distinct set (tailwind-family, matching
# shadcn's origin). Registered under modes "lime" (light) and "lime-dark".

# Light
CATEGORICAL["lime"] = (
    "#aff33e",  # 1 lime (primary)
    "#3b82f6",  # 2 blue
    "#f97316",  # 3 orange
    "#8b5cf6",  # 4 violet
    "#ec4899",  # 5 pink
    "#14b8a6",  # 6 teal
    "#eab308",  # 7 amber
    "#ef4444",  # 8 red
)
SEQUENTIAL["lime"] = (
    "#f7fee7",
    "#ecfccb",
    "#d9f99d",
    "#bef264",
    "#a3e635",
    "#84cc16",
    "#65a30d",
    "#4d7c0f",
    "#3f6212",
)
DIVERGING["lime"] = ("#ef4444", "#f1f5f9", "#84cc16")
EMPHASIS["lime"] = "#aff33e"
DEEMPHASIS["lime"] = "#94a3b8"
SURFACE["lime"] = "#fbfcf8"
PRIMARY_INK["lime"] = "#0f172a"
SECONDARY_INK["lime"] = "#475569"
MUTED["lime"] = "#94a3b8"
GRIDLINE["lime"] = "#e2e8f0"
BASELINE["lime"] = "#cbd5e1"
FONT_FAMILY["lime"] = ("Inter", "system-ui", "sans-serif")

# Dark (shadcn .dark): brighter hues on a deep slate surface.
CATEGORICAL["lime-dark"] = (
    "#aff33e",  # 1 lime (primary)
    "#60a5fa",  # 2 blue
    "#fb923c",  # 3 orange
    "#a78bfa",  # 4 violet
    "#f472b6",  # 5 pink
    "#2dd4bf",  # 6 teal
    "#fbbf24",  # 7 amber
    "#f87171",  # 8 red
)
SEQUENTIAL["lime-dark"] = (
    "#1a2e05",
    "#3f6212",
    "#4d7c0f",
    "#65a30d",
    "#84cc16",
    "#a3e635",
    "#bef264",
    "#d9f99d",
    "#ecfccb",
)
DIVERGING["lime-dark"] = ("#f87171", "#1e293b", "#a3e635")
EMPHASIS["lime-dark"] = "#aff33e"
DEEMPHASIS["lime-dark"] = "#475569"
SURFACE["lime-dark"] = "#020617"
PRIMARY_INK["lime-dark"] = "#f8fafc"
SECONDARY_INK["lime-dark"] = "#cbd5e1"
MUTED["lime-dark"] = "#64748b"
GRIDLINE["lime-dark"] = "#1e293b"
BASELINE["lime-dark"] = "#334155"
FONT_FAMILY["lime-dark"] = ("Inter", "system-ui", "sans-serif")
