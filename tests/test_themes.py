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


def test_shadcn_themes_resolve_and_carry_validated_palette():
    from vizlib.themes import resolve_theme

    assert resolve_theme("shadcn") is viz.SHADCN
    assert resolve_theme("shadcn-dark") is viz.SHADCN_DARK
    # Same validated palette as light/dark — only the chrome/shape changes.
    assert viz.SHADCN.categorical == viz.LIGHT.categorical
    assert viz.SHADCN_DARK.categorical == viz.DARK.categorical


def test_shadcn_style_knobs():
    for th in (viz.SHADCN, viz.SHADCN_DARK):
        assert th.axis_lines is False
        assert th.bar_radius > 0
    # Classic themes keep the default chrome.
    assert viz.LIGHT.axis_lines is True
    assert viz.LIGHT.bar_radius == 0.0


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
