"""Themes: a small bundle of palettes + chrome + typography, plus the global
theme state and the matplotlib ``rcParams`` application.

The default look is **shadcn** — :data:`LIGHT` / :data:`DARK` carry the shadcn
aesthetic (rounded bar ends, no axis spines, hidden value axis, zinc/card neutrals)
over vizlib's validated colorblind-safe palette. :data:`CLASSIC` / :data:`CLASSIC_DARK`
preserve the original vizlib look, and :data:`LIME` / :data:`LIME_DARK` is a custom
theme. A theme is applied globally with :func:`set_theme` or scoped with the
:func:`theme` context manager; individual chart calls can also override per-call via
their ``theme=`` argument.
"""

from __future__ import annotations

import contextlib
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType

import matplotlib as mpl
from cycler import cycler

from . import palettes

# Deliberate type scale (points). Title is largest, then subtitle, axis labels,
# ticks, data-label annotations, and source captions — a readable hierarchy the
# charts pull from rather than sprinkling ad-hoc sizes.
_TYPE_SCALE: Mapping[str, int] = MappingProxyType(
    {
        "title": 15,
        "subtitle": 12,
        "label": 11,
        "legend": 10,
        "tick": 10,
        "annotation": 9,
        "caption": 8,
    }
)


@dataclass(frozen=True)
class Theme:
    """An immutable bundle of the colors and typography a chart draws with.

    Build one of these to define a custom look, or use the built-in :data:`LIGHT`
    and :data:`DARK`. Pass it to :func:`set_theme`, :func:`theme`, or any chart's
    ``theme=`` argument.
    """

    name: str
    surface: str
    primary_ink: str
    secondary_ink: str
    muted: str
    gridline: str
    baseline: str
    categorical: tuple[str, ...]
    sequential: tuple[str, ...]
    diverging: tuple[str, str, str]  # (low pole, midpoint, high pole)
    emphasis: str
    deemphasis: str
    font_family: tuple[str, ...] = field(default=("sans-serif",))
    type_scale: Mapping[str, int] = field(default_factory=lambda: _TYPE_SCALE)
    # Chrome/shape style knobs (defaults preserve the classic look).
    axis_lines: bool = True  # draw the left/bottom hairline spines
    bar_radius: float = 0.0  # fraction of bar thickness to round the data-end corners
    value_axis: bool = True  # show the value-axis ticks/labels (shadcn hides them)

    @classmethod
    def from_mode(cls, mode: str) -> "Theme":
        """Assemble a theme from the validated palette tokens for ``mode``."""
        return cls(
            name=mode,
            surface=palettes.SURFACE[mode],
            primary_ink=palettes.PRIMARY_INK[mode],
            secondary_ink=palettes.SECONDARY_INK[mode],
            muted=palettes.MUTED[mode],
            gridline=palettes.GRIDLINE[mode],
            baseline=palettes.BASELINE[mode],
            categorical=palettes.CATEGORICAL[mode],
            sequential=palettes.SEQUENTIAL[mode],
            diverging=palettes.DIVERGING[mode],
            emphasis=palettes.EMPHASIS[mode],
            deemphasis=palettes.DEEMPHASIS[mode],
            font_family=palettes.FONT_FAMILY.get(mode, ("sans-serif",)),
        )


# The default look is shadcn: rounded bar ends, no axis spines, a hidden value axis
# (a faint horizontal grid carries it), zinc/card neutrals, and an Arial-metric sans
# — over vizlib's validated colorblind-safe palette.
_SHADCN_CHROME = dict(axis_lines=False, bar_radius=0.10, value_axis=False)
LIGHT = replace(Theme.from_mode("light"), **_SHADCN_CHROME)
DARK = replace(Theme.from_mode("dark"), **_SHADCN_CHROME)
# "classic" — the original vizlib look (hairline spines, visible value axis, square
# bars, default sans), kept for anyone who wants it.
CLASSIC = replace(Theme.from_mode("classic"), name="classic")
CLASSIC_DARK = replace(Theme.from_mode("classic-dark"), name="classic-dark")
# "Lime Green" — a custom theme ported from a shadcn theme (lime primary).
LIME = Theme.from_mode("lime")
LIME_DARK = Theme.from_mode("lime-dark")

_BUILTIN: dict[str, Theme] = {
    "light": LIGHT,
    "dark": DARK,
    "classic": CLASSIC,
    "classic-dark": CLASSIC_DARK,
    "lime": LIME,
    "lime-dark": LIME_DARK,
}
_active: Theme = LIGHT


def resolve_theme(theme: Theme | str | None) -> Theme:
    """Turn a ``theme=`` argument into a concrete :class:`Theme`.

    ``None`` -> the active global theme; a name -> the matching built-in; a
    :class:`Theme` -> itself.
    """
    if theme is None:
        return _active
    if isinstance(theme, Theme):
        return theme
    if isinstance(theme, str):
        try:
            return _BUILTIN[theme]
        except KeyError:
            raise ValueError(
                f"unknown theme {theme!r}; expected one of {sorted(_BUILTIN)} "
                f"or a Theme instance"
            ) from None
    raise TypeError(f"theme must be a str, Theme, or None; got {type(theme).__name__}")


def apply_theme(theme: Theme) -> None:
    """Write ``theme`` into matplotlib's global ``rcParams``.

    This sets the defaults new figures inherit. Chart functions additionally style
    their own axes so a caller-supplied ``ax`` is themed regardless of rcParams.
    """
    mpl.rcParams.update(
        {
            "figure.facecolor": theme.surface,
            "axes.facecolor": theme.surface,
            "savefig.facecolor": theme.surface,
            "text.color": theme.primary_ink,
            "axes.titlecolor": theme.primary_ink,
            "axes.labelcolor": theme.secondary_ink,
            "axes.edgecolor": theme.baseline,
            "xtick.color": theme.muted,
            "ytick.color": theme.muted,
            "xtick.labelcolor": theme.secondary_ink,
            "ytick.labelcolor": theme.secondary_ink,
            "grid.color": theme.gridline,
            "grid.linewidth": 0.8,
            "axes.grid": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.family": list(theme.font_family),
            "axes.prop_cycle": cycler(color=list(theme.categorical)),
            "axes.titlesize": theme.type_scale["title"],
            "axes.labelsize": theme.type_scale["label"],
            "xtick.labelsize": theme.type_scale["tick"],
            "ytick.labelsize": theme.type_scale["tick"],
            "legend.fontsize": theme.type_scale["legend"],
        }
    )


def set_theme(theme: Theme | str) -> Theme:
    """Set the global default theme (by name or :class:`Theme`) and return it."""
    resolved = resolve_theme(theme)
    global _active
    _active = resolved
    apply_theme(resolved)
    return resolved


def get_theme() -> Theme:
    """Return the active global theme."""
    return _active


@contextlib.contextmanager
def theme(theme: Theme | str):
    """Temporarily activate ``theme`` for the duration of the ``with`` block."""
    previous = _active
    try:
        yield set_theme(theme)
    finally:
        set_theme(previous)


# Apply the default so importing vizlib themes matplotlib immediately.
apply_theme(_active)
