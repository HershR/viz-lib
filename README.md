# chartcn

[![PyPI](https://img.shields.io/pypi/v/chartcn.svg)](https://pypi.org/project/chartcn/)
[![Python](https://img.shields.io/pypi/pyversions/chartcn.svg)](https://pypi.org/project/chartcn/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

A **shadcn-inspired** chart library — a thin wrapper around
[matplotlib](https://matplotlib.org/) that turns a
[pandas](https://pandas.pydata.org/) DataFrame into a clean chart in one call,
in light **and** dark mode.

It doesn't add chart types or draw anything itself — it makes the **shadcn charts
look the default**: rounded bar ends, borderless axes, a faint horizontal grid, and
light/dark card surfaces, over a **colorblind-safe palette**. Every function returns
the underlying matplotlib `Axes`, so you can always drop down to raw matplotlib.

Same data, one call — matplotlib's defaults (left) vs chartcn (right):

![matplotlib default vs chartcn](https://raw.githubusercontent.com/HershR/viz-lib/master/examples/images/before_after.png)

## Install

```bash
pip install chartcn
```

Requires Python 3.10+ (pulls in matplotlib and pandas).

## Quickstart

```python
import pandas as pd
import chartcn as viz

sales = pd.DataFrame(
    {"region": ["North", "South", "East", "West"], "revenue": [120, 90, 150, 60]}
)
ax = viz.bar(sales, x="region", y="revenue", sort="desc", title="Revenue by region")
ax.figure.savefig("revenue.png", dpi=150, bbox_inches="tight")
```

The return value is a real matplotlib `Axes`, so you keep full control — compose into
your own figure with `ax=`, or drop to raw matplotlib any time:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
viz.bar(sales, x="region", y="revenue", ax=ax, title="Q3 sales")
ax.axhline(100, color="0.6", lw=1)   # raw matplotlib
```

## Charts

| Function | For | Highlights |
|---|---|---|
| `viz.bar` | comparing magnitude | `by=` grouped · `stacked=True` · `horizontal=True` · `sort=` |
| `viz.line` | trends over time | `by=` for multiple series · `highlight=` |
| `viz.scatter` | relationships | `by=` for categories · `size=` for a third dimension |
| `viz.hist` | distributions | `bins="auto"` · `by=` for groups |

```python
# One series is the point, the rest are context
viz.line(usage, x="month", y="active_users", by="plan", highlight="Pro")

# Grouped bars
viz.bar(survey, x="quarter", y="responses", by="channel")

# A distribution in dark mode
viz.hist(latency, x="ms", bins=40, theme="dark", title="Request latency")
```

Every function shares the same keywords, so learning one teaches the rest:
`x`, `y`, `by`, `highlight`, `sort`, `label`, `texture`, `title`, `subtitle`,
`caption`, `xlabel`, `ylabel`, `theme`, `palette`, `ax`.

- **`highlight=`** accents one series/group and grays the rest (dropping the legend) —
  the honest alternative to giving every series a loud color.
- **`label="auto"`** labels only the extreme or highlighted mark, never every point.
- **`texture=True`** adds hatches (bar/hist), dash patterns (line), or marker shapes
  (scatter) so a chart stays legible in black-and-white and for colorblind readers.

## Theming

`light` is the default; switch per call, per block, or globally:

```python
viz.bar(sales, x="region", y="revenue", theme="dark")   # per call

with viz.theme("dark"):                                  # scoped
    viz.bar(sales, x="region", y="revenue")

viz.set_theme("dark")                                    # global
```

| Theme | Look |
|---|---|
| **`light`** (default) / **`dark`** | The shadcn look — rounded bars, no spines, faint grid, card surfaces — over the colorblind-safe palette. |
| **`classic`** / **`classic-dark`** | Hairline spines, square bars, the default sans. |
| **`lime`** / **`lime-dark`** | A lime-accent theme (palette not colorblind-validated). |

Build your own by passing `palette=` to any chart, or with
`dataclasses.replace(viz.LIGHT, ...)` to tweak chrome knobs (`axis_lines`,
`bar_radius`, `value_axis`).

## Examples

Runnable scripts for every chart, emphasis, theming, and grayscale/texture output
live in [`examples/`](./examples), with a rendered gallery in
[`examples/README.md`](./examples/README.md).

## License

[MIT](./LICENSE)
