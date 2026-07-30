"""Line charts: a multi-series trend, and the emphasis form.

Run:  python examples/line_trends.py
"""

from pathlib import Path

import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

# Tidy (long) monthly data: one row per (month, plan).
usage = pd.DataFrame(
    {
        "month": list(range(1, 13)) * 2,
        "plan": ["Pro"] * 12 + ["Free"] * 12,
        "active_users": [
            5,
            9,
            14,
            21,
            25,
            30,
            38,
            46,
            52,
            60,
            68,
            74,  # Pro
            20,
            24,
            27,
            30,
            34,
            36,
            41,
            44,
            47,
            51,
            55,
            58,  # Free
        ],
    }
)

# Multiple series: one categorical hue each, with a legend.
ax = viz.line(
    usage, x="month", y="active_users", by="plan", title="Active users by plan"
)
ax.figure.savefig(IMAGES / "line_multi.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "line_multi.png")

# Emphasis: highlight the one series that is the point. The rest go gray, the
# legend is dropped, and only the highlighted line's endpoint is labeled.
ax = viz.line(
    usage,
    x="month",
    y="active_users",
    by="plan",
    highlight="Pro",
    title="Pro is pulling ahead",
)
ax.figure.savefig(IMAGES / "line_emphasis.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "line_emphasis.png")
