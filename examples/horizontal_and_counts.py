"""Horizontal bars, and counting rows when you omit `y`.

Run:  python examples/horizontal_and_counts.py
"""

from pathlib import Path

import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

# Horizontal is better for long category names; combine with sort.
teams = pd.DataFrame(
    {
        "team": ["Platform", "Growth", "Data Science", "Infrastructure", "Design"],
        "tickets": [48, 31, 22, 55, 17],
    }
)
ax = viz.bar(
    teams,
    x="team",
    y="tickets",
    horizontal=True,
    sort="desc",
    title="Open tickets by team",
)
ax.figure.savefig(IMAGES / "horizontal_bar.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "horizontal_bar.png")

# Omit `y` and vizlib counts rows per category — a frequency chart.
survey = pd.DataFrame({"grade": list("AABBBCADBBAACB")})
ax = viz.bar(survey, x="grade", sort="desc", title="Grade distribution (row counts)")
ax.figure.savefig(IMAGES / "counts.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "counts.png")
