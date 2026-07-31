# Changelog

All notable changes to `chartcn` are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-31

Initial release.

### Added

- **Core-4 charts** on a shared contract: `bar` (grouped / stacked / horizontal,
  `sort=`, row counts when `y` is omitted), `line`, `scatter` (`size=`), and `hist`
  (`bins="auto"`). Every function takes a pandas DataFrame plus column names and
  returns the underlying matplotlib `Axes`.
- **Shared keyword vocabulary** across all charts — `x`, `y`, `by`, `highlight`,
  `sort`, `label`, `texture`, `title`, `subtitle`, `caption`, `xlabel`, `ylabel`,
  `theme`, `palette`, `ax`.
- **Emphasis** (`highlight=`) on all four charts: accents the selected series/group
  and grays the rest, dropping the legend. Selective direct labels (`label="auto"`)
  on bar and line.
- **Theming engine** — an immutable `Theme` dataclass with chrome/shape knobs
  (`axis_lines`, `bar_radius`, `value_axis`), plus `set_theme`, `get_theme`, and the
  `theme()` context manager. Built-in themes: `light` / `dark` (the default shadcn
  look) and `classic` / `classic-dark` (the original look).
- **Default look is shadcn** — rounded bar ends, no axis spines, a faint horizontal
  grid, card surfaces, and an Arial-metric sans, over a validated colorblind-safe
  8-hue categorical palette (fixed order; a 9th series folds into "Other"). Both axes
  are labeled by default.
- **Opt-in texture channel** (`texture=True`) — hatches (bar/hist), dash patterns
  (line), and marker shapes (scatter) for black-and-white / colorblind legibility.
- Ships `py.typed`; runtime dependencies are `matplotlib` and `pandas`.

[0.1.0]: https://github.com/HershR/viz-lib/releases/tag/v0.1.0
