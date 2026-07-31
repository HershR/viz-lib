"""Tests for viz.scatter."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes
from matplotlib.colors import to_hex

import chartcn as viz


@pytest.fixture(autouse=True)
def _light_theme():
    viz.set_theme("light")
    yield
    plt.close("all")


@pytest.fixture
def points():
    return pd.DataFrame(
        {
            "height": [150, 160, 170, 180, 190],
            "weight": [50, 60, 65, 80, 90],
            "group": ["A", "A", "B", "B", "B"],
            "pop": [1, 5, 2, 9, 4],
        }
    )


def test_returns_axes(points):
    assert isinstance(viz.scatter(points, x="height", y="weight"), Axes)


def test_single_group_one_collection_slot_one(points):
    ax = viz.scatter(points, x="height", y="weight")
    assert len(ax.collections) == 1
    assert to_hex(ax.collections[0].get_facecolor()[0]) == viz.LIGHT.categorical[0]


def test_grouped_collections_and_legend(points):
    ax = viz.scatter(points, x="height", y="weight", by="group")
    assert len(ax.collections) == 2
    assert ax.get_legend() is not None


def test_size_scales_marker_area(points):
    ax = viz.scatter(points, x="height", y="weight", size="pop")
    sizes = ax.collections[0].get_sizes()
    assert len(sizes) == 5
    assert sizes.min() < sizes.max()  # varies with pop


def test_no_size_constant_area(points):
    ax = viz.scatter(points, x="height", y="weight")
    sizes = ax.collections[0].get_sizes()
    assert len(set(np.round(sizes, 3))) == 1


def test_highlight_emphasis(points):
    # group order is first-seen: A then B
    ax = viz.scatter(points, x="height", y="weight", by="group", highlight="A")
    faces = [to_hex(c.get_facecolor()[0]) for c in ax.collections]
    assert faces[0] == viz.LIGHT.emphasis  # A highlighted
    assert faces[1] == viz.LIGHT.deemphasis  # B grayed
    assert ax.get_legend() is None  # legend dropped in emphasis mode


def test_texture_distinct_markers(points):
    ax = viz.scatter(points, x="height", y="weight", by="group", texture=True)
    p0 = ax.collections[0].get_paths()[0].vertices
    p1 = ax.collections[1].get_paths()[0].vertices
    # Different marker shapes -> different path vertices.
    assert p0.shape != p1.shape or not np.array_equal(p0, p1)


def test_y_is_required(points):
    with pytest.raises(TypeError):
        viz.scatter(points, x="height")  # missing y


def test_theme_and_palette_override(points):
    ax = viz.scatter(points, x="height", y="weight", theme="dark")
    assert to_hex(ax.collections[0].get_facecolor()[0]) == viz.DARK.categorical[0]
    ax = viz.scatter(points, x="height", y="weight", palette=["#0f0f0f"])
    assert to_hex(ax.collections[0].get_facecolor()[0]) == "#0f0f0f"


def test_draws_into_supplied_ax(points):
    fig, ax = plt.subplots()
    assert viz.scatter(points, x="height", y="weight", ax=ax) is ax


def test_invalid_column_raises(points):
    with pytest.raises(KeyError):
        viz.scatter(points, x="height", y="nope")
