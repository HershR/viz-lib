"""Multi-series bars: grouped (default) and stacked, driven by `by=`.

Run:  python examples/grouped_and_stacked.py
"""

from pathlib import Path

import pandas as pd

import chartcn as viz

IMAGES = Path(__file__).parent / "images"

# Tidy (long) data: one row per (quarter, channel).
survey = pd.DataFrame(
    {
        "quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3", "Q4", "Q4"],
        "channel": ["Web", "Store"] * 4,
        "responses": [30, 18, 42, 25, 38, 30, 45, 33],
    }
)

# Grouped: bars sit side by side, one categorical hue per series, with a legend.
ax = viz.bar(
    survey,
    x="quarter",
    y="responses",
    by="channel",
    title="Responses by channel (grouped)",
)
ax.figure.savefig(IMAGES / "grouped_bar.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "grouped_bar.png")

# Stacked: same data, stacked=True. A 2px surface gap separates the segments.
ax = viz.bar(
    survey,
    x="quarter",
    y="responses",
    by="channel",
    stacked=True,
    title="Responses by channel (stacked)",
)
ax.figure.savefig(IMAGES / "stacked_bar.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "stacked_bar.png")
