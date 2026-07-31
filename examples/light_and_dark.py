"""Light and dark mode — the default shadcn look in both.

vizlib renders the shadcn aesthetic by default (rounded bars, no axis spines, hidden
value axis, faint grid) over the validated colorblind-safe palette. The default theme
is `light`; `theme="dark"` (or `viz.set_theme("dark")`) gives the dark card.

Run:  python examples/light_and_dark.py
"""

from pathlib import Path

import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

revenue = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "visitors": [186, 305, 237, 173, 209, 264],
    }
)


def save(ax, name, theme):
    surface = viz.DARK.surface if theme == "dark" else viz.LIGHT.surface
    ax.figure.set_facecolor(surface)
    ax.figure.savefig(IMAGES / name, dpi=120, bbox_inches="tight", facecolor=surface)
    print("wrote", IMAGES / name)


# Default look (light) — no theme argument needed.
save(
    viz.bar(
        revenue,
        x="month",
        y="visitors",
        title="Bar chart",
        subtitle="January - June 2024",
    ),
    "light_mode.png",
    "light",
)

# Dark mode — same chart, theme="dark".
save(
    viz.bar(
        revenue,
        x="month",
        y="visitors",
        theme="dark",
        title="Bar chart",
        subtitle="January - June 2024",
    ),
    "dark_mode.png",
    "dark",
)
