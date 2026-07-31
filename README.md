# chartcn

> A **shadcn-inspired** chart library: a thin, opinionated wrapper around
> [matplotlib](https://matplotlib.org/) that turns a
> [pandas](https://pandas.pydata.org/) DataFrame into a clean, shadcn-style chart in
> one call — in light **and** dark mode.

matplotlib can draw almost anything, but its defaults look dated: loud colors, heavy
gridlines, boxed-in axes, no dark mode. `chartcn` doesn't replace matplotlib or add
new chart types — it makes the **shadcn charts aesthetic the default**: rounded bar
ends, borderless axes, a whisper-faint horizontal grid, muted labels on both axes,
and light/dark card surfaces — all over a **colorblind-safe palette**.

Same data, the same one call — matplotlib's defaults (left) vs chartcn (right):

![matplotlib default vs chartcn](./examples/images/before_after.png)

> ✅ **Default look is shadcn, light + dark.** `viz.bar(df, x=…, y=…)` renders the
> shadcn style out of the box; `theme="dark"` gives the dark card. The four core
> charts (`bar`, `line`, `scatter`, `hist`) share emphasis (`highlight=`) and an
> opt-in texture channel. The original chartcn look is preserved as `classic` /
> `classic-dark`. See [`shadcnStyle.md`](./legacy/shadcnStyle.md) for the style breakdown
> and [`mvp.md`](./legacy/mvp.md) for the roadmap.

---

## Why chartcn

- **shadcn look, zero config.** No theme setup, no color lists, no `despine()`
  boilerplate — the first chart you draw already looks like a shadcn chart.
- **Light and dark, first-class.** `theme="dark"` (or `set_theme("dark")`) switches
  to the dark card; both are hand-tuned, not an auto-inversion.
- **Colorblind-safe palette.** Under the shadcn chrome sits an eight-hue categorical
  palette in a fixed, validated order (checked against simulated protanopia/
  deuteranopia) — never a random color cycle.
- **Clarity over decoration.** Recessive chrome, thin marks, selective labels, and an
  *emphasis* mode (`highlight=`) that spotlights the one series that matters.
- **Never a dead end.** Every function returns the underlying matplotlib `Axes`, so
  you can always drop down to raw matplotlib. Prefer the old look? `theme="classic"`.

---

## Installation

Not yet published to PyPI. Install from source:

```bash
git clone https://github.com/HershR/viz-lib.git
cd viz-lib
pip install -e .
```

Requires Python 3.10+, matplotlib, and pandas. The package uses a `src/` layout
(`src/chartcn/`).

---

## Quickstart

A complete, runnable example:

```python
import pandas as pd
import chartcn as viz

sales = pd.DataFrame(
    {"region": ["North", "South", "East", "West"], "revenue": [120, 90, 150, 60]}
)
ax = viz.bar(sales, x="region", y="revenue", sort="desc", title="Revenue by region")
ax.figure.savefig("revenue.png", dpi=150, bbox_inches="tight")
```

More patterns (assuming `sales`, `usage`, `survey`, `latency` DataFrames):

```python
import matplotlib.pyplot as plt
import chartcn as viz

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
See [`mvp.md`](./legacy/mvp.md#4-public-api) for full signatures.

---

## Theming

```python
# light is the default; switch to the dark card:
with viz.theme("dark"):
    viz.bar(sales, x="region", y="revenue")

viz.set_theme("dark")                                  # or set it globally
viz.bar(sales, x="region", y="revenue", theme="classic")  # or per-call override
```

Built-in themes:

| Theme | Look |
|---|---|
| **`light`** (default) / **`dark`** | The shadcn aesthetic — rounded bars, no spines, faint grid, card surfaces, both axes labeled — over the validated colorblind-safe palette. |
| **`classic`** / **`classic-dark`** | The original chartcn look: hairline spines, a visible value axis, square bars, the default sans. |
| **`lime`** / **`lime-dark`** | A custom lime-accent theme (palette not colorblind-validated). |

Each theme carries a categorical/sequential/diverging palette, chrome tokens, and a
type scale. A `Theme` also exposes chrome/shape knobs — `axis_lines` (draw the
left/bottom spines), `bar_radius` (round bar ends), and `value_axis` (show the
value-axis ticks) — so you can build your own look with
`dataclasses.replace(viz.LIGHT, ...)`, or pass `palette=` to any chart. See
[`shadcnStyle.md`](./legacy/shadcnStyle.md) for the shadcn style breakdown.

---

## Examples

Runnable scripts covering every chart, emphasis, theming, and black-and-white
(texture) output live in [`examples/`](./examples), with a rendered gallery in
[`examples/README.md`](./examples/README.md):

```bash
python examples/before_after.py     # matplotlib default vs chartcn
python examples/black_and_white.py  # texture channel, in color and grayscale
```

---

## Roadmap

- `df.viz.bar(...)` — a native pandas `.viz` accessor
- More chart types: box/violin, area, heatmap, dumbbell, KPI/stat tiles
- Small-multiples / faceting
- A built-in colorblind-safety validator for custom palettes

Full scope, milestones, and design rationale live in [`mvp.md`](./legacy/mvp.md).

---

## Scope & non-goals

`chartcn` is a **wrapper, not a renderer** — it never draws anything from scratch.
Out of scope for v1: interactivity/tooltips (matplotlib static output only),
dashboards, geospatial/3D/animation, and non-pandas inputs. It also deliberately
avoids known-bad patterns — no dual-axis charts, no rainbow sequential ramps, no
recolor-on-filter, no a-number-on-every-point. See
[`mvp.md`](./legacy/mvp.md#10-non-goals--anti-patterns-the-library-refuses-to-make-easy).

---

## License

[MIT](./LICENSE).
