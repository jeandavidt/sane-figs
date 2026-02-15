"""Tests for presets module."""

import pytest

from sane_figs.core.presets import (
    ARTICLE_PRESET,
    PRESENTATION_PRESET,
    get_preset,
    list_presets,
)



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
