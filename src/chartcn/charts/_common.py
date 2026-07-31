"""Helpers shared by the chart functions: data shaping, series folding, and color
assignment. Keeping these here (rather than in one chart module) lets every chart
apply the same fixed-palette, fold-past-8, and emphasis rules.
"""

from __future__ import annotations

import warnings

import pandas as pd
from matplotlib.colors import to_rgb

# Series past this count are folded into "Other" rather than generating new hues.
MAX_SERIES = 8

# Secondary-encoding channels for the opt-in ``texture=`` mode — fixed ordered
# sequences (parallel to the fixed categorical order) so a series keeps the same
# non-color cue regardless of how many series are present. Used only for print /
# colorblind legibility, never by default. Slot 1 is the plain form (solid).
HATCHES = ("", "//", "\\\\", "xx", "--", "||", "..", "++")
LINESTYLES = (
    "-",
    "--",
    "-.",
    ":",
    (0, (3, 1, 1, 1)),
    (0, (5, 1)),
    (0, (1, 1)),
    (0, (4, 2)),
)
MARKERS = ("o", "s", "^", "D", "v", "P", "X", "*")


def channel(seq, i):
    """Pick the i-th entry of a secondary-encoding sequence, cycling if needed."""
    return seq[i % len(seq)]


def darken(color, factor: float = 0.55):
    """Return a darker shade of ``color`` (for a hatch/edge that reads in grayscale)."""
    r, g, b = to_rgb(color)
    return (r * factor, g * factor, b * factor)


def as_set(value) -> set:
    """Normalize a scalar / list / None into a set (for ``highlight=``)."""
    if value is None:
        return set()
    if isinstance(value, (list, tuple, set)):
        return set(value)
    return {value}


def with_palette(theme, palette):
    """Return a copy of ``theme`` with its categorical colors replaced."""
    if palette is None:
        return theme
    return theme.__class__(**{**theme.__dict__, "categorical": tuple(palette)})


def aggregate_matrix(
    df: pd.DataFrame, x: str, y: str | None, by: str | None, agg: str = "sum"
) -> pd.DataFrame:
    """Reduce ``df`` to a (categories x series) matrix of values.

    Single series -> one column named after ``y`` (or "count"). With ``by`` set ->
    one column per ``by`` value, in first-seen order. ``y=None`` counts rows; a
    given ``y`` is reduced with ``agg`` ("sum" for magnitude, "mean" for a trend).
    """
    if by is None:
        if y is None:
            series = df.groupby(x, sort=False).size()
            series.name = "count"
        else:
            series = df.groupby(x, sort=False)[y].agg(agg)
        return series.to_frame()

    if y is None:
        grouped = df.groupby([x, by], sort=False).size()
    else:
        grouped = df.groupby([x, by], sort=False)[y].agg(agg)
    matrix = grouped.unstack(by)
    col_order = list(dict.fromkeys(df[by]))
    row_order = list(dict.fromkeys(df[x]))
    matrix = matrix.reindex(index=row_order, columns=col_order)
    return matrix.fillna(0)


def fold_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """Keep the top 7 series by total, fold the rest into a single "Other" column."""
    if matrix.shape[1] <= MAX_SERIES:
        return matrix
    totals = matrix.sum(axis=0).sort_values(ascending=False)
    keep = set(totals.index[: MAX_SERIES - 1])
    kept_cols = [c for c in matrix.columns if c in keep]  # preserve original order
    other_cols = [c for c in matrix.columns if c not in keep]
    warnings.warn(
        f"{matrix.shape[1]} series exceeds the {MAX_SERIES}-hue limit; "
        f"folded {len(other_cols)} into 'Other'.",
        stacklevel=3,
    )
    folded = matrix[kept_cols].copy()
    folded["Other"] = matrix[other_cols].sum(axis=1)
    return folded


def split_groups(df: pd.DataFrame, by: str | None) -> list[tuple[object, pd.DataFrame]]:
    """Split ``df`` into ``[(group_name, subframe)]`` in first-seen order.

    ``by=None`` yields a single unnamed group. Used by charts that plot raw rows
    (scatter, hist) rather than an aggregated matrix.
    """
    if by is None:
        return [(None, df)]
    names = list(dict.fromkeys(df[by]))
    return [(name, df[df[by] == name]) for name in names]


def fold_groups(
    groups: list[tuple[object, pd.DataFrame]],
) -> list[tuple[object, pd.DataFrame]]:
    """Fold groups past ``MAX_SERIES`` into a combined "Other" (top-7 by row count)."""
    if len(groups) <= MAX_SERIES:
        return groups
    ranked = sorted(groups, key=lambda g: len(g[1]), reverse=True)
    keep_names = {name for name, _ in ranked[: MAX_SERIES - 1]}
    kept = [(name, sub) for name, sub in groups if name in keep_names]
    other = [sub for name, sub in groups if name not in keep_names]
    warnings.warn(
        f"{len(groups)} groups exceeds the {MAX_SERIES}-hue limit; "
        f"folded {len(other)} into 'Other'.",
        stacklevel=3,
    )
    kept.append(("Other", pd.concat(other)))
    return kept


def resolve_colors(columns, theme, highlight_set) -> tuple[list[str], bool]:
    """Map each series/group name to a color. Returns (colors, emphasis_mode).

    In emphasis mode (``highlight_set`` non-empty) matched names take the accent hue
    and the rest go muted gray. Otherwise names take the fixed categorical slots in
    order, with an "Other" fold column pinned to the muted token.
    """
    if highlight_set:
        colors = [
            theme.emphasis if col in highlight_set else theme.deemphasis
            for col in columns
        ]
        return colors, True
    colors = []
    for i, col in enumerate(columns):
        if col == "Other":
            colors.append(theme.muted)
        else:
            colors.append(theme.categorical[i % len(theme.categorical)])
    return colors, False
