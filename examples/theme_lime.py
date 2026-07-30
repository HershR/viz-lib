"""The built-in "Lime Green" theme (ported from a shadcn theme).

`theme="lime"` / `theme="lime-dark"` render a lime primary/accent over light and
dark surfaces. Single-series charts and the first series use the lime primary; the
rest of the categorical palette is a curated, distinct set.

Run:  python examples/theme_lime.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

sales = pd.DataFrame(
    {
        "region": ["North", "South", "East", "West", "Central"],
        "revenue": [120_000, 90_000, 150_000, 60_000, 105_000],
    }
)
usage = pd.DataFrame(
    {
        "month": list(range(1, 9)) * 2,
        "plan": ["Pro"] * 8 + ["Free"] * 8,
        "active_users": [5, 9, 14, 21, 25, 30, 38, 46, 20, 24, 27, 30, 34, 36, 41, 44],
    }
)
rng = np.random.default_rng(11)
points = pd.DataFrame(
    {
        "x": rng.normal(50, 12, 90),
        "y": rng.normal(50, 14, 90),
        "segment": rng.choice(["A", "B", "C"], 90),
    }
)


def save(ax, name, dark=False):
    surface = viz.LIME_DARK.surface if dark else viz.LIME.surface
    ax.figure.set_facecolor(surface)
    ax.figure.savefig(IMAGES / name, dpi=120, bbox_inches="tight", facecolor=surface)
    print("wrote", IMAGES / name)


# Light: the lime primary on a single-series bar, and the curated multi-series set.
save(
    viz.bar(
        sales,
        x="region",
        y="revenue",
        sort="desc",
        theme="lime",
        title="Revenue by region (lime)",
    ),
    "lime_bar.png",
)
save(
    viz.bar(
        usage,
        x="month",
        y="active_users",
        by="plan",
        theme="lime",
        title="Active users by plan (lime)",
    ),
    "lime_grouped.png",
)

# Dark: same theme family on the deep slate surface.
save(
    viz.line(
        usage,
        x="month",
        y="active_users",
        by="plan",
        highlight="Pro",
        theme="lime-dark",
        title="Pro is pulling ahead (lime-dark)",
    ),
    "lime_dark_line.png",
    dark=True,
)
save(
    viz.scatter(
        points,
        x="x",
        y="y",
        by="segment",
        theme="lime-dark",
        title="Segments (lime-dark)",
    ),
    "lime_dark_scatter.png",
    dark=True,
)
