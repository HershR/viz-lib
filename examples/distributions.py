"""Histograms: a single distribution, overlaid groups, and emphasis via `highlight=`.

Run:  python examples/distributions.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

import chartcn as viz

IMAGES = Path(__file__).parent / "images"

rng = np.random.default_rng(3)
requests = pd.DataFrame(
    {
        "latency_ms": np.concatenate(
            [rng.normal(120, 25, 500), rng.normal(210, 30, 400)]
        ),
        "region": ["us-east"] * 500 + ["eu-west"] * 400,
    }
)

# A single distribution in one hue.
ax = viz.hist(
    requests, x="latency_ms", bins=30, title="Request latency", xlabel="latency (ms)"
)
ax.figure.savefig(IMAGES / "hist_single.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "hist_single.png")

# Overlaid groups: translucent, one categorical hue each, aligned on shared bins.
ax = viz.hist(
    requests,
    x="latency_ms",
    by="region",
    bins=30,
    title="Latency by region",
    xlabel="latency (ms)",
)
ax.figure.savefig(IMAGES / "hist_overlaid.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "hist_overlaid.png")

# Emphasis: highlight one distribution; the rest fade back, legend dropped.
ax = viz.hist(
    requests,
    x="latency_ms",
    by="region",
    bins=30,
    highlight="eu-west",
    title="eu-west stands out",
    xlabel="latency (ms)",
)
ax.figure.savefig(IMAGES / "hist_emphasis.png", dpi=120, bbox_inches="tight")
print("wrote", IMAGES / "hist_emphasis.png")
