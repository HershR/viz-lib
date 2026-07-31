"""chartcn — an opinionated matplotlib wrapper for pandas DataFrames.

Good defaults, applied automatically: colorblind-safe palettes, recessive chrome,
selective labels, an emphasis mode, and a real dark theme. Every chart returns the
underlying matplotlib ``Axes`` so you can always drop down to raw matplotlib.

    >>> import chartcn as viz
    >>> ax = viz.bar(sales, x="region", y="revenue", sort="desc")
"""

from __future__ import annotations

from .charts import bar, hist, line, scatter
from .themes import (
    CLASSIC,
    CLASSIC_DARK,
    DARK,
    LIGHT,
    LIME,
    LIME_DARK,
    Theme,
    get_theme,
    set_theme,
    theme,
)

__version__ = "0.1.0"

__all__ = [
    "bar",
    "line",
    "scatter",
    "hist",
    "Theme",
    "LIGHT",
    "DARK",
    "CLASSIC",
    "CLASSIC_DARK",
    "LIME",
    "LIME_DARK",
    "set_theme",
    "get_theme",
    "theme",
    "__version__",
]
