# vizlib — MVP

> **Working name:** `vizlib` (placeholder — rename before publishing).
> A thin, opinionated wrapper around **matplotlib** that turns a **pandas
> DataFrame** into a publication-ready chart in one call.

---

## 1. Overview & problem statement

matplotlib can draw almost anything, but its **defaults look bad**: loud saturated
colors cycled in an unsafe order, heavy gridlines, boxed-in axes, tick labels that
collide, and no dark mode. Most people either fight the styling by hand every time
or reach for another library. Existing wrappers (seaborn, pandas `.plot`) improve
ergonomics but still don't make a chart that is *clear* and *looks good* by default.

**Value proposition:** `vizlib` does not add new plot types or a new rendering
engine. It applies **good defaults automatically** on top of matplotlib —
colorblind-safe palettes, recessive chrome, selective labels, an emphasis-first
mindset, and a real dark mode — so the *first* chart you draw is already good.

**Hard constraint:** this is a **wrapper, never a from-scratch renderer.** Every
chart is produced by calling matplotlib; `vizlib` only chooses inputs and
post-styles the result. Every function returns the underlying matplotlib object so
users can always drop down to raw matplotlib.

**One-line pitch:** _`vizlib.bar(df, x="region", y="sales")` → a chart you'd put in
a report, with zero styling arguments._

---

## 2. Design principles

These are the opinions the library encodes as defaults. They are non-negotiable in
v1 — they are the product.

1. **Form before color.** The data's job (magnitude / trend / identity / polarity /
   one headline) picks the chart type. Color is assigned last, by the job it does.
2. **Sequential is the safe default; emphasis is the honest one.** When the story is
   "this one series is the point," `vizlib` highlights it and grays the rest
   (`highlight=`) instead of handing every series a loud color.
3. **Colorblind-safe categorical palette, fixed order, never cycled.** Eight hues in
   a validated order (§5). A 9th series is folded into "Other" — the library will
   not generate a 9th hue.
4. **One axis, ever.** No dual-axis (two y-scales) charts — they invent correlations.
   Two measures of different scale → two charts or index to a common base.
5. **Recessive chrome.** Hairline gridlines one shade off the surface, no top/right
   spines, solid (never dashed) axis rules, generous padding.
6. **Thin marks with breathing room.** A 2px gap between adjacent/stacked fills;
   markers ≥ 8px; saturated fills only for small marks and accents, never big blocks.
7. **Label selectively; legend for ≥ 2 series.** Never a number on every point — the
   endpoint / extreme / highlighted series gets a direct label, the axis and (later)
   tooltip carry the rest. A single series needs no legend (the title names it).
8. **Dark mode is selected, not flipped.** The dark theme is its own set of steps
   validated against the dark surface — not an automatic inversion.

---

## 3. Scope

| In scope (v1) | Out of scope (v1) |
|---|---|
| **Core 4 charts:** bar (incl. grouped & stacked), line, scatter, histogram | Interactivity / tooltips / hover (matplotlib static output only) |
| **Emphasis / highlight** across bar & line | Dashboards, multi-chart layout managers |
| Light + dark **theming** with validated palettes | Geospatial / choropleth, 3D, animation |
| **pandas DataFrame** input, tidy (long) or wide | Non-pandas inputs (raw lists, numpy-only, polars) |
| Selective **direct labels** + legends | Statistical modeling (regression fits, KDE, CIs) |
| **PNG / SVG export** helper | Box/violin, area, heatmap, dumbbell, KPI tiles → **roadmap** |
| Returns raw matplotlib `Axes`/`Figure` for further tweaking | New rendering / any from-scratch drawing |

**Roadmap (post-MVP):** `.viz` DataFrame accessor; box/violin, area, heatmap,
dumbbell; KPI / stat tiles & hero numbers; diverging bar; small-multiples/faceting;
a colorblind-safety validator baked into `set_theme`.

---

## 4. Public API

### 4.1 Shape

Each chart type is a **top-level function** taking a DataFrame plus column names,
returning the matplotlib `Axes` it drew on:

```python
import vizlib as viz

ax = viz.bar(df, x="region", y="sales")
ax = viz.line(df, x="month", y="revenue", by="product")
```

Because the return value is a real `Axes`, raw matplotlib always remains available:

```python
ax = viz.bar(df, x="region", y="sales", title="Q3 sales")
ax.axhline(100_000, color="0.6", lw=1)      # drop down to matplotlib anytime
ax.figure.savefig("q3.png", dpi=200)
```

### 4.2 Shared keyword vocabulary

Every chart function speaks the same keywords, so learning one teaches the rest.

| Keyword | Meaning |
|---|---|
| `df` | pandas DataFrame (first positional arg) |
| `x`, `y` | column name(s) for the axes |
| `by` | column to split into series (categorical color / grouping) |
| `highlight` | value(s) of `by` to emphasize; everything else is grayed |
| `sort` | `None` / `"asc"` / `"desc"` — order categories by value (bar) |
| `label` | `"auto"` (default, selective) / `True` / `False` — direct value labels |
| `title`, `xlabel`, `ylabel` | text overrides (sensible defaults from column names) |
| `theme` | theme name or `Theme` object; falls back to the global theme |
| `palette` | override the categorical/sequential palette for this chart |
| `ax` | draw into an existing `Axes` (compose into a figure you control) |
| `**kwargs` | forwarded to the underlying matplotlib call (escape hatch) |

### 4.3 Chart functions (v1)

```python
viz.bar(df, x, y=None, by=None, *, stacked=False, horizontal=False,
        sort=None, highlight=None, label="auto", theme=None, palette=None,
        title=None, xlabel=None, ylabel=None, ax=None, **kwargs) -> Axes

viz.line(df, x, y=None, by=None, *, highlight=None, label="auto",
         theme=None, palette=None, title=None, xlabel=None, ylabel=None,
         ax=None, **kwargs) -> Axes

viz.scatter(df, x, y, by=None, *, size=None, highlight=None, theme=None,
            palette=None, title=None, xlabel=None, ylabel=None, ax=None,
            **kwargs) -> Axes

viz.hist(df, x, by=None, *, bins="auto", highlight=None, theme=None,
         palette=None, title=None, xlabel=None, ylabel=None, ax=None,
         **kwargs) -> Axes
```

Notes:
- `bar` with `by` set → **grouped**; add `stacked=True` → **stacked**. Long-named or
  many categories → `horizontal=True`.
- `y=None` on `bar`/`line` means "count rows per `x`" (a frequency chart).
- `highlight="Acme"` colors the Acme series in slot-1 accent and grays the others —
  the emphasis form (works on `bar` and `line`).

### 4.4 Usage snippets

```python
import matplotlib.pyplot as plt
import vizlib as viz

# Magnitude, sorted, top category labeled automatically
viz.bar(sales, x="region", y="revenue", sort="desc")

# Trend with one series as the point, the rest as context
viz.line(usage, x="month", y="active_users", by="plan", highlight="Pro")

# Distinct series, grouped
viz.bar(survey, x="quarter", y="responses", by="channel")

# Distribution, dark theme, into a specific subplot
fig, ax = plt.subplots()
viz.hist(latency, x="ms", bins=40, theme="dark", ax=ax, title="Request latency")
```

### 4.5 Fast-follow: `.viz` accessor (not MVP-blocking)

A thin pandas extension that delegates to the same functions, for a native feel:

```python
df.viz.bar(x="region", y="sales")     # == viz.bar(df, x="region", y="sales")
```

Documented here so the v1 API is designed to support it; implementation is deferred.

---

## 5. Theming system

### 5.1 Interface

```python
viz.set_theme("light")            # global default (also "dark")
viz.set_theme(Theme(...))         # custom theme object
with viz.theme("dark"):           # scoped override
    viz.bar(df, x="region", y="sales")
```

A `Theme` is a small dataclass bundling palettes + chrome + typography. Applying a
theme sets matplotlib `rcParams` and is what each chart function reads before
drawing. Two themes ship in v1: **light** and **dark**.

### 5.2 Palettes (validated default)

The categorical palette is eight hues in a **fixed, colorblind-safe order** — the
order is the safety mechanism and is never re-cycled or re-ranked. Values below are
the validated reference palette; the dark column is the same hues re-stepped for the
dark surface, not a different palette.

| Slot | Hue | Light | Dark |
|---|---|---|---|
| 1 | blue | `#2a78d6` | `#3987e5` |
| 2 | orange | `#eb6834` | `#d95926` |
| 3 | aqua | `#1baf7a` | `#199e70` |
| 4 | yellow | `#eda100` | `#c98500` |
| 5 | magenta | `#e87ba4` | `#d55181` |
| 6 | green | `#008300` | `#008300` |
| 7 | violet | `#4a3aa7` | `#9085e9` |
| 8 | red | `#e34948` | `#e66767` |

- **Sequential** (magnitude / histograms of a value): single hue **blue**,
  light→dark (`#cde2fb` → `#0d366b`).
- **Diverging** (above/below a baseline — roadmap charts): **blue ↔ red** poles with
  a neutral gray midpoint (`#f0efec` light / `#383835` dark).
- **Emphasis:** highlighted series → slot-1 accent; de-emphasized series → muted gray
  (`#898781`).

> The default palette is chosen to pass colorblind-safety checks (adjacent-pair
> separation under simulated protanopia/deuteranopia). A validator that enforces this
> on custom palettes is a roadmap item; until then, custom palettes are the user's
> responsibility.

### 5.3 Chrome & ink tokens

| Role | Light | Dark |
|---|---|---|
| Figure / axes surface | `#fcfcfb` | `#1a1a19` |
| Primary ink (title) | `#0b0b0b` | `#ffffff` |
| Secondary ink (labels) | `#52514e` | `#c3c2b7` |
| Muted (ticks/axis labels) | `#898781` | `#898781` |
| Gridline (hairline) | `#e1e0d9` | `#2c2c2a` |
| Baseline / axis | `#c3c2b7` | `#383835` |

### 5.4 Typography & chrome rules

- One sans typeface throughout (matplotlib default sans; configurable on the theme).
- Top & right spines removed; left/bottom spines are hairlines in the baseline token.
- Gridlines: solid horizontal hairlines only (y-grid for bar/line), never dashed.
- Padding generous; tick density capped to avoid label collisions.

---

## 6. Architecture

Small, flat package — each piece does one thing.

```
vizlib/
  __init__.py      # re-exports bar, line, scatter, hist, set_theme, theme, Theme
  core.py          # apply_theme(), _resolve_theme(), _despine(), _direct_labels(),
                   # _finalize(ax, ...)  — shared post-styling helpers
  palettes.py      # PALETTES dict, categorical/sequential/diverging accessors
  themes.py        # Theme dataclass, LIGHT, DARK, set_theme(), theme() ctx manager
  charts/
    bar.py         # viz.bar
    line.py        # viz.line
    scatter.py     # viz.scatter
    hist.py        # viz.hist
  accessor.py      # (fast-follow) registers the .viz DataFrame accessor
```

**The contract every chart function follows:**

1. **Validate input** — columns exist in `df`, dtypes make sense, resolve
   tidy-vs-wide, apply `sort`.
2. **Resolve theme** — `theme` arg → global → default; pull palette + chrome.
3. **Call matplotlib** — the actual `ax.bar` / `ax.plot` / `ax.scatter` / `ax.hist`
   with palette colors and thin-mark params. (This is the only drawing step; nothing
   is drawn by hand.)
4. **Post-style** — `core._finalize`: despine, hairline grid, apply ink tokens,
   selective direct labels, legend for ≥ 2 series, emphasis graying if `highlight`.
5. **Return** the `Axes`.

Creating vs. reusing axes: if `ax=None`, make a themed `Figure`/`Axes`; otherwise
draw into the caller's `ax` and leave figure-level styling to them.

---

## 7. Dependencies & packaging

- **Runtime:** `matplotlib`, `pandas`, `numpy` (transitively via both).
- **Python:** 3.10+.
- **Build:** `pyproject.toml` (PEP 621), setuptools or hatchling backend.
- **Dev:** `pytest` + `pytest-mpl` (image-comparison tests), `ruff`, `black`.
- **Install:** `pip install vizlib` (name is a placeholder).

```toml
# pyproject.toml (sketch)
[project]
name = "vizlib"
requires-python = ">=3.10"
dependencies = ["matplotlib>=3.7", "pandas>=2.0"]
```

---

## 8. Milestones / build order

| # | Milestone | Done when |
|---|---|---|
| **M1** | Theming engine + `bar` | `set_theme`, `Theme`, light/dark palettes exist; `viz.bar` draws a themed grouped/stacked/horizontal bar and returns an `Axes`. |
| **M2** | Remaining Core 4 | `line`, `scatter`, `hist` implemented on the shared contract; all four honor the shared keyword vocabulary. |
| **M3** | Shared emphasis | `highlight=` accents the selected series/group and grays the rest (dropping the legend) on **all four** charts via a shared path; `label="auto"` selective labels on bar & line. Direct labels stay bar/line-only (a value per point/bin is the anti-pattern). |
| **M4** | Polish, docs, gallery | README, an examples gallery (side-by-side "matplotlib default vs vizlib"), image-comparison tests, `pyproject.toml` packaged & pip-installable. |

---

## 9. Success criteria

- A DataFrame → a **publication-ready chart in one call, zero styling arguments.**
- The default palette **passes colorblind-safety checks** (adjacent-pair separation
  under simulated protanopia/deuteranopia).
- **Every chart is one function call** from a DataFrame using the shared vocabulary.
- Output **composes with raw matplotlib** — any chart accepts `ax=` and returns the
  `Axes`, so it drops into an existing figure.
- **Dark mode** produces a chart that looks designed for a dark surface, not inverted.
- The examples gallery makes the "before vs after" improvement obvious at a glance.

---

## 10. Non-goals & anti-patterns the library refuses to make easy

`vizlib` will **not** provide a comfortable path to these known-bad outputs:

- **Dual-axis charts** (two y-scales) — no API for a secondary y-axis.
- **Rainbow / multi-hue sequential** ramps for magnitude — sequential is one hue.
- **Recolor-on-filter** — color follows the entity, not its current rank, so
  dropping a series never repaints the survivors.
- **A number on every data point** — `label="auto"` is selective by design.
- **Thick saturated blocks + heavy/dashed gridlines** — the defaults are thin marks
  and recessive hairline chrome.
- **Generating a 9th categorical hue** — beyond 8 series, fold the tail into "Other."
