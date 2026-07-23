"""Shared post-styling helpers used by every chart function.

The contract each chart follows: validate input -> resolve theme -> call
matplotlib -> post-style here -> return the ``Axes``. These helpers own the
"post-style" step so styling stays consistent across chart types.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .themes import Theme


def new_axes(theme: Theme, ax: Axes | None) -> Axes:
    """Return the axes to draw on: the caller's, or a fresh themed one."""
    if ax is not None:
        return ax
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.set_facecolor(theme.surface)
    return ax


def style_axes(ax: Axes, theme: Theme, *, grid_axis: str | None = "y") -> None:
    """Apply recessive chrome to ``ax``: surface, spines, ticks, and hairline grid.

    ``grid_axis`` is "y" (default), "x", "both", or ``None`` for no grid. Gridlines
    are solid hairlines one shade off the surface; the top/right spines are removed
    and the remaining spines are hairlines in the baseline token.
    """
    ax.set_facecolor(theme.surface)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(theme.baseline)
        ax.spines[side].set_linewidth(1.0)

    ax.tick_params(colors=theme.muted, labelcolor=theme.secondary_ink, length=0)

    if grid_axis:
        ax.grid(
            visible=True,
            axis=grid_axis,
            color=theme.gridline,
            linewidth=0.8,
            linestyle="-",
        )
        # Grid sits behind the marks.
        ax.set_axisbelow(True)


def finalize(
    ax: Axes,
    theme: Theme,
    *,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
) -> None:
    """Apply title and axis labels with the theme's ink colors."""
    if title:
        ax.set_title(
            title,
            color=theme.primary_ink,
            fontsize=13,
            fontweight="bold",
            loc="left",
            pad=12,
        )
    if xlabel is not None:
        ax.set_xlabel(xlabel, color=theme.secondary_ink)
    if ylabel is not None:
        ax.set_ylabel(ylabel, color=theme.secondary_ink)


def add_legend(ax: Axes, theme: Theme) -> None:
    """Add a recessive legend (only call when there are >= 2 labeled series)."""
    legend = ax.legend(
        frameon=False,
        labelcolor=theme.secondary_ink,
        fontsize=10,
        loc="best",
    )
    if legend is not None:
        legend.set_title(None)


def format_value(v: float) -> str:
    """Compact human-readable formatting for direct labels."""
    try:
        fv = float(v)
    except (TypeError, ValueError):
        return str(v)
    if fv != fv:  # NaN
        return ""
    if abs(fv) >= 1000:
        return f"{fv:,.0f}"
    if fv.is_integer():
        return f"{int(fv)}"
    return f"{fv:,.2f}"
