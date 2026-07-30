# vizlib

> **Working name — subject to change.** A thin, opinionated wrapper around
> [matplotlib](https://matplotlib.org/) that turns a
> [pandas](https://pandas.pydata.org/) DataFrame into a publication-ready chart in
> one call.

matplotlib can draw almost anything, but its defaults look bad: loud saturated
colors in a colorblind-unsafe order, heavy gridlines, boxed-in axes, and no dark
mode. `vizlib` doesn't replace matplotlib or add new chart types — it applies
**good defaults automatically** so the *first* chart you draw is already clear and
good-looking.

Same data, the same one call — matplotlib's defaults (left) vs vizlib (right):

![matplotlib default vs vizlib](./examples/images/before_after.png)

> ✅ **Status: MVP core complete (M1–M4).** The theming engine (`set_theme`, `theme`,
> `Theme`; light, dark, and the custom `lime` / `lime-dark`), the **Core-4 charts**
> — `bar`, `line`, `scatter`, `hist` — shared **emphasis** (`highlight=`) across all
> four, a portable render-matrix test suite, and a buildable/typed package. See
> [`mvp.md`](./mvp.md) for the roadmap and what's next (the `.viz` accessor and more
> chart types).

---

## Why vizlib

- **Good defaults, zero config.** No theme setup, no color lists, no `despine()`
  boilerplate. One call from a DataFrame gives you a chart you'd put in a report.
- **Colorblind-safe by design.** An eight-hue categorical palette in a fixed,
  validated order (checked against simulated protanopia/deuteranopia) — never a
  random color cycle.
- **Clarity over decoration.** Recessive hairline chrome, thin marks, selective
  labels, and an *emphasis* mode that highlights the one series that matters and
  grays the rest.
- **Real dark mode.** A dark theme with its own validated steps — not an automatic
  color inversion.
- **Never a dead end.** Every function returns the underlying matplotlib `Axes`, so
  you can always drop down to raw matplotlib for anything vizlib doesn't cover.

---

## Installation

Not yet published to PyPI. Install from source:

```bash
git clone https://github.com/HershR/viz-lib.git
cd viz-lib
pip install -e .
```

Requires Python 3.10+, matplotlib, and pandas. The package uses a `src/` layout
(`src/vizlib/`).

---

## Quickstart

A complete, runnable example:

```python
import pandas as pd
import vizlib as viz

sales = pd.DataFrame(
    {"region": ["North", "South", "East", "West"], "revenue": [120, 90, 150, 60]}
)
ax = viz.bar(sales, x="region", y="revenue", sort="desc", title="Revenue by region")
ax.figure.savefig("revenue.png", dpi=150, bbox_inches="tight")
```

More patterns (assuming `sales`, `usage`, `survey`, `latency` DataFrames):

```python
import matplotlib.pyplot as plt
import vizlib as viz

# Magnitude — sorted bars, top category labeled automatically
viz.bar(sales, x="region", y="revenue", sort="desc")

# Trend — one series is the point, the rest are context
viz.line(usage, x="month", y="active_users", by="plan", highlight="Pro")

# Distinct series — grouped bars
viz.bar(survey, x="quarter", y="responses", by="channel")

# Distribution — dark theme, into a subplot you control
fig, ax = plt.subplots()
viz.hist(latency, x="ms", bins=40, theme="dark", ax=ax, title="Request latency")
```

Every chart returns a matplotlib `Axes`, so you keep full control:

```python
ax = viz.bar(sales, x="region", y="revenue", title="Q3 sales")
ax.axhline(100_000, color="0.6", lw=1)   # raw matplotlib, anytime
ax.figure.savefig("q3.png", dpi=200)
```

---

## Chart types (v1)

| Function | For | Notes |
|---|---|---|
| `viz.bar` | comparing magnitude | `by=` → grouped; `stacked=True`; `horizontal=True`; `sort=` |
| `viz.line` | trends over time | `by=` for multiple series; `highlight=` for emphasis |
| `viz.scatter` | relationships | `by=` for categories, `size=` for a third dimension, `highlight=` for emphasis |
| `viz.hist` | distributions | `bins="auto"` by default; `by=` for groups, `highlight=` for emphasis |

Every function shares the same keyword vocabulary — `x`, `y`, `by`, `highlight`,
`sort`, `label`, `texture`, `title`, `subtitle`, `caption`, `theme`, `palette`,
`ax` — so learning one teaches the rest. Titles sit upper-left with an optional
`subtitle` beneath and a muted `caption` (source line) at the bottom, sized by a
deliberate type scale. Small multi-series line charts are labeled directly at each
line's end instead of via a legend. `texture=True` is an opt-in secondary-encoding
channel (hatches on bars/histograms, dash patterns on lines, marker shapes on
scatter) so a chart stays legible in black-and-white and for colorblind readers.
See [`mvp.md`](./mvp.md#4-public-api) for full signatures.

---

## Theming

```python
viz.set_theme("light")      # or "dark" — the global default
with viz.theme("dark"):     # scoped override
    viz.bar(sales, x="region", y="revenue")
```

Six themes are built in — **light**, **dark** (vizlib's validated colorblind-safe
palette), the custom **lime** / **lime-dark**, and **shadcn** / **shadcn-dark** — each
with a categorical, sequential, and diverging palette plus recessive chrome tokens
and a deliberate type scale. See [`mvp.md`](./mvp.md#5-theming-system) for values.

The **shadcn** / **shadcn-dark** theme mimics the shadcn charts look — shadcn's own
chart palette (coral/teal/slate/… light, blue/green/… dark), **rounded bar ends, no
axis spines, and a hidden value axis** (a faint horizontal grid carries it), in an
Arial-metric sans. The **lime** / **lime-dark** theme puts a lime accent over light
and dark surfaces. (Both custom palettes are not colorblind-validated.)

```python
viz.bar(sales, x="region", y="revenue", theme="shadcn")        # rounded, borderless
with viz.theme("shadcn-dark"):
    viz.line(usage, x="month", y="users", by="plan")
```

A `Theme` also exposes three chrome/shape knobs — `axis_lines` (draw the left/bottom
spines), `bar_radius` (round bar ends), and `value_axis` (show the value-axis ticks)
— so you can build your own look with `dataclasses.replace(viz.LIGHT, ...)`, or pass
`palette=` to any chart.

---

## Examples

Runnable scripts covering every chart, emphasis, theming, and black-and-white
(texture) output live in [`examples/`](./examples), with a rendered gallery in
[`examples/README.md`](./examples/README.md):

```bash
python examples/before_after.py     # matplotlib default vs vizlib
python examples/black_and_white.py  # texture channel, in color and grayscale
```

---

## Roadmap

- `df.viz.bar(...)` — a native pandas `.viz` accessor
- More chart types: box/violin, area, heatmap, dumbbell, KPI/stat tiles
- Small-multiples / faceting
- A built-in colorblind-safety validator for custom palettes

Full scope, milestones, and design rationale live in [`mvp.md`](./mvp.md).

---

## Scope & non-goals

`vizlib` is a **wrapper, not a renderer** — it never draws anything from scratch.
Out of scope for v1: interactivity/tooltips (matplotlib static output only),
dashboards, geospatial/3D/animation, and non-pandas inputs. It also deliberately
avoids known-bad patterns — no dual-axis charts, no rainbow sequential ramps, no
recolor-on-filter, no a-number-on-every-point. See
[`mvp.md`](./mvp.md#10-non-goals--anti-patterns-the-library-refuses-to-make-easy).

---

## License

[MIT](./LICENSE).
