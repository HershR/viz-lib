"""Shared post-styling helpers used by every chart function.

The contract each chart follows: validate input -> resolve theme -> call
matplotlib -> post-style here -> return the ``Axes``. These helpers own the
"post-style" step so styling stays consistent across chart types.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path

from .themes import Theme


def new_axes(theme: Theme, ax: Axes | None) -> Axes:
    """Return the axes to draw on: the caller's, or a fresh themed one."""
    if ax is not None:
        return ax
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.set_facecolor(theme.surface)
    return ax


def style_axes(
    ax: Axes,
    theme: Theme,
    *,
    grid_axis: str | None = "y",
    value_axis: str | None = None,
) -> None:
    """Apply recessive chrome to ``ax``: surface, spines, ticks, and hairline grid.

    ``grid_axis`` is "y" (default), "x", "both", or ``None`` for no grid. Gridlines
    are solid hairlines one shade off the surface; the top/right spines are removed
    and the remaining spines are hairlines in the baseline token (hidden entirely when
    ``theme.axis_lines`` is False). ``value_axis`` ("y"/"x") names the value axis; when
    ``theme.value_axis`` is False its tick labels are dropped (the grid carries it).
    """
    ax.set_facecolor(theme.surface)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        if theme.axis_lines:
            ax.spines[side].set_visible(True)
            ax.spines[side].set_color(theme.baseline)
            ax.spines[side].set_linewidth(1.0)
        else:
            ax.spines[side].set_visible(False)

    ax.tick_params(
        colors=theme.muted,
        labelcolor=theme.secondary_ink,
        labelsize=theme.type_scale["tick"],
        length=0,
    )

    if value_axis and not theme.value_axis:
        if value_axis == "y":
            ax.tick_params(axis="y", labelleft=False, left=False)
        elif value_axis == "x":
            ax.tick_params(axis="x", labelbottom=False, bottom=False)

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
    subtitle: str | None = None,
    caption: str | None = None,
) -> None:
    """Apply the title, optional subtitle/caption, and axis labels.

    The title is a bold, left-justified upper-left line in primary ink; the subtitle
    sits just beneath it in secondary ink; the caption is a muted source line at the
    lower-left. All sizes come from the theme's type scale so the hierarchy is
    deliberate (title > subtitle > axis label > tick > annotation > caption).
    """
    scale = theme.type_scale
    if title:
        ax.set_title(
            title,
            color=theme.primary_ink,
            fontsize=scale["title"],
            fontweight="bold",
            loc="left",
            pad=28 if subtitle else 12,
        )
    if subtitle:
        ax.annotate(
            subtitle,
            xy=(0, 1),
            xycoords="axes fraction",
            xytext=(0, 8),
            textcoords="offset points",
            ha="left",
            va="bottom",
            color=theme.secondary_ink,
            fontsize=scale["subtitle"],
            annotation_clip=False,
        )
    if caption:
        ax.annotate(
            caption,
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(0, -40),
            textcoords="offset points",
            ha="left",
            va="top",
            color=theme.muted,
            fontsize=scale["caption"],
            annotation_clip=False,
        )
    if xlabel is not None:
        ax.set_xlabel(xlabel, color=theme.secondary_ink, fontsize=scale["label"])
    if ylabel is not None:
        ax.set_ylabel(ylabel, color=theme.secondary_ink, fontsize=scale["label"])


def add_legend(ax: Axes, theme: Theme) -> None:
    """Add a recessive legend (only call when there are >= 2 labeled series)."""
    legend = ax.legend(
        frameon=False,
        labelcolor=theme.secondary_ink,
        fontsize=theme.type_scale["legend"],
        loc="best",
    )
    if legend is not None:
        legend.set_title(None)


def _rounded_bar_path(x0, y0, w, h, r, horizontal):
    """A rectangle path with its two data-end corners rounded by radius ``r``.

    Vertical bars round the top (away from the y=0 baseline); horizontal bars round
    the right end. ``r`` is clamped to half the thickness and the bar length.
    """
    if horizontal:
        r = max(0.0, min(r, abs(h) / 2, abs(w)))
        # Round the right corners.
        verts = [
            (x0, y0),
            (x0 + w - r, y0),
            (x0 + w, y0),  # control -> bottom-right corner
            (x0 + w, y0 + r),
            (x0 + w, y0 + h - r),
            (x0 + w, y0 + h),  # control -> top-right corner
            (x0 + w - r, y0 + h),
            (x0, y0 + h),
            (x0, y0),
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
    else:
        r = max(0.0, min(r, abs(w) / 2, abs(h)))
        # Round the top corners.
        verts = [
            (x0, y0),
            (x0, y0 + h - r),
            (x0, y0 + h),  # control -> top-left corner
            (x0 + r, y0 + h),
            (x0 + w - r, y0 + h),
            (x0 + w, y0 + h),  # control -> top-right corner
            (x0 + w, y0 + h - r),
            (x0 + w, y0),
            (x0, y0),
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
    return Path(verts, codes)


def round_bars(ax, containers, theme, *, horizontal, only_top_segment=False):
    """Replace bar rectangles with rounded-data-end path patches (shadcn look).

    ``containers`` is the list of BarContainers drawn for the chart. Each rectangle
    is swapped for a :class:`PathPatch` with the same style so colors, hatches, and
    edges survive. ``only_top_segment`` rounds just the last container (stacked-bar
    tops); otherwise every bar is rounded.
    """
    if theme.bar_radius <= 0:
        return
    targets = containers[-1:] if only_top_segment else containers
    for container in targets:
        # A BarContainer exposes .patches; hist may return a plain patch list.
        rects = getattr(container, "patches", container)
        for rect in list(rects):
            w, h = rect.get_width(), rect.get_height()
            if w == 0 or h == 0:
                continue
            thickness = abs(h) if horizontal else abs(w)
            r = theme.bar_radius * thickness
            path = _rounded_bar_path(rect.get_x(), rect.get_y(), w, h, r, horizontal)
            patch = PathPatch(
                path,
                facecolor=rect.get_facecolor(),
                edgecolor=rect.get_edgecolor(),
                linewidth=rect.get_linewidth(),
                hatch=rect.get_hatch(),
                zorder=rect.get_zorder(),
            )
            rect.remove()
            ax.add_patch(patch)


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
