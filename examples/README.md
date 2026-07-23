# vizlib examples

Runnable scripts that demonstrate the features implemented so far (M1: the theming
engine and `viz.bar`). Each script builds a chart from a small pandas DataFrame and
saves a PNG into [`images/`](./images).

## Setup

From the repository root, install the library (editable) into your environment:

```bash
pip install -e .
```

This pulls in the runtime dependencies (matplotlib, pandas) and puts `vizlib` on
your import path.

## Running the examples

Run any script from the **repository root**:

```bash
python examples/basic_bar.py
python examples/grouped_and_stacked.py
python examples/emphasis.py
python examples/horizontal_and_counts.py
python examples/theming.py
```

Or run them all at once:

```bash
for f in examples/*.py; do python "$f"; done
```

Each script prints the path of the image it writes. The scripts save PNGs rather
than opening a window, so they work in a headless environment; to view a chart
interactively instead, replace the `savefig(...)` call with `plt.show()`.

## What each script shows

| Script | Feature |
|---|---|
| [`basic_bar.py`](./basic_bar.py) | A single series, sorted, with the top bar auto-labeled |
| [`grouped_and_stacked.py`](./grouped_and_stacked.py) | Multi-series bars via `by=` — grouped and stacked |
| [`emphasis.py`](./emphasis.py) | `highlight=` — accent the one bar that matters, gray the rest |
| [`horizontal_and_counts.py`](./horizontal_and_counts.py) | `horizontal=True`, and row counts when `y` is omitted |
| [`theming.py`](./theming.py) | The dark theme, the `theme()` context manager, and a custom `Theme` |

## Gallery

### `basic_bar.py`
A single series in the slot-1 accent, sorted descending, with only the extreme bar
labeled — the axis carries the rest.

![basic bar](./images/basic_bar.png)

### `grouped_and_stacked.py`
Two series (`Web`, `Store`) in fixed categorical hues, with a frameless legend.
Grouped (left) and stacked (right); stacked segments are separated by a 2px surface
gap.

![grouped bar](./images/grouped_bar.png)
![stacked bar](./images/stacked_bar.png)

### `emphasis.py`
`highlight="East"` colors East in the accent hue, pushes every other bar to a muted
gray, drops the legend, and labels the highlighted bar.

![emphasis](./images/emphasis.png)

### `horizontal_and_counts.py`
Horizontal bars for longer category names (left), and a frequency chart built by
omitting `y` so rows are counted per category (right).

![horizontal bar](./images/horizontal_bar.png)
![counts](./images/counts.png)

### `theming.py`
The built-in dark theme (its own validated steps, not an inversion) and a custom
`Theme` with a warm emphasis accent.

![dark theme](./images/theme_dark.png)
![custom theme](./images/theme_custom.png)
