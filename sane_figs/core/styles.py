"""Style definitions for sane-figs.

Styles determine visual appearance (colors, fonts, grid settings, etc.)
independent of figure sizing.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import TitleConfig, LegendConfig, AxisTitleSpacingConfig

from sane_figs.styling.layout import PlotStyle, TitleConfig, LegendConfig, AxisTitleSpacingConfig
from sane_figs.styling.colorways import COLORBLIND_SAFE_COLORWAY, BIOMATH_COLORWAY


@dataclass
class Style:
    """
    A style defining visual appearance independent of sizing.

    Styles control colors, fonts, grid settings, and other visual
    aesthetics that can be applied across different modes.

    Attributes:
        name: Name of the style.
        font_family: Font family to use.
        colorway: Color palette to use.
        plot_style: Grid, spines, and background settings.
        title_config: Title alignment configuration.
        legend_config: Legend positioning configuration.
        axis_title_spacing: Axis title spacing configuration.
        watermark: Optional watermark configuration.
    """

    name: str
    font_family: str = "sans-serif"
    colorway: "Colorway | None" = None
    plot_style: PlotStyle = field(default_factory=PlotStyle)
    title_config: "TitleConfig | None" = None
    legend_config: "LegendConfig | None" = None
    axis_title_spacing: "AxisTitleSpacingConfig | None" = None
    watermark: "WatermarkConfig | None" = None


# Style registry
_STYLE_REGISTRY: dict[str, Style] = {}


def register_style(style: Style) -> None:
    """
    Register a style in the registry.

    Args:
        style: The Style object to register.

    Raises:
        ValueError: If the style name is a built-in style that already exists.
    """
    built_in = ["default", "modeleau", "biomath"]
    if style.name in built_in and style.name in _STYLE_REGISTRY:
        raise ValueError(
            f"Cannot re-register built-in style '{style.name}'. Use a different name."
        )
    _STYLE_REGISTRY[style.name] = style


def unregister_style(name: str) -> None:
    """
    Unregister a style by name.

    Args:
        name: The name of the style to unregister.

    Raises:
        ValueError: If the style is not found or is a built-in style.
    """
    if name not in _STYLE_REGISTRY:
        raise ValueError(f"Style '{name}' not found.")

    built_in = ["default", "modeleau", "biomath"]
    if name in built_in:
        raise ValueError(f"Cannot unregister built-in style '{name}'.")

    del _STYLE_REGISTRY[name]


def get_style(name: str | Style) -> Style:
    """
    Get a style by name.

    Args:
        name: The style name or a Style object (returned as-is).

    Returns:
        The Style object.

    Raises:
        ValueError: If the style is not recognized.
    """
    if isinstance(name, Style):
        return name

    if name not in _STYLE_REGISTRY:
        raise ValueError(
            f"Unknown style '{name}'. Available styles: {list(_STYLE_REGISTRY.keys())}"
        )
    return _STYLE_REGISTRY[name]


def list_styles() -> list[str]:
    """
    List all available style names.

    Returns:
        List of style names.
    """
    return list(_STYLE_REGISTRY.keys())


# Built-in styles

# Default Style
# Clean, professional look with light grid
_DEFAULT_STYLE = Style(
    name="default",
    font_family="sans-serif",
    colorway=None,  # Will use DEFAULT_COLORWAY
    plot_style=PlotStyle(),
    title_config=TitleConfig(alignment="center"),
    legend_config=LegendConfig(position="inside_upper_right"),
    axis_title_spacing=AxisTitleSpacingConfig(),
    watermark=None,
)

# ModelEAU Style
# Uses colorblind-safe colors with Arial font for accessibility
_MODELEAU_STYLE = Style(
    name="modeleau",
    font_family="Arial",
    colorway=COLORBLIND_SAFE_COLORWAY,
    plot_style=PlotStyle(),
    title_config=TitleConfig(alignment="center"),
    legend_config=LegendConfig(position="inside_upper_right"),
    axis_title_spacing=AxisTitleSpacingConfig(),
    watermark=None,
)

# Biomath Style
# Uses UGent Bioscience Engineering colors with monospace font
_BIOMATH_STYLE = Style(
    name="biomath",
    font_family="monospace",
    colorway=BIOMATH_COLORWAY,
    plot_style=PlotStyle(),
    title_config=TitleConfig(alignment="center"),
    legend_config=LegendConfig(position="inside_upper_right"),
    axis_title_spacing=AxisTitleSpacingConfig(),
    watermark=None,
)

# Register built-in styles
register_style(_DEFAULT_STYLE)
register_style(_MODELEAU_STYLE)
register_style(_BIOMATH_STYLE)

# Export for convenience
DEFAULT_STYLE = _DEFAULT_STYLE
MODELEAU_STYLE = _MODELEAU_STYLE
BIOMATH_STYLE = _BIOMATH_STYLE
