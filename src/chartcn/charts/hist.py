"""``viz.hist`` — the distribution of one numeric column.

A single distribution (one hue) or several overlaid groups via ``by=``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from .. import core
from ..themes import resolve_theme
from ._common import (
    HATCHES,
    as_set,
    channel,
    darken,
    fold_groups,
    resolve_colors,
    split_groups,
    with_palette,
)


def hist(
    df: pd.DataFrame,
    x: str,
    by: str | None = None,
    *,
    bins="auto",
    highlight=None,
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
    """Draw a themed histogram from ``df`` and return the matplotlib ``Axes``.

    ``x`` is the numeric column to bin. ``by`` overlays one translucent distribution
    per category (fixed palette, folded past 8). ``bins`` forwards to numpy/matplotlib
    ("auto" or an int); a shared set of edges is computed so overlaid groups align.
    ``highlight`` (matched against ``by`` groups) accents the selected distribution(s)
    in the theme accent and fades the rest to gray, dropping the legend.
    ``texture=True`` gives each distribution a distinct hatch for black-and-white /
    colorblind legibility (multi-group, non-emphasis only).
    """
    # 1. Validate.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    for name, col in (("x", x), ("by", by)):
        if col is not None and col not in df.columns:
            raise KeyError(f"{name}={col!r} is not a column in df")

    # 2. Resolve theme (+ optional palette override).
    th = with_palette(resolve_theme(theme), palette)

    # 3. Groups + a shared bin edge set across the whole column.
    groups = fold_groups(split_groups(df, by))
    names = [name for name, _ in groups]
    highlight_set = as_set(highlight)
    if by is None:
        colors, emphasis_mode = [th.categorical[0]], False
    else:
        colors, emphasis_mode = resolve_colors(names, th, highlight_set)

    all_values = df[x].to_numpy(dtype=float)
    all_values = all_values[~np.isnan(all_values)]
    edges = np.histogram_bin_edges(all_values, bins=bins)

    # 4. Draw. Single group is opaque; overlaid groups are translucent. In emphasis
    #    mode the highlighted distribution stays bold and the rest fade back. Opt-in
    #    texture gives each group a distinct hatch for grayscale legibility.
    multi = by is not None and len(groups) > 1
    textured = texture and multi and not emphasis_mode
    ax = core.new_axes(th, ax)
    containers = []
    for i, ((name, sub), color) in enumerate(zip(groups, colors)):
        values = sub[x].to_numpy(dtype=float)
        values = values[~np.isnan(values)]
        if emphasis_mode:
            alpha = 0.85 if name in highlight_set else 0.3
        else:
            alpha = 0.6 if multi else 1.0
        _n, _bins, patches = ax.hist(
            values,
            bins=edges,
            color=color,
            alpha=alpha,
            edgecolor=darken(color) if textured else th.surface,
            linewidth=0.8,
            hatch=channel(HATCHES, i) if textured else None,
            label=(str(name) if name is not None else None),
            **kwargs,
        )
        containers.append(patches)

    # 5. Post-style.
    core.style_axes(ax, th, grid_axis="y", value_axis="y")
    if multi and not emphasis_mode:
        core.add_legend(ax, th)
    final_ylabel = ylabel if ylabel is not None else "count"
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

    # Rounded bar ends (shadcn-style themes).
    if th.bar_radius > 0:
        core.round_bars(ax, containers, th, horizontal=False)

    return ax
