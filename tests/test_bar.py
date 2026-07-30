"""Tests for viz.bar."""

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
def sales():
    return pd.DataFrame(
        {
            "region": ["North", "South", "East", "West"],
            "revenue": [120, 90, 150, 60],
        }
    )


@pytest.fixture
def tidy():
    return pd.DataFrame(
        {
            "quarter": ["Q1", "Q1", "Q2", "Q2"],
            "channel": ["web", "store", "web", "store"],
            "responses": [10, 5, 12, 7],
        }
    )


def test_returns_axes(sales):
    ax = viz.bar(sales, x="region", y="revenue")
    assert isinstance(ax, Axes)


def test_single_series_bar_count(sales):
    ax = viz.bar(sales, x="region", y="revenue")
    # One patch per category.
    assert len(ax.patches) == 4


def test_single_series_uses_slot_one_hue(sales):
    ax = viz.bar(sales, x="region", y="revenue")
    assert to_hex(ax.patches[0].get_facecolor()) == viz.LIGHT.categorical[0]


def test_count_when_y_omitted():
    df = pd.DataFrame({"grade": ["A", "B", "A", "A", "B", "C"]})
    ax = viz.bar(df, x="grade")
    assert len(ax.patches) == 3
    heights = sorted(p.get_height() for p in ax.patches)
    assert heights == [1, 2, 3]  # C=1, B=2, A=3


def test_sort_desc_orders_categories(sales):
    ax = viz.bar(sales, x="region", y="revenue", sort="desc")
    heights = [p.get_height() for p in ax.patches]
    assert heights == sorted(heights, reverse=True)


def test_sort_asc_orders_categories(sales):
    ax = viz.bar(sales, x="region", y="revenue", sort="asc")
    heights = [p.get_height() for p in ax.patches]
    assert heights == sorted(heights)


def test_grouped_bar_series_count(tidy):
    ax = viz.bar(tidy, x="quarter", y="responses", by="channel")
    # 2 quarters x 2 channels = 4 bars.
    assert len(ax.patches) == 4
    # Two distinct series colors.
    colors = {to_hex(p.get_facecolor()) for p in ax.patches}
    assert viz.LIGHT.categorical[0] in colors
    assert viz.LIGHT.categorical[1] in colors


def test_grouped_bar_has_legend(tidy):
    ax = viz.bar(tidy, x="quarter", y="responses", by="channel")
    assert ax.get_legend() is not None


def test_stacked_bar_stacks(tidy):
    ax = viz.bar(tidy, x="quarter", y="responses", by="channel", stacked=True)
    # Still 4 patches, but the second series sits on top (nonzero y offset).
    bottoms = [p.get_y() for p in ax.patches]
    assert any(b > 0 for b in bottoms)


def test_horizontal_orientation(sales):
    ax = viz.bar(sales, x="region", y="revenue", horizontal=True)
    # Horizontal bars have varying widths, constant-ish heights.
    widths = [p.get_width() for p in ax.patches]
    assert max(widths) == 150


def test_highlight_emphasis_colors(sales):
    ax = viz.bar(sales, x="region", y="revenue", highlight="East")
    faces = {
        cat: to_hex(p.get_facecolor())
        for cat, p in zip(["North", "South", "East", "West"], ax.patches)
    }
    assert faces["East"] == viz.LIGHT.emphasis
    assert faces["North"] == viz.LIGHT.deemphasis
    # No legend in emphasis mode.
    assert ax.get_legend() is None


def test_label_auto_labels_single_extreme(sales):
    ax = viz.bar(sales, x="region", y="revenue", label="auto")
    texts = [t.get_text() for t in ax.texts]
    assert texts == ["150"]  # only the max bar


def test_label_true_labels_all(sales):
    ax = viz.bar(sales, x="region", y="revenue", label=True)
    assert len(ax.texts) == 4


def test_label_false_no_labels(sales):
    ax = viz.bar(sales, x="region", y="revenue", label=False)
    assert len(ax.texts) == 0


def test_folds_beyond_eight_series():
    df = pd.DataFrame(
        {
            "x": ["a"] * 10,
            "grp": [f"s{i}" for i in range(10)],
            "v": list(range(1, 11)),
        }
    )
    with pytest.warns(UserWarning, match="folded"):
        ax = viz.bar(df, x="x", y="v", by="grp")
    # 8 columns max after folding (7 kept + Other).
    assert len(ax.patches) == 8


def test_draws_into_supplied_ax(sales):
    fig, ax = plt.subplots()
    returned = viz.bar(sales, x="region", y="revenue", ax=ax)
    assert returned is ax


def test_theme_override_per_call(sales):
    ax = viz.bar(sales, x="region", y="revenue", theme="dark")
    assert to_hex(ax.patches[0].get_facecolor()) == viz.DARK.categorical[0]


def test_palette_override(sales):
    ax = viz.bar(sales, x="region", y="revenue", palette=["#123456"])
    assert to_hex(ax.patches[0].get_facecolor()) == "#123456"


def test_texture_hatches_grouped_series(tidy):
    ax = viz.bar(tidy, x="quarter", y="responses", by="channel", texture=True)
    hatches = {p.get_hatch() for p in ax.patches}
    assert len(hatches) > 1  # distinct per series


def test_no_texture_by_default(tidy):
    ax = viz.bar(tidy, x="quarter", y="responses", by="channel")
    assert all(p.get_hatch() is None for p in ax.patches)


def test_subtitle_and_caption_render(sales):
    ax = viz.bar(
        sales,
        x="region",
        y="revenue",
        title="Revenue",
        subtitle="by region, Q3",
        caption="Source: demo",
    )
    texts = {t.get_text() for t in ax.texts}
    assert "by region, Q3" in texts
    assert "Source: demo" in texts


def test_shadcn_theme_rounds_bars_and_hides_spines(sales):
    from matplotlib.patches import PathPatch

    ax = viz.bar(sales, x="region", y="revenue", theme="shadcn")
    # Rounded bars are PathPatches, not plain Rectangles.
    assert all(isinstance(p, PathPatch) for p in ax.patches)
    assert ax.spines["left"].get_visible() is False
    assert ax.spines["bottom"].get_visible() is False
    # Value (y) axis is hidden: no y tick labels.
    assert all(t.get_text() == "" for t in ax.get_yticklabels())


def test_default_theme_keeps_square_bars(sales):
    from matplotlib.patches import Rectangle

    ax = viz.bar(sales, x="region", y="revenue")
    assert all(isinstance(p, Rectangle) for p in ax.patches)
    assert ax.spines["left"].get_visible() is True


def test_invalid_column_raises(sales):
    with pytest.raises(KeyError):
        viz.bar(sales, x="nope", y="revenue")


def test_invalid_sort_raises(sales):
    with pytest.raises(ValueError, match="sort"):
        viz.bar(sales, x="region", y="revenue", sort="upward")
