"""Tests for the theming engine."""

import matplotlib as mpl
import pytest

import vizlib as viz
from vizlib.themes import apply_theme, resolve_theme


def test_builtin_themes_have_eight_categorical_hues():
    for th in (viz.LIGHT, viz.DARK):
        assert len(th.categorical) == 8
        assert all(c.startswith("#") for c in th.categorical)


def test_resolve_theme_by_name_and_instance():
    assert resolve_theme("light") is viz.LIGHT
    assert resolve_theme("dark") is viz.DARK
    assert resolve_theme(viz.DARK) is viz.DARK


def test_resolve_theme_none_returns_active():
    viz.set_theme("light")
    assert resolve_theme(None) is viz.LIGHT


def test_resolve_theme_unknown_name_raises():
    with pytest.raises(ValueError, match="unknown theme"):
        resolve_theme("neon")


def test_set_theme_updates_rcparams():
    viz.set_theme("dark")
    assert mpl.rcParams["axes.facecolor"] == viz.DARK.surface
    viz.set_theme("light")
    assert mpl.rcParams["axes.facecolor"] == viz.LIGHT.surface


def test_theme_context_manager_restores_previous():
    viz.set_theme("light")
    with viz.theme("dark") as active:
        assert active is viz.DARK
        assert viz.get_theme() is viz.DARK
    assert viz.get_theme() is viz.LIGHT


def test_theme_is_immutable():
    with pytest.raises(Exception):
        viz.LIGHT.surface = "#000000"


def test_default_light_dark_are_shadcn_styled():
    # The default look is shadcn: rounded bars, no spines, both axes labeled.
    for th in (viz.LIGHT, viz.DARK):
        assert th.axis_lines is False
        assert th.bar_radius > 0
        assert th.value_axis is True
    # ...over vizlib's validated CVD-safe palette (blue lead), not coral/teal.
    assert viz.LIGHT.categorical[0] == "#2a78d6"
    assert viz.LIGHT.categorical == viz.CLASSIC.categorical


def test_classic_themes_keep_the_original_chrome():
    from vizlib.themes import resolve_theme

    assert resolve_theme("classic") is viz.CLASSIC
    assert resolve_theme("classic-dark") is viz.CLASSIC_DARK
    for th in (viz.CLASSIC, viz.CLASSIC_DARK):
        assert th.axis_lines is True
        assert th.bar_radius == 0.0
        assert th.value_axis is True


def test_theme_type_scale_is_hierarchical():
    ts = viz.LIGHT.type_scale
    assert ts["title"] > ts["subtitle"] > ts["label"]
    assert ts["label"] >= ts["tick"] >= ts["annotation"] > ts["caption"]
    # Custom themes inherit the same scale by default.
    assert viz.LIME.type_scale["title"] == ts["title"]


def test_prop_cycle_matches_categorical():
    apply_theme(viz.LIGHT)
    cycle_colors = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
    assert cycle_colors == list(viz.LIGHT.categorical)
