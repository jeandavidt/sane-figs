"""Tests for watermarks module."""

import pytest

from sane_figs.styling.watermarks import (
    WatermarkConfig,
    create_image_watermark,
    create_text_watermark,
    get_watermark_position,
)


def test_create_text_watermark():
    """Test creating a text watermark configuration."""
    watermark = create_text_watermark("© 2025 My Lab")

    assert watermark.text == "© 2025 My Lab"
    assert watermark.image_path is None
    assert watermark.position == "bottom-right"
    assert watermark.opacity == 0.3
    assert watermark.font_size == 12.0


def test_create_text_watermark_custom():
    """Test creating a text watermark with custom settings."""
    watermark = create_text_watermark(
        "Draft",
        position="center",
        opacity=0.5,
        font_size=20,
        font_weight="bold",
        font_color="#FF0000",
    )

    assert watermark.text == "Draft"
    assert watermark.position == "center"
    assert watermark.opacity == 0.5
    assert watermark.font_size == 20.0
    assert watermark.font_weight == "bold"
    assert watermark.font_color == "#FF0000"


def test_create_image_watermark(tmp_path):
    """Test creating an image watermark configuration."""
    # Create a temporary image file
    import os

    image_path = tmp_path / "test.png"
    # Create a minimal PNG file
    with open(image_path, "wb") as f:
        # Write a minimal PNG header (1x1 transparent pixel)
        f.write(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
            b"\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )

    watermark = create_image_watermark(str(image_path))

    assert watermark.image_path == str(image_path)
    assert watermark.text is None
    assert watermark.position == "bottom-right"
    assert watermark.opacity == 0.3
    assert watermark.scale == 0.1


def test_create_image_watermark_not_found():
    """Test creating an image watermark with non-existent file."""
    with pytest.raises(FileNotFoundError, match="Image file not found"):
        create_image_watermark("nonexistent.png")


def test_watermark_config_validation():
    """Test WatermarkConfig validation."""
    # Test invalid position
    with pytest.raises(ValueError, match="Invalid position"):
        WatermarkConfig(text="Test", position="invalid")

    # Test invalid opacity
    with pytest.raises(ValueError, match="Opacity must be between"):
        WatermarkConfig(text="Test", opacity=1.5)

    # Test invalid scale
    with pytest.raises(ValueError, match="Scale must be between"):
        WatermarkConfig(text="Test", scale=1.5)

    # Test invalid margin
    with pytest.raises(ValueError, match="Margin must be a tuple"):
        WatermarkConfig(text="Test", margin=(0.5,))

    # Test invalid margin values
    with pytest.raises(ValueError, match="Margin values must be between"):
        WatermarkConfig(text="Test", margin=(1.5, 0.5))

    # Test no image or text
    with pytest.raises(ValueError, match="Either image_path or text must be provided"):
        WatermarkConfig()


def test_get_watermark_position():
    """Test watermark position calculation."""
    # Test top-left
    x, y = get_watermark_position("top-left", 100, 100, 10, 10, 0.02, 0.02)
    assert x == 2.0
    assert y == 88.0

    # Test top-right
    x, y = get_watermark_position("top-right", 100, 100, 10, 10, 0.02, 0.02)
    assert x == 88.0
    assert y == 88.0

    # Test bottom-left
    x, y = get_watermark_position("bottom-left", 100, 100, 10, 10, 0.02, 0.02)
    assert x == 2.0
    assert y == 2.0

    # Test bottom-right
    x, y = get_watermark_position("bottom-right", 100, 100, 10, 10, 0.02, 0.02)
    assert x == 88.0
    assert y == 2.0

    # Test center
    x, y = get_watermark_position("center", 100, 100, 10, 10, 0.02, 0.02)
    assert x == 45.0
    assert y == 45.0


def test_get_watermark_position_invalid():
    """Test watermark position calculation with invalid position."""
    with pytest.raises(ValueError, match="Unknown position"):
        get_watermark_position("invalid", 100, 100, 10, 10, 0.02, 0.02)
