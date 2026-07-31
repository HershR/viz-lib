"""Render-matrix smoke tests.

Rather than pixel-compare against committed baselines (fragile across matplotlib /
font versions), this exercises every chart across its option combinations and all
themes, asserting each renders without error and produces the expected artists.
Portable and fast — it catches "this combination raises" and "nothing got drawn".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes

import vizlib as viz

THEMES = [None, "light", "dark", "classic", "classic-dark", "lime", "lime-dark"]

SALES = pd.DataFrame(
    {"region": ["North", "South", "East", "West"], "revenue": [120, 90, 150, 60]}
)
TIDY = pd.DataFrame(
    {
        "quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3"],
        "channel": ["Web", "Store"] * 3,
        "responses": [30, 18, 42, 25, 38, 30],
    }
)
TREND = pd.DataFrame(
    {
        "month": [1, 2, 3, 4] * 2,
        "plan": ["Pro"] * 4 + ["Free"] * 4,
        "users": [5, 9, 14, 20, 12, 15, 17, 19],
    }
)
POINTS = pd.DataFrame(
    {
        "x": np.linspace(0, 10, 30),
        "y": np.linspace(0, 5, 30) + np.tile([0, 1, -1], 10),
        "grp": (["A"] * 10) + (["B"] * 10) + (["C"] * 10),
        "w": np.arange(1, 31),
    }
)
DIST = pd.DataFrame(
    {
        "value": np.concatenate([np.linspace(0, 5, 100), np.linspace(3, 9, 100)]),
        "cohort": ["new"] * 100 + ["returning"] * 100,
    }
)


@pytest.fixture(autouse=True)
def _reset():
    viz.set_theme("light")
    yield
    plt.close("all")


def _ok(ax):
    assert isinstance(ax, Axes)
    assert ax.figure is not None


BAR_SINGLE = [
    {"x": "region", "y": "revenue"},
    {"x": "region", "y": "revenue", "sort": "desc"},
    {"x": "region", "y": "revenue", "sort": "asc"},
    {"x": "region", "y": "revenue", "horizontal": True},
    {"x": "region", "y": "revenue", "highlight": "East"},
    {"x": "region", "y": "revenue", "label": True},
    {"x": "region", "y": "revenue", "label": False},
    {"x": "region"},  # count (y omitted)
]
BAR_GROUPED = [
    {"x": "quarter", "y": "responses", "by": "channel"},
    {"x": "quarter", "y": "responses", "by": "channel", "stacked": True},
    {"x": "quarter", "y": "responses", "by": "channel", "horizontal": True},
    {"x": "quarter", "y": "responses", "by": "channel", "highlight": "Web"},
    {"x": "quarter", "y": "responses", "by": "channel", "texture": True},
    {
        "x": "quarter",
        "y": "responses",
        "by": "channel",
        "stacked": True,
        "texture": True,
    },
]
LINE_CASES = [
    {"x": "month", "y": "users"},
    {"x": "month", "y": "users", "by": "plan"},
    {"x": "month", "y": "users", "by": "plan", "highlight": "Pro"},
    {"x": "month", "y": "users", "by": "plan", "label": True},
    {"x": "month", "y": "users", "by": "plan", "texture": True},
    {"x": "month"},  # count
]
SCATTER_CASES = [
    {"x": "x", "y": "y"},
    {"x": "x", "y": "y", "by": "grp"},
    {"x": "x", "y": "y", "size": "w"},
    {"x": "x", "y": "y", "by": "grp", "highlight": "A"},
    {"x": "x", "y": "y", "by": "grp", "texture": True},
]
HIST_CASES = [
    {"x": "value"},
    {"x": "value", "bins": 8},
    {"x": "value", "by": "cohort"},
    {"x": "value", "by": "cohort", "highlight": "new"},
    {"x": "value", "by": "cohort", "texture": True},
]


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("kw", BAR_SINGLE)
def test_bar_single_matrix(theme, kw):
    ax = viz.bar(SALES, theme=theme, **kw)
    _ok(ax)
    assert len(ax.patches) == len(SALES)


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("kw", BAR_GROUPED)
def test_bar_grouped_matrix(theme, kw):
    ax = viz.bar(TIDY, theme=theme, **kw)
    _ok(ax)
    assert len(ax.patches) == 6  # 3 quarters x 2 channels


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("kw", LINE_CASES)
def test_line_matrix(theme, kw):
    ax = viz.line(TREND, theme=theme, **kw)
    _ok(ax)
    assert len(ax.lines) >= 1


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("kw", SCATTER_CASES)
def test_scatter_matrix(theme, kw):
    ax = viz.scatter(POINTS, theme=theme, **kw)
    _ok(ax)
    assert len(ax.collections) >= 1


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("kw", HIST_CASES)
def test_hist_matrix(theme, kw):
    ax = viz.hist(DIST, theme=theme, **kw)
    _ok(ax)
    assert len(ax.patches) >= 1
