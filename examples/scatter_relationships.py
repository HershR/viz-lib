"""Scatter plots: colored by group, sized via `size=`, and emphasis via `highlight=`.

Run:  python examples/scatter_relationships.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

import vizlib as viz

IMAGES = Path(__file__).parent / "images"

rng = np.random.default_rng(7)
n = 90
countries = pd.DataFrame(
    {
        "income": rng.normal(40, 12, n).clip(5),
        "life_expectancy": rng.normal(72, 6, n).clip(50),
        "continent": rng.choice(["Africa", "Asia", "Europe"], n),
        "population": rng.integers(2, 200, n),
    }
)

# Colored by a categorical column (fixed palette, one hue per group).
ax = viz.scatter(
    countries,
    x="income",
    y="life_expectancy",
    by="continent",
    title="Life expectancy vs income",
)
ax.figure.savefig(IMAGES / "scatter_groups.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "scatter_groups.png")

# A third dimension via size= (mapped to marker area, with a visibility floor).
ax = viz.scatter(
    countries,
    x="income",
    y="life_expectancy",
    size="population",
    title="...sized by population",
)
ax.figure.savefig(IMAGES / "scatter_sized.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "scatter_sized.png")

# Emphasis: highlight one group; the rest fade to gray and the legend is dropped.
ax = viz.scatter(
    countries,
    x="income",
    y="life_expectancy",
    by="continent",
    highlight="Europe",
    title="Europe, in context",
)
ax.figure.savefig(IMAGES / "scatter_emphasis.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "scatter_emphasis.png")
