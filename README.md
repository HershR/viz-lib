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

```python
import vizlib as viz

viz.bar(sales, x="region", y="revenue", sort="desc")
```

> ⚠️ **Status: early / MVP in progress.** The theming engine (`set_theme`, `theme`,
> `Theme`, light & dark) and the **Core-4 charts** — `bar`, `line`, `scatter`,
> `hist` (M1 + M2) — are implemented. Next up (M3) is shared emphasis/labeling
> across all chart types. See [`mvp.md`](./mvp.md) for the full plan.

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
`sort`, `label`, `title`, `theme`, `palette`, `ax` — so learning one teaches the
rest. See [`mvp.md`](./mvp.md#4-public-api) for full signatures.

---

## Theming

```python
viz.set_theme("light")      # or "dark" — the global default
with viz.theme("dark"):     # scoped override
    viz.bar(sales, x="region", y="revenue")
```

Two themes ship in v1 (**light** and **dark**), each with a validated categorical,
sequential, and diverging palette plus recessive chrome tokens. See
[`mvp.md`](./mvp.md#5-theming-system) for the palette values.

A custom **`lime`** / **`lime-dark`** theme ("Lime Green", ported from a shadcn
theme) is also built in — a lime primary/accent over light and dark surfaces:

```python
viz.bar(sales, x="region", y="revenue", theme="lime")        # by name
with viz.theme("lime-dark"):
    viz.line(usage, x="month", y="users", by="plan")
```

Build your own by constructing a `Theme` (see `viz.LIME`) or passing `palette=` to
any chart.

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
