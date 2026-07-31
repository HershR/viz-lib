"""Emphasis: highlight the one bar that matters, gray the rest.

`highlight=` is the honest answer to "make this clearer" — it colors the selected
category in the accent hue, pushes the rest to a muted gray, drops the legend, and
labels the highlighted bar.

Run:  python examples/emphasis.py
"""

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

ax = viz.bar(
    sales, x="region", y="revenue", highlight="East", title="East leads the quarter"
)

ax.figure.savefig(IMAGES / "emphasis.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "emphasis.png")
