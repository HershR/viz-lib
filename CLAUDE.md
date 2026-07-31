# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`chartcn` is a **shadcn-inspired chart library** — an opinionated wrapper around
matplotlib that renders **pandas DataFrames**. It draws nothing from scratch; every
chart is a matplotlib call, and the value is the *good defaults* on top. The
**default look is shadcn** (`light`/`dark`): rounded bar ends, no axis spines, a
faint horizontal grid, card surfaces, an Arial-metric sans, both axes labeled
— over a colorblind-safe palette. The original look is preserved as
`classic`/`classic-dark`. Read `legacy/shadcnStyle.md` for the style breakdown, `legacy/mvp.md` for
the design spec/roadmap, and `README.md` for the user-facing pitch.

## Commands

The package uses a `src/` layout, so install it editable before running anything:

```bash
pip install -e .                 # runtime deps: matplotlib, pandas
pip install -e ".[dev]"          # + pytest, pytest-mpl, ruff, black
```

```bash
pytest                           # full suite (config in pyproject.toml -> tests/)
pytest tests/test_bar.py         # one file
pytest tests/test_bar.py::test_highlight_emphasis_colors   # one test
pytest -k emphasis               # by keyword

ruff check src tests             # lint
black src tests                  # format

python -m build                  # build sdist + wheel into dist/ (ships py.typed)
```

`tests/test_render_matrix.py` is a portable render-matrix suite (every chart ×
option combo × theme, asserting artists render) — used instead of pixel baselines,
which break across matplotlib/font versions.

Tests force the headless `Agg` backend via `tests/conftest.py` (imported before
pyplot). Any script or test that renders must not require a display; save with
`savefig` rather than `show`.

## Architecture

### The chart contract

Every chart function (`charts/bar.py`, `line.py`, `scatter.py`, `hist.py`) follows
the same five-step pipeline, and new chart types must too:

1. **Validate** input — df is a DataFrame, columns exist, args in range.
2. **Resolve theme** — `themes.resolve_theme(theme)` turns the `theme=` arg
   (`None` → active global, name → built-in, or a `Theme`) into a concrete `Theme`.
3. **Call matplotlib** — the actual `ax.bar`/`ax.plot`/… . This is the *only*
   drawing step. `core.new_axes(theme, ax)` returns the caller's `ax` or a fresh
   themed one.
4. **Post-style** via `core` helpers — `style_axes` (despine, hairline grid, muted
   ticks), `finalize` (upper-left title + optional `subtitle`/`caption` + axis
   labels, all sized by the theme's `type_scale`), `add_legend`, `format_value`.
5. **Return the `Axes`.** Never return `None` — callers drop down to raw matplotlib
   from the returned object.

### Module roles

- `palettes.py` — pure color data (no logic), keyed by mode `"light"`/`"dark"`:
  the 8-hue categorical order, sequential/diverging ramps, and chrome/ink tokens.
- `themes.py` — the immutable `Theme` dataclass assembled from `palettes`. The
  default `LIGHT`/`DARK` wear the **shadcn** chrome (knobs `axis_lines=False`,
  `bar_radius=0.10`; `value_axis=True` so both axes stay labeled; zinc/card neutrals,
  Liberation Sans) over
  the validated CVD palette, built via `dataclasses.replace(from_mode(...), ...)`.
  `CLASSIC`/`CLASSIC_DARK` are the original look (classic-chrome defaults).
  Also: global theme state
  (`set_theme`/`get_theme`/`theme`) and `apply_theme` (rcParams). `Theme` carries
  chrome/shape knobs — `axis_lines` (spines), `bar_radius` (rounded bar ends),
  `value_axis` (value-axis ticks) — that `core.style_axes`/`core.round_bars` honor.
- `core.py` — theme-agnostic post-styling helpers shared by all charts.
- `charts/_common.py` — data-shaping and color logic shared across charts:
  `aggregate_matrix`/`fold_matrix` (bar, line), `split_groups`/`fold_groups`
  (scatter, hist), `resolve_colors`, `with_palette`, `as_set`. New charts reuse
  these rather than reimplementing the fixed-palette/fold-past-8 rules.
- `charts/` — one module per chart type, re-exported from `charts/__init__.py`,
  then from the top-level `__init__.py`.

Theming is applied **twice on purpose**: `apply_theme` sets global `rcParams` (what
new figures inherit), and `core.style_axes` restyles the specific `Axes` so a
caller-supplied `ax=` is themed regardless of global state.

### Design non-negotiables (these are the product — do not "simplify" them away)

These come from `legacy/mvp.md` §2/§10 and are encoded as defaults:

- **Categorical palette is a fixed 8-hue order, never cycled.** The order *is* the
  colorblind-safety mechanism. A 9th series must fold into "Other" (see
  `_fold_series` in `bar.py`) — never generate or cycle a new hue.
- **Emphasis over rainbow.** `highlight=` colors the selected mark(s) in the accent
  hue and grays the rest (and suppresses the legend); this is the intended answer to
  "make it clearer," not more colors.
- **Recessive chrome:** no top/right spines, solid hairline gridlines, muted ticks.
- **Selective labels:** `label="auto"` labels only the extreme/highlighted mark —
  never a value on every mark. A small multi-series line (≤ 4) is labeled directly
  at each line's end (series name, in the line color) and drops the legend; larger
  sets keep the legend.
- **One axis.** Do not add a dual-axis / secondary-y API.
- **Dark mode is a distinct validated theme**, not an auto-inversion of the light one.
- **Texture is opt-in, never default.** `texture=True` adds a secondary-encoding
  channel for black-and-white / colorblind legibility — hatches (bar/hist), dash
  patterns (line), marker shapes (scatter), from fixed ordered sets in
  `charts/_common.py`. Applied only to multi-series, non-emphasis charts; emphasis
  is already lightness-distinct so it stays untextured.

## Branches & roadmap

Milestones are defined in `legacy/mvp.md` §8. `implement-core-charts` holds M1 (theming +
`viz.bar`), M2 (`line`/`scatter`/`hist` on the same contract), and M3 (shared
emphasis): all four charts now take `highlight=` (accent the selected series/group,
gray the rest, drop the legend) via the shared `resolve_colors` path. Direct value
labels (`label=`) stay bar/line-only by design — a value on every point/bin is the
anti-pattern. An `examples/` showcase (scripts + rendered gallery) lives on the
separate `examples` branch, based on `implement-core-charts`.
