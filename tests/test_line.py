"""Tests for viz.line."""

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.axes import Axes
from matplotlib.colors import to_hex

import vizlib as viz


@pytest.fixture(autouse=True)
def _light_theme():
    viz.set_theme("light")
    yield
    plt.close("all")


@pytest.fixture
def trend():
    return pd.DataFrame({"month": [1, 2, 3, 4], "revenue": [10, 14, 12, 20]})


@pytest.fixture
def multi():
    return pd.DataFrame(
        {
            "month": [1, 2, 3, 1, 2, 3],
            "plan": ["Pro", "Pro", "Pro", "Free", "Free", "Free"],
            "users": [5, 8, 13, 20, 22, 25],
        }
    )


def test_returns_axes(trend):
    assert isinstance(viz.line(trend, x="month", y="revenue"), Axes)


def test_single_series_one_line_slot_one(trend):
    ax = viz.line(trend, x="month", y="revenue")
    assert len(ax.lines) == 1
    assert to_hex(ax.lines[0].get_color()) == viz.LIGHT.categorical[0]


def test_multi_series_colors(multi):
    ax = viz.line(multi, x="month", y="users", by="plan")
    assert len(ax.lines) == 2
    colors = {to_hex(ln.get_color()) for ln in ax.lines}
    assert colors == {viz.LIGHT.categorical[0], viz.LIGHT.categorical[1]}


def test_small_multi_series_direct_labeled_no_legend(multi):
    # <= 4 series + label="auto": lines are labeled by name at their ends, and the
    # legend is dropped (direct labeling beats a legend).
    ax = viz.line(multi, x="month", y="users", by="plan")
    assert ax.get_legend() is None
    assert {"Pro", "Free"} <= {t.get_text() for t in ax.texts}


def test_many_series_keep_legend():
    df = pd.DataFrame(
        {
            "t": list(range(4)) * 5,
            "g": sum(([f"s{i}"] * 4 for i in range(5)), []),
            "v": list(range(20)),
        }
    )
    ax = viz.line(df, x="t", y="v", by="g")  # 5 series > direct-label cap
    assert ax.get_legend() is not None


def test_label_false_multi_keeps_legend_no_labels(multi):
    ax = viz.line(multi, x="month", y="users", by="plan", label=False)
    assert ax.get_legend() is not None
    assert len(ax.texts) == 0


def test_numeric_x_sorted(trend):
    shuffled = trend.sample(frac=1, random_state=0)
    ax = viz.line(shuffled, x="month", y="revenue")
    xdata = ax.lines[0].get_xdata()
    assert list(xdata) == sorted(xdata)


def test_highlight_emphasis(multi):
    ax = viz.line(multi, x="month", y="users", by="plan", highlight="Pro")
    colors = {}
    for ln in ax.lines:
        colors[ln.get_label()] = to_hex(ln.get_color())
    assert colors["Pro"] == viz.LIGHT.emphasis
    assert colors["Free"] == viz.LIGHT.deemphasis
    assert ax.get_legend() is None


def test_label_auto_single_endpoint(trend):
    ax = viz.line(trend, x="month", y="revenue", label="auto")
    assert [t.get_text() for t in ax.texts] == ["20"]  # last point


def test_label_true_labels_each_endpoint(multi):
    ax = viz.line(multi, x="month", y="users", by="plan", label=True)
    assert len(ax.texts) == 2


def test_count_when_y_omitted():
    df = pd.DataFrame({"day": [1, 1, 2, 3, 3, 3]})
    ax = viz.line(df, x="day")
    ydata = ax.lines[0].get_ydata()
    assert list(ydata) == [2, 1, 3]  # counts per day, sorted by day


def test_folds_beyond_eight_series():
    df = pd.DataFrame(
        {
            "t": [1, 2] * 10,
            "g": sum(([f"s{i}"] * 2 for i in range(10)), []),
            "v": list(range(20)),
        }
    )
    with pytest.warns(UserWarning, match="folded"):
        ax = viz.line(df, x="t", y="v", by="g")
    assert len(ax.lines) == 8


def test_texture_distinct_linestyles(multi):
    ax = viz.line(multi, x="month", y="users", by="plan", texture=True)
    styles = {ln.get_linestyle() for ln in ax.lines}
    assert len(styles) > 1


def test_no_texture_default_solid(multi):
    ax = viz.line(multi, x="month", y="users", by="plan")
    assert {ln.get_linestyle() for ln in ax.lines} == {"-"}


def test_theme_and_palette_override(trend):
    ax = viz.line(trend, x="month", y="revenue", theme="dark")
    assert to_hex(ax.lines[0].get_color()) == viz.DARK.categorical[0]
    ax = viz.line(trend, x="month", y="revenue", palette=["#abcdef"])
    assert to_hex(ax.lines[-1].get_color()) == "#abcdef"


def test_draws_into_supplied_ax(trend):
    fig, ax = plt.subplots()
    assert viz.line(trend, x="month", y="revenue", ax=ax) is ax


def test_invalid_column_raises(trend):
    with pytest.raises(KeyError):
        viz.line(trend, x="month", y="nope")
