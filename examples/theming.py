"""Theming: the built-in dark theme, a scoped override, and a custom Theme.

Run:  python examples/theming.py
"""

from dataclasses import replace
from pathlib import Path

import pandas as pd

import chartcn as viz

IMAGES = Path(__file__).parent / "images"

sales = pd.DataFrame(
    {
        "region": ["North", "South", "East", "West", "Central"],
        "revenue": [120_000, 90_000, 150_000, 60_000, 105_000],
    }
)

# 1. Per-call theme override — dark, without changing the global default.
ax = viz.bar(
    sales, x="region", y="revenue", sort="desc", theme="dark", title="Dark theme"
)
ax.figure.set_facecolor(viz.DARK.surface)
ax.figure.savefig(
    IMAGES / "theme_dark.png", dpi=120, bbox_inches="tight", facecolor=viz.DARK.surface
)
print("wrote", IMAGES / "theme_dark.png")

# 2. A scoped override with the context manager: everything inside the block
#    uses the dark theme; the previous theme is restored on exit.
with viz.theme("dark"):
    assert viz.get_theme() is viz.DARK
assert viz.get_theme() is viz.LIGHT

# 3. A custom Theme built from a built-in — here, a warm accent for emphasis.
warm = replace(viz.LIGHT, name="warm", emphasis="#eb6834")
ax = viz.bar(
    sales,
    x="region",
    y="revenue",
    highlight="East",
    theme=warm,
    title="Custom theme (warm emphasis)",
)
ax.figure.savefig(IMAGES / "theme_custom.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "theme_custom.png")
