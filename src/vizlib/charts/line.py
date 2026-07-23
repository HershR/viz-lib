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
    aggregate_matrix,
    as_set,
    fold_matrix,
    resolve_colors,
    with_palette,
)


def line(
    df: pd.DataFrame,
    x: str,
    y: str | None = None,
    by: str | None = None,
    *,
    highlight=None,
    label: str | bool = "auto",
    theme=None,
    palette=None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> Axes:
    """Draw a themed line chart from ``df`` and return the matplotlib ``Axes``.

    Parameters mirror :func:`vizlib.bar`. ``y=None`` counts rows per ``x``; duplicate
    ``(x, series)`` values are averaged. ``highlight`` (matched against ``by`` series)
    accents the selected line(s) and grays the rest. ``label`` places an endpoint
    value: "auto" on a single/highlighted series, ``True`` on every series' endpoint,
    ``False`` none — never a value on every point.
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

    # 4. Draw.
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
            label=str(col),
            zorder=3 if highlighted else 2,
            **kwargs,
        )
        drawn.append((ln, values))

    # 5. Post-style.
    core.style_axes(ax, th, grid_axis="y")
    if not x_is_ordinal:
        ax.set_xticks(positions, [str(c) for c in matrix.index])

    _label_endpoints(
        ax, th, drawn, positions, label, emphasis_mode, columns, highlight_set
    )

    if multi and not emphasis_mode:
        core.add_legend(ax, th)

    core.finalize(
        ax,
        th,
        title=title,
        xlabel=xlabel if xlabel is not None else x,
        ylabel=ylabel if ylabel is not None else (y if y is not None else "count"),
    )
    return ax


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
            fontsize=9,
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
