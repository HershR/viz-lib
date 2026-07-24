"""``viz.bar`` — the M1 chart.

Compares magnitude across categories. Supports a single series, grouped or stacked
multi-series (via ``by=``), horizontal orientation, sorting, emphasis
(``highlight=``), and selective direct labels.
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


def bar(
    df: pd.DataFrame,
    x: str,
    y: str | None = None,
    by: str | None = None,
    *,
    stacked: bool = False,
    horizontal: bool = False,
    sort: str | None = None,
    highlight=None,
    label: str | bool = "auto",
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
    """Draw a themed bar chart from ``df`` and return the matplotlib ``Axes``.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    x : str
        Column for the categorical axis.
    y : str, optional
        Column for the value axis. If omitted, rows are counted per ``x``.
    by : str, optional
        Column to split into series (grouped, or stacked with ``stacked=True``).
    stacked, horizontal : bool
        Bar layout options.
    sort : {None, "asc", "desc"}
        Order categories by value (by row total when ``by`` is set).
    highlight : value or list, optional
        Value(s) to emphasize. Matches ``by`` series when ``by`` is set, otherwise
        ``x`` categories. Emphasized marks take the accent hue; the rest go gray.
    label : {"auto", True, False}
        Direct value labels. "auto" labels the single largest bar of a one-series
        chart (or the highlighted marks); ``True`` labels every bar.
    theme : Theme or str, optional
        Per-call theme override; falls back to the global theme.
    palette : sequence of colors, optional
        Override the categorical colors for this chart.
    title, xlabel, ylabel : str, optional
        Text overrides. Axis labels default to the column names.
    ax : matplotlib.axes.Axes, optional
        Draw into an existing axes instead of creating one.
    **kwargs
        Forwarded to the underlying matplotlib ``bar``/``barh`` call.

    Returns
    -------
    matplotlib.axes.Axes
    """
    # 1. Validate input.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    for name, col in (("x", x), ("y", y), ("by", by)):
        if col is not None and col not in df.columns:
            raise KeyError(f"{name}={col!r} is not a column in df")
    if sort not in (None, "asc", "desc"):
        raise ValueError(f"sort must be None, 'asc', or 'desc'; got {sort!r}")

    # 2. Resolve theme (+ optional palette override).
    th = with_palette(resolve_theme(theme), palette)

    # 3. Shape the data.
    matrix = aggregate_matrix(df, x, y, by, agg="sum")
    matrix = fold_matrix(matrix)

    if sort is not None:
        totals = matrix.sum(axis=1)
        matrix = matrix.loc[totals.sort_values(ascending=(sort == "asc")).index]

    categories = [str(c) for c in matrix.index]
    columns = list(matrix.columns)
    multi = by is not None and len(columns) > 1

    # Highlight matches series (when by is set) or x categories otherwise.
    highlight_set = as_set(highlight)
    if highlight_set and by is None:
        colors = [
            th.emphasis if cat in {str(h) for h in highlight_set} else th.deemphasis
            for cat in matrix.index
        ]
        emphasis_mode = True
        series_colors = None
    else:
        series_colors, emphasis_mode = resolve_colors(columns, th, highlight_set)
        colors = None

    ax = core.new_axes(th, ax)
    n = len(categories)
    positions = np.arange(n)
    plot = ax.barh if horizontal else ax.bar
    span_kw = "height" if horizontal else "width"

    drawn = []  # (bar_container, value_array) for labeling

    if by is None:
        # Single series.
        values = matrix.iloc[:, 0].to_numpy(dtype=float)
        bar_colors = colors if colors is not None else series_colors[0]
        container = plot(
            positions, values, **{span_kw: 0.8}, color=bar_colors, **kwargs
        )
        drawn.append((container, values))
    elif stacked:
        offset = np.zeros(n)
        base_kw = "left" if horizontal else "bottom"
        for j, col in enumerate(columns):
            values = matrix[col].to_numpy(dtype=float)
            container = plot(
                positions,
                values,
                **{span_kw: 0.8, base_kw: offset},
                color=series_colors[j],
                label=str(col),
                edgecolor=th.surface,
                linewidth=1.5,
                **kwargs,
            )
            drawn.append((container, values))
            offset = offset + values
    else:
        # Grouped.
        group_span = 0.8
        bar_span = group_span / len(columns)
        for j, col in enumerate(columns):
            values = matrix[col].to_numpy(dtype=float)
            shift = (j - (len(columns) - 1) / 2) * bar_span
            container = plot(
                positions + shift,
                values,
                **{span_kw: bar_span},
                color=series_colors[j],
                label=str(col),
                **kwargs,
            )
            drawn.append((container, values))

    # 4. Post-style.
    grid_axis = "x" if horizontal else "y"
    core.style_axes(ax, th, grid_axis=grid_axis)
    if horizontal:
        ax.set_yticks(positions, categories)
        ax.invert_yaxis()  # first category at the top
    else:
        ax.set_xticks(positions, categories)

    _apply_labels(
        ax,
        th,
        drawn,
        label,
        horizontal,
        emphasis_mode,
        colors,
        highlight_set,
        matrix,
        by,
    )

    # Legend only for genuine multi-color multi-series (not the emphasis form).
    if multi and not emphasis_mode:
        core.add_legend(ax, th)

    default_cat_label = x
    default_val_label = y if y is not None else "count"
    if horizontal:
        xlabel = xlabel if xlabel is not None else default_val_label
        ylabel = ylabel if ylabel is not None else default_cat_label
    else:
        xlabel = xlabel if xlabel is not None else default_cat_label
        ylabel = ylabel if ylabel is not None else default_val_label
    core.finalize(
        ax,
        th,
        title=title,
        subtitle=subtitle,
        caption=caption,
        xlabel=xlabel,
        ylabel=ylabel,
    )

    return ax


def _apply_labels(
    ax,
    theme,
    drawn,
    label,
    horizontal,
    emphasis_mode,
    category_colors,
    highlight_set,
    matrix,
    by,
):
    """Place direct value labels according to the ``label`` setting."""
    if label is False:
        return

    def annotate(container, indices):
        for i in indices:
            rect = container.patches[i]
            value = rect.get_width() if horizontal else rect.get_height()
            if value == 0:
                continue
            if horizontal:
                xy = (rect.get_width(), rect.get_y() + rect.get_height() / 2)
                xytext, ha, va = (4, 0), "left", "center"
            else:
                xy = (rect.get_x() + rect.get_width() / 2, rect.get_height())
                xytext, ha, va = (0, 4), "center", "bottom"
            ax.annotate(
                core.format_value(value),
                xy=xy,
                xytext=xytext,
                textcoords="offset points",
                ha=ha,
                va=va,
                color=theme.secondary_ink,
                fontsize=theme.type_scale["annotation"],
            )

    if label is True:
        for container, values in drawn:
            annotate(container, range(len(values)))
        return

    # label == "auto": selective.
    if emphasis_mode and category_colors is not None:
        # Single-series emphasis: label the highlighted x categories.
        wanted = {str(h) for h in highlight_set}
        idx = [i for i, cat in enumerate(matrix.index) if str(cat) in wanted]
        annotate(drawn[0][0], idx)
    elif len(drawn) == 1:
        # Single series: label the extreme (largest) bar.
        values = drawn[0][1]
        if len(values):
            annotate(drawn[0][0], [int(np.argmax(values))])
    # Multi-series non-emphasis: legend + axis carry it; no direct labels.
