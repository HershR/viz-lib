"""``viz.line`` — trends over time (or any ordered x).

Single series or multiple series via ``by=``, with emphasis (``highlight=``) and
selective endpoint labels.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from .. import core
from ..themes import resolve_theme
from ._common import (
    LINESTYLES,
    aggregate_matrix,
    as_set,
    channel,
    fold_matrix,
    resolve_colors,
    with_palette,
)

# At or below this many series, label lines directly at their ends (and drop the
# legend) rather than making the reader bounce to a legend box.
_DIRECT_LABEL_MAX = 4


def line(
    df: pd.DataFrame,
    x: str,
    y: str | None = None,
    by: str | None = None,
    *,
    highlight=None,
    label: str | bool = "auto",
    texture: bool = False,
    theme=None,
    palette=None,
    title: str | None = None,
    subtitle: str | None = None,
    caption: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> Axes:
    """Draw a themed line chart from ``df`` and return the matplotlib ``Axes``.

    Parameters mirror :func:`vizlib.bar`. ``y=None`` counts rows per ``x``; duplicate
    ``(x, series)`` values are averaged. ``highlight`` (matched against ``by`` series)
    accents the selected line(s) and grays the rest.

    ``label`` controls direct labels (never a value on every point):

    - ``"auto"`` (default): a single series is labeled with its endpoint value; a
      small multi-series set (<= 4) is labeled directly at each line's end with the
      **series name** in the line's color, and the legend is dropped; larger sets
      keep a legend. Emphasis labels the highlighted line(s).
    - ``True``: label every series' endpoint value. ``False``: no direct labels.

    ``texture=True`` gives each series a distinct dash pattern for black-and-white /
    colorblind legibility (multi-series, non-emphasis only).
    """
    # 1. Validate.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    for name, col in (("x", x), ("y", y), ("by", by)):
        if col is not None and col not in df.columns:
            raise KeyError(f"{name}={col!r} is not a column in df")

    # 2. Resolve theme (+ optional palette override).
    th = with_palette(resolve_theme(theme), palette)

    # 3. Shape the data (mean over duplicate x per series -> a trend).
    matrix = fold_matrix(aggregate_matrix(df, x, y, by, agg="mean"))
    x_is_ordinal = pd.api.types.is_numeric_dtype(
        df[x]
    ) or pd.api.types.is_datetime64_any_dtype(df[x])
    if x_is_ordinal:
        matrix = matrix.sort_index()

    columns = list(matrix.columns)
    multi = by is not None and len(columns) > 1

    highlight_set = as_set(highlight)
    series_colors, emphasis_mode = resolve_colors(columns, th, highlight_set)

    # 4. Draw. Opt-in secondary encoding gives each series a distinct dash pattern
    # so lines stay separable in grayscale (multi-series, non-emphasis only).
    textured = texture and multi and not emphasis_mode
    ax = core.new_axes(th, ax)
    positions = matrix.index.to_numpy() if x_is_ordinal else np.arange(len(matrix))

    drawn = []  # (line2d, values) for endpoint labeling
    for j, col in enumerate(columns):
        values = matrix[col].to_numpy(dtype=float)
        highlighted = str(col) in {str(h) for h in highlight_set}
        (ln,) = ax.plot(
            positions,
            values,
            color=series_colors[j],
            linewidth=2,
            linestyle=channel(LINESTYLES, j) if textured else "-",
            label=str(col),
            zorder=3 if highlighted else 2,
            **kwargs,
        )
        drawn.append((ln, values))

    # 5. Post-style.
    core.style_axes(ax, th, grid_axis="y", value_axis="y")
    if not x_is_ordinal:
        ax.set_xticks(positions, [str(c) for c in matrix.index])

    # Small multi-series: label each line at its end with the series name and skip
    # the legend; otherwise fall back to selective value labels.
    direct_named = (
        multi
        and not emphasis_mode
        and label == "auto"
        and len(columns) <= _DIRECT_LABEL_MAX
    )
    if direct_named:
        _label_series_names(ax, th, drawn, positions, columns, series_colors)
    else:
        _label_endpoints(
            ax, th, drawn, positions, label, emphasis_mode, columns, highlight_set
        )

    if multi and not emphasis_mode and not direct_named:
        core.add_legend(ax, th)

    final_ylabel = ylabel if ylabel is not None else (y if y is not None else "count")
    if not th.value_axis:
        final_ylabel = None  # hidden value axis -> no value label
    core.finalize(
        ax,
        th,
        title=title,
        subtitle=subtitle,
        caption=caption,
        xlabel=xlabel if xlabel is not None else x,
        ylabel=final_ylabel,
    )
    return ax


def _label_series_names(ax, theme, drawn, positions, columns, series_colors):
    """Label each line at its endpoint with the series name, in the line's color."""
    for (_ln, values), col, color in zip(drawn, columns, series_colors):
        idx = _last_valid(values)
        if idx is None:
            continue
        ax.annotate(
            str(col),
            xy=(positions[idx], values[idx]),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            color=color,
            fontsize=theme.type_scale["annotation"],
            fontweight="bold",
        )


def _label_endpoints(
    ax, theme, drawn, positions, label, emphasis_mode, columns, highlight_set
):
    """Label the last point of selected series (never every point)."""
    if label is False:
        return

    def annotate(line2d, values):
        idx = _last_valid(values)
        if idx is None:
            return
        ax.annotate(
            core.format_value(values[idx]),
            xy=(positions[idx], values[idx]),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            color=theme.secondary_ink,
            fontsize=theme.type_scale["annotation"],
        )

    if label is True:
        for line2d, values in drawn:
            annotate(line2d, values)
        return

    # label == "auto": selective.
    wanted = {str(h) for h in highlight_set}
    if emphasis_mode:
        for (line2d, values), col in zip(drawn, columns):
            if str(col) in wanted:
                annotate(line2d, values)
    elif len(drawn) == 1:
        annotate(*drawn[0])


def _last_valid(values) -> int | None:
    """Index of the last non-NaN value, or None if all NaN/empty."""
    valid = np.where(~np.isnan(values))[0]
    return int(valid[-1]) if len(valid) else None
