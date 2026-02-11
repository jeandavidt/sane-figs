"""Watermark system for sane-figs."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class WatermarkConfig:
    """
    Configuration for adding watermarks to figures.

    Attributes:
        image_path: Path to an image file for the watermark (optional).
        text: Text to use as watermark (optional).
        position: Position of the watermark ('top-left', 'top-right',
            'bottom-left', 'bottom-right', 'center').
        opacity: Opacity of the watermark (0.0 to 1.0).
        scale: Scale of the watermark relative to figure size (0.0 to 1.0).
        margin: Margin as (x, y) fraction of figure size.
        font_size: Font size for text watermarks (in points).
        font_family: Font family for text watermarks.
        font_weight: Font weight for text watermarks.
        font_color: Font color for text watermarks.
    """

    image_path: str | None = None
    text: str | None = None
    position: str = "bottom-right"
    opacity: float = 0.3
    scale: float = 0.1
    margin: tuple[float, float] = (0.02, 0.02)
    font_size: float = 12.0
    font_family: str = "sans-serif"
    font_weight: str = "normal"
    font_color: str = "#000000"

    def __post_init__(self) -> None:
        """Validate the watermark configuration."""
        if self.image_path is None and self.text is None:
            raise ValueError("Either image_path or text must be provided.")

        valid_positions = [
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "center",
        ]
        if self.position not in valid_positions:
            raise ValueError(
                f"Invalid position '{self.position}'. "
                f"Valid positions: {valid_positions}"
            )

        if not 0.0 <= self.opacity <= 1.0:
            raise ValueError(f"Opacity must be between 0.0 and 1.0, got {self.opacity}")

        if not 0.0 <= self.scale <= 1.0:
            raise ValueError(f"Scale must be between 0.0 and 1.0, got {self.scale}")

        if len(self.margin) != 2:
            raise ValueError(f"Margin must be a tuple of 2 values, got {self.margin}")

        if not (0.0 <= self.margin[0] <= 1.0 and 0.0 <= self.margin[1] <= 1.0):
            raise ValueError(
                f"Margin values must be between 0.0 and 1.0, got {self.margin}"
            )


def create_text_watermark(
    text: str,
    position: str = "bottom-right",
    opacity: float = 0.3,
    font_size: float = 12.0,
    font_family: str = "sans-serif",
    font_weight: str = "normal",
    font_color: str = "#000000",
    **kwargs,
) -> WatermarkConfig:
    """
    Create a text watermark configuration.

    Args:
        text: The text to use as watermark.
        position: Position of the watermark.
        opacity: Opacity of the watermark (0.0 to 1.0).
        font_size: Font size in points.
        font_family: Font family.
        font_weight: Font weight.
        font_color: Font color.
        **kwargs: Additional arguments passed to WatermarkConfig.

    Returns:
        A WatermarkConfig object for a text watermark.

    Example:
        >>> import sane_figs
        >>> watermark = sane_figs.create_text_watermark(
        ...     '© 2025 My Lab',
        ...     position='bottom-right',
        ...     opacity=0.3
        ... )
    """
    return WatermarkConfig(
        text=text,
        position=position,
        opacity=opacity,
        font_size=font_size,
        font_family=font_family,
        font_weight=font_weight,
        font_color=font_color,
        **kwargs,
    )


def create_image_watermark(
    image_path: str,
    position: str = "bottom-right",
    opacity: float = 0.3,
    scale: float = 0.1,
    margin: tuple[float, float] = (0.02, 0.02),
    **kwargs,
) -> WatermarkConfig:
    """
    Create an image watermark configuration.

    Args:
        image_path: Path to the image file.
        position: Position of the watermark.
        opacity: Opacity of the watermark (0.0 to 1.0).
        scale: Scale of the watermark relative to figure size.
        margin: Margin as (x, y) fraction of figure size.
        **kwargs: Additional arguments passed to WatermarkConfig.

    Returns:
        A WatermarkConfig object for an image watermark.

    Example:
        >>> import sane_figs
        >>> watermark = sane_figs.create_image_watermark(
        ...     'logo.png',
        ...     position='bottom-right',
        ...     opacity=0.2,
        ...     scale=0.1
        ... )
    """
    # Validate that the image file exists
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    return WatermarkConfig(
        image_path=image_path,
        position=position,
        opacity=opacity,
        scale=scale,
        margin=margin,
        **kwargs,
    )


def get_watermark_position(
    position: str,
    figure_width: float,
    figure_height: float,
    watermark_width: float,
    watermark_height: float,
    margin_x: float,
    margin_y: float,
) -> tuple[float, float]:
    """
    Calculate the (x, y) position for a watermark.

    Args:
        position: Position string ('top-left', 'top-right', etc.).
        figure_width: Width of the figure.
        figure_height: Height of the figure.
        watermark_width: Width of the watermark.
        watermark_height: Height of the watermark.
        margin_x: Horizontal margin as fraction of figure size.
        margin_y: Vertical margin as fraction of figure size.

    Returns:
        Tuple of (x, y) coordinates for the watermark.
    """
    margin_x_px = figure_width * margin_x
    margin_y_px = figure_height * margin_y

    if position == "top-left":
        x = margin_x_px
        y = figure_height - watermark_height - margin_y_px
    elif position == "top-right":
        x = figure_width - watermark_width - margin_x_px
        y = figure_height - watermark_height - margin_y_px
    elif position == "bottom-left":
        x = margin_x_px
        y = margin_y_px
    elif position == "bottom-right":
        x = figure_width - watermark_width - margin_x_px
        y = margin_y_px
    elif position == "center":
        x = (figure_width - watermark_width) / 2
        y = (figure_height - watermark_height) / 2
    else:
        raise ValueError(f"Unknown position: {position}")

    return (x, y)
