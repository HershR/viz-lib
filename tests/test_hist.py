"""Tests for viz.hist."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes
from matplotlib.colors import to_hex

import chartcn as viz


@pytest.fixture(autouse=True)
def _classic_theme():
    # Bin assertions introspect Rectangle patches; the default (shadcn) rounds them
    # into PathPatches, so run these under the classic theme.
    viz.set_theme("classic")
    yield
    plt.close("all")


@pytest.fixture
def dist():
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "value": rng.normal(size=200),
            "cohort": np.where(rng.random(200) < 0.5, "new", "returning"),
        }
    )


def test_returns_axes(dist):
    assert isinstance(viz.hist(dist, x="value"), Axes)


def test_single_group_bins_and_slot_one(dist):
    ax = viz.hist(dist, x="value", bins=10)
    assert len(ax.patches) == 10
    assert to_hex(ax.patches[0].get_facecolor()) == viz.LIGHT.categorical[0]


def test_multi_group_overlaid_and_legend(dist):
    ax = viz.hist(dist, x="value", by="cohort", bins=10)
    # nbins * ngroups patches (10 * 2), overlaid.
    assert len(ax.patches) == 20
    assert ax.get_legend() is not None


def test_multi_group_uses_categorical_colors(dist):
    ax = viz.hist(dist, x="value", by="cohort", bins=5)
    colors = {to_hex(p.get_facecolor()) for p in ax.patches}
    assert viz.LIGHT.categorical[0] in colors
    assert viz.LIGHT.categorical[1] in colors


def test_shared_bins_align_across_groups(dist):
    ax = viz.hist(dist, x="value", by="cohort", bins=8)
    lefts = sorted({round(p.get_x(), 6) for p in ax.patches})
    # Both groups share the same 8 bin left-edges (not 16 distinct).
    assert len(lefts) == 8


def test_highlight_emphasis(dist):
    ax = viz.hist(dist, x="value", by="cohort", bins=6, highlight="new")
    colors = {to_hex(p.get_facecolor()) for p in ax.patches}
    assert viz.LIGHT.emphasis in colors  # highlighted distribution
    assert viz.LIGHT.deemphasis in colors  # faded context
    assert ax.get_legend() is None  # legend dropped in emphasis mode


def test_default_theme_rounds_bins(dist):
    from matplotlib.patches import PathPatch

    # Default look is shadcn: rounded bins, no spines.
    ax = viz.hist(dist, x="value", bins=6, theme="light")
    assert any(isinstance(p, PathPatch) for p in ax.patches)
    assert ax.spines["left"].get_visible() is False


def test_texture_hatches_groups(dist):
    ax = viz.hist(dist, x="value", by="cohort", bins=6, texture=True)
    hatches = {p.get_hatch() for p in ax.patches}
    assert len(hatches) > 1


def test_theme_and_palette_override(dist):
    ax = viz.hist(dist, x="value", bins=5, theme="dark")
    assert to_hex(ax.patches[0].get_facecolor()) == viz.DARK.categorical[0]
    ax = viz.hist(dist, x="value", bins=5, palette=["#654321"])
    assert to_hex(ax.patches[0].get_facecolor()) == "#654321"


def test_draws_into_supplied_ax(dist):
    fig, ax = plt.subplots()
    assert viz.hist(dist, x="value", ax=ax) is ax


def test_invalid_column_raises(dist):
    with pytest.raises(KeyError):
        viz.hist(dist, x="nope")
