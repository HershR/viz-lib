"""Basic bar chart: a single series, sorted, with the top bar labeled.

Run:  python examples/basic_bar.py
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

# One call, zero styling arguments. sort="desc" orders the bars; label="auto"
# (the default) labels just the largest bar.
ax = viz.bar(sales, x="region", y="revenue", sort="desc", title="Revenue by region")

ax.figure.savefig(IMAGES / "basic_bar.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "basic_bar.png")
