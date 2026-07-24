"""Chart functions. Each takes a DataFrame and returns a matplotlib Axes."""

from .bar import bar
from .hist import hist
from .line import line
from .scatter import scatter

__all__ = ["bar", "line", "scatter", "hist"]
