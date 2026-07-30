"""Black-and-white legibility: the opt-in `texture=` secondary-encoding channel.

`texture=True` gives each series a non-color cue — hatches on bars, dash patterns on
lines, marker shapes on scatter — so a chart survives grayscale printing and reads
for colorblind viewers. This script renders a textured grouped bar and multi-line in
color, then desaturates them to grayscale to prove the series stay distinct with
color removed.

Run:  python examples/black_and_white.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

survey = pd.DataFrame(
    {
        "quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3", "Q4", "Q4"],
        "channel": ["Web", "Store"] * 4,
        "responses": [30, 18, 42, 25, 38, 30, 45, 33],
    }
)
usage = pd.DataFrame(
    {
        "month": list(range(1, 9)) * 3,
        "plan": ["Pro"] * 8 + ["Free"] * 8 + ["Team"] * 8,
        "users": [5, 9, 14, 21, 25, 30, 38, 46]
        + [20, 24, 27, 30, 34, 36, 41, 44]
        + [2, 5, 9, 15, 22, 31, 42, 55],
    }
)

fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
viz.bar(survey, x="quarter", y="responses", by="channel", texture=True,
        ax=axes[0], title="Responses by channel", subtitle="texture=True")
viz.line(usage, x="month", y="users", by="plan", texture=True,
         ax=axes[1], title="Users by plan", subtitle="texture=True")
fig.patch.set_facecolor("#fcfcfb")
fig.tight_layout(pad=2.5)
color = IMAGES / "black_and_white_color.png"
fig.savefig(color, dpi=120)
print("wrote", color)

# Desaturate to grayscale to prove the series remain distinguishable.
img = plt.imread(color)[..., :3]
luminance = img @ np.array([0.2126, 0.7152, 0.0722])
g, gax = plt.subplots(figsize=(14, 5.2))
gax.imshow(luminance, cmap="gray", vmin=0, vmax=1)
gax.axis("off")
gray = IMAGES / "black_and_white_gray.png"
g.savefig(gray, dpi=120, bbox_inches="tight", pad_inches=0)
print("wrote", gray)
