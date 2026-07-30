"""The built-in "shadcn" theme — the shadcn charts aesthetic.

`theme="shadcn"` / `theme="shadcn-dark"` render vizlib's validated palette with the
shadcn look: rounded bar ends, no axis spines, a faint horizontal-only grid, and
muted labels. Only the chrome/shape changes — the colorblind-safe palette is intact.

Run:  python examples/theme_shadcn.py
"""

from pathlib import Path

import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

sales = pd.DataFrame(
    {
        "region": ["North", "South", "East", "West", "Central"],
        "revenue": [120_000, 90_000, 150_000, 60_000, 105_000],
    }
)
survey = pd.DataFrame(
    {
        "quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3", "Q4", "Q4"],
        "channel": ["Web", "Store"] * 4,
        "responses": [30, 18, 42, 25, 38, 30, 45, 33],
    }
)
usage = pd.DataFrame(
    {
        "month": list(range(1, 9)) * 2,
        "plan": ["Pro"] * 8 + ["Free"] * 8,
        "active_users": [5, 9, 14, 21, 25, 30, 38, 46, 20, 24, 27, 30, 34, 36, 41, 44],
    }
)


def save(ax, name, dark=False):
    surface = viz.SHADCN_DARK.surface if dark else viz.SHADCN.surface
    ax.figure.set_facecolor(surface)
    ax.figure.savefig(IMAGES / name, dpi=120, bbox_inches="tight", facecolor=surface)
    print("wrote", IMAGES / name)


# Light: rounded bars, borderless.
save(
    viz.bar(
        sales,
        x="region",
        y="revenue",
        sort="desc",
        theme="shadcn",
        title="Revenue by region",
    ),
    "shadcn_bar.png",
)
save(
    viz.bar(
        survey,
        x="quarter",
        y="responses",
        by="channel",
        theme="shadcn",
        title="Responses by channel",
    ),
    "shadcn_grouped.png",
)

# Dark: the same look on the deep surface.
save(
    viz.line(
        usage,
        x="month",
        y="active_users",
        by="plan",
        theme="shadcn-dark",
        title="Active users by plan",
    ),
    "shadcn_dark_line.png",
    dark=True,
)
