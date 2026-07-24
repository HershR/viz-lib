"""``viz.scatter`` — relationships between two numeric columns.

Optional categorical color groups via ``by=`` and a third dimension via ``size=``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from .. import core
from ..themes import resolve_theme
from ._common import as_set, fold_groups, resolve_colors, split_groups, with_palette

# Marker area range (points^2). The floor keeps markers comfortably clickable/visible.
_SIZE_MIN, _SIZE_MAX = 30.0, 300.0
_SIZE_DEFAULT = 40.0


def scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    by: str | None = None,
    *,
    size: str | None = None,
    highlight=None,
    theme=None,
    palette=None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> Axes:
    """Draw a themed scatter plot from ``df`` and return the matplotlib ``Axes``.

    ``x`` and ``y`` are required numeric columns. ``by`` colors points by category
    (fixed palette, folded past 8). ``size`` maps a numeric column to marker area.
    ``highlight`` (matched against ``by`` groups) accents the selected group(s) in
    the theme accent and fades the rest to gray, dropping the legend.
    """
    # 1. Validate.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    for name, col in (("x", x), ("y", y), ("by", by), ("size", size)):
        if col is not None and col not in df.columns:
            raise KeyError(f"{name}={col!r} is not a column in df")

    # 2. Resolve theme (+ optional palette override).
    th = with_palette(resolve_theme(theme), palette)

    # 3. Groups (raw rows, not aggregated) and colors.
    groups = fold_groups(split_groups(df, by))
    names = [name for name, _ in groups]
    highlight_set = as_set(highlight)
    if by is None:
        colors, emphasis_mode = [th.categorical[0]], False
    else:
        colors, emphasis_mode = resolve_colors(names, th, highlight_set)

    # Shared size scaling across the whole column so groups are comparable.
    size_scale = _size_scaler(df[size]) if size is not None else None

    # 4. Draw.
    ax = core.new_axes(th, ax)
    for (name, sub), color in zip(groups, colors):
        s = size_scale(sub[size]) if size_scale is not None else _SIZE_DEFAULT
        if emphasis_mode:
            alpha = 0.9 if name in highlight_set else 0.45
        else:
            alpha = 0.9
        ax.scatter(
            sub[x],
            sub[y],
            s=s,
            color=color,
            edgecolor=th.surface,
            linewidth=0.6,
            alpha=alpha,
            label=(str(name) if name is not None else None),
            **kwargs,
        )

    # 5. Post-style.
    core.style_axes(ax, th, grid_axis="both")
    if by is not None and len(groups) > 1 and not emphasis_mode:
        core.add_legend(ax, th)
    core.finalize(
        ax,
        th,
        title=title,
        xlabel=xlabel if xlabel is not None else x,
        ylabel=ylabel if ylabel is not None else y,
    )
    return ax


def _size_scaler(column: pd.Series):
    """Return a function mapping raw size values to marker areas in [MIN, MAX]."""
    values = column.to_numpy(dtype=float)
    lo, hi = np.nanmin(values), np.nanmax(values)
    span = hi - lo

    def scale(sub_values):
        arr = np.asarray(sub_values, dtype=float)
        if span == 0:
            return np.full(arr.shape, (_SIZE_MIN + _SIZE_MAX) / 2)
        frac = (arr - lo) / span
        return _SIZE_MIN + frac * (_SIZE_MAX - _SIZE_MIN)

    return scale
