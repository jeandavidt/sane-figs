"""Tests for colorways module."""

import pytest

from sane_figs.styling.colorways import (
    COLORBLIND_SAFE_COLORWAY,
    DEFAULT_COLORWAY,
    NATURE_COLORWAY,
    PASTEL_COLORWAY,
    VIBRANT_COLORWAY,
    Colorway,
    get_colorway,
    list_colorways,
    register_colorway,
    unregister_colorway,
)


def test_default_colorway():
    """Test default colorway configuration."""
    assert DEFAULT_COLORWAY.name == "default"
    assert len(DEFAULT_COLORWAY.categorical) == 10
    assert len(DEFAULT_COLORWAY.sequential) == 9
    assert len(DEFAULT_COLORWAY.diverging) == 11
    assert len(DEFAULT_COLORWAY.qualitative) == 10


def test_nature_colorway():
    """Test nature colorway configuration."""
    assert NATURE_COLORWAY.name == "nature"
    assert len(NATURE_COLORWAY.categorical) == 10
    assert len(NATURE_COLORWAY.sequential) == 10
    assert len(NATURE_COLORWAY.diverging) == 11
    assert len(NATURE_COLORWAY.qualitative) == 10


def test_vibrant_colorway():
    """Test vibrant colorway configuration."""
    assert VIBRANT_COLORWAY.name == "vibrant"
    assert len(VIBRANT_COLORWAY.categorical) == 10
    assert len(VIBRANT_COLORWAY.sequential) == 10
    assert len(VIBRANT_COLORWAY.diverging) == 11
    assert len(VIBRANT_COLORWAY.qualitative) == 10


def test_pastel_colorway():
    """Test pastel colorway configuration."""
    assert PASTEL_COLORWAY.name == "pastel"
    assert len(PASTEL_COLORWAY.categorical) == 10
    assert len(PASTEL_COLORWAY.sequential) == 10
    assert len(PASTEL_COLORWAY.diverging) == 11
    assert len(PASTEL_COLORWAY.qualitative) == 10


def test_colorblind_safe_colorway():
    """Test colorblind-safe colorway configuration."""
    assert COLORBLIND_SAFE_COLORWAY.name == "colorblind-safe"
    assert len(COLORBLIND_SAFE_COLORWAY.categorical) == 8
    assert len(COLORBLIND_SAFE_COLORWAY.sequential) == 9
    assert len(COLORBLIND_SAFE_COLORWAY.diverging) == 10
    assert len(COLORBLIND_SAFE_COLORWAY.qualitative) == 8


def test_get_colorway():
    """Test getting colorway by name."""
    default = get_colorway("default")
    assert default.name == "default"

    nature = get_colorway("nature")
    assert nature.name == "nature"


def test_get_colorway_invalid():
    """Test getting colorway with invalid name."""
    with pytest.raises(ValueError, match="Unknown colorway"):
        get_colorway("invalid")


def test_list_colorways():
    """Test listing available colorways."""
    colorways = list_colorways()
    assert "default" in colorways
    assert "nature" in colorways
    assert "vibrant" in colorways
    assert "pastel" in colorways
    assert "colorblind-safe" in colorways
    assert len(colorways) >= 5


def test_register_colorway():
    """Test registering a custom colorway."""
    custom = Colorway(
        name="custom",
        description="Custom colorway",
        categorical=["#FF0000", "#00FF00", "#0000FF"],
        sequential=["#FF0000", "#00FF00", "#0000FF"],
        diverging=["#FF0000", "#00FF00", "#0000FF"],
        qualitative=["#FF0000", "#00FF00", "#0000FF"],
    )

    register_colorway(custom)

    # Verify it was registered
    retrieved = get_colorway("custom")
    assert retrieved.name == "custom"

    # Clean up
    unregister_colorway("custom")


def test_register_colorway_duplicate():
    """Test registering a colorway with duplicate name."""
    with pytest.raises(ValueError, match="already exists"):
        register_colorway(DEFAULT_COLORWAY)


def test_unregister_colorway():
    """Test unregistering a colorway."""
    custom = Colorway(
        name="custom2",
        description="Custom colorway 2",
        categorical=["#FF0000", "#00FF00", "#0000FF"],
        sequential=["#FF0000", "#00FF00", "#0000FF"],
        diverging=["#FF0000", "#00FF00", "#0000FF"],
        qualitative=["#FF0000", "#00FF00", "#0000FF"],
    )

    register_colorway(custom)
    unregister_colorway("custom2")

    # Verify it was unregistered
    with pytest.raises(ValueError, match="Unknown colorway"):
        get_colorway("custom2")


def test_unregister_colorway_not_found():
    """Test unregistering a colorway that doesn't exist."""
    with pytest.raises(ValueError, match="not found"):
        unregister_colorway("nonexistent")


def test_unregister_colorway_builtin():
    """Test unregistering a built-in colorway."""
    with pytest.raises(ValueError, match="Cannot unregister built-in"):
        unregister_colorway("default")
