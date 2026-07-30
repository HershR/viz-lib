"""matplotlib default vs vizlib — the same data, the same one call.

Each row draws a chart with raw matplotlib defaults (left) and with vizlib (right)
so the difference in defaults is obvious at a glance. This is the whole pitch:
vizlib doesn't draw anything matplotlib can't — it just picks good defaults.

Run:  python examples/before_after.py
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

sales = pd.DataFrame(
    {
        "region": ["North", "South", "East", "West", "Central"],
        "revenue": [120, 90, 150, 60, 105],
    }
)
usage = pd.DataFrame(
    {
        "month": list(range(1, 9)) * 2,
        "plan": ["Pro"] * 8 + ["Free"] * 8,
        "users": [5, 9, 14, 21, 25, 30, 38, 46, 20, 24, 27, 30, 34, 36, 41, 44],
    }
)

# Start from matplotlib's true defaults so the left column is an honest "before"
# (importing vizlib themes the global rcParams; reset them here). vizlib styles its
# own axes explicitly, so the right column is unaffected by this reset.
mpl.rcParams.update(mpl.rcParamsDefault)

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# --- Row 1: bar ---------------------------------------------------------------
axes[0, 0].bar(sales["region"], sales["revenue"])
axes[0, 0].set_title("matplotlib · bar")
viz.bar(
    sales, x="region", y="revenue", sort="desc", ax=axes[0, 1], title="vizlib · bar"
)

# --- Row 2: multi-series line -------------------------------------------------
for plan, grp in usage.groupby("plan"):
    axes[1, 0].plot(grp["month"], grp["users"], label=plan)
axes[1, 0].legend()
axes[1, 0].set_title("matplotlib · line")
viz.line(usage, x="month", y="users", by="plan", ax=axes[1, 1], title="vizlib · line")

fig.suptitle("matplotlib default   vs   vizlib", fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(IMAGES / "before_after.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "before_after.png")
