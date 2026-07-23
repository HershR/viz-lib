"""vizlib — an opinionated matplotlib wrapper for pandas DataFrames.

Good defaults, applied automatically: colorblind-safe palettes, recessive chrome,
selective labels, an emphasis mode, and a real dark theme. Every chart returns the
underlying matplotlib ``Axes`` so you can always drop down to raw matplotlib.

    >>> import vizlib as viz
    >>> ax = viz.bar(sales, x="region", y="revenue", sort="desc")
"""

from __future__ import annotations

from .charts import bar
from .themes import DARK, LIGHT, Theme, get_theme, set_theme, theme

__version__ = "0.1.0"

__all__ = [
    "bar",
    "Theme",
    "LIGHT",
    "DARK",
    "set_theme",
    "get_theme",
    "theme",
    "__version__",
]
