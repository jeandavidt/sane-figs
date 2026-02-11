"""Tests for presets module."""

import pytest

from sane_figs.core.presets import (
    ARTICLE_PRESET,
    PRESENTATION_PRESET,
    get_preset,
    list_presets,
)


def test_article_preset():
    """Test article preset configuration."""
    assert ARTICLE_PRESET.name == "article"
    assert ARTICLE_PRESET.mode == "article"
    assert ARTICLE_PRESET.figure_size == (3.5, 2.625)
    assert ARTICLE_PRESET.dpi == 300
    assert ARTICLE_PRESET.font_size["title"] == 9.0
    assert ARTICLE_PRESET.font_size["label"] == 8.0
    assert ARTICLE_PRESET.font_size["legend"] == 7.0
    assert ARTICLE_PRESET.font_size["tick"] == 7.0
    assert ARTICLE_PRESET.line_width == 1.0
    assert ARTICLE_PRESET.marker_size == 4.0


def test_presentation_preset():
    """Test presentation preset configuration."""
    assert PRESENTATION_PRESET.name == "presentation"
    assert PRESENTATION_PRESET.mode == "presentation"
    assert PRESENTATION_PRESET.figure_size == (13.33, 7.5)
    assert PRESENTATION_PRESET.dpi == 150
    assert PRESENTATION_PRESET.font_size["title"] == 28.0
    assert PRESENTATION_PRESET.font_size["label"] == 24.0
    assert PRESENTATION_PRESET.font_size["legend"] == 20.0
    assert PRESENTATION_PRESET.font_size["tick"] == 20.0
    assert PRESENTATION_PRESET.line_width == 3.0
    assert PRESENTATION_PRESET.marker_size == 10.0


def test_get_preset():
    """Test getting preset by mode."""
    article = get_preset("article")
    assert article.name == "article"

    presentation = get_preset("presentation")
    assert presentation.name == "presentation"


def test_get_preset_invalid():
    """Test getting preset with invalid mode."""
    with pytest.raises(ValueError, match="Unknown preset"):
        get_preset("invalid")


def test_list_presets():
    """Test listing available presets."""
    presets = list_presets()
    assert "article" in presets
    assert "presentation" in presets
    # At minimum, we should have the built-in presets
    assert len(presets) >= 2
