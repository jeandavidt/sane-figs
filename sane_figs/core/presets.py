"""Style presets for sane-figs.

Presets are now containers that combine a Mode (sizing/dimensions) with a
Style (visual appearance). This allows for flexible combinations like
article-sized figures with presentation-style colors.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.modes import Mode
    from sane_figs.core.styles import Style
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import TitleConfig, LegendConfig, AxisTitleSpacingConfig

from sane_figs.styling.colorways import (
    ULAVAL_COLORWAY,
    MODELEAU_COLORWAY,
    MARIMO_COLORWAY,
    DEFAULT_COLORWAY,
    VIBRANT_COLORWAY,
)
from sane_figs.styling.layout import (
    PlotStyle,
    TitleConfig,
    LegendConfig,
    AxisTitleSpacingConfig,
)


@dataclass
class Preset:
    """
    A preset combining a Mode (sizing) with a Style (visual appearance).

    Presets are the primary way users configure figure styling in sane-figs.
    They combine:
    - Mode: Figure dimensions, DPI, font sizes, line/marker sizing
    - Style: Colors, fonts, grid settings, and other visual aesthetics

    Attributes:
        name: Name of the preset.
        mode: The mode identifier ('article', 'presentation', etc.).
        figure_size: Figure size as (width, height) in inches.
        dpi: Dots per inch for output.
        font_family: Font family to use.
        font_size: Dictionary of font sizes for different elements.
        line_width: Line width for plots.
        marker_size: Marker size for scatter plots.
        screen_dpi: DPI for screen/display rendering.
        plot_style: Shared visual chrome (grid, spines, background, …).
        colorway: Colorway to use.
        watermark: Optional watermark configuration.
        title_config: Configuration for title alignment.
        legend_config: Configuration for legend positioning.
        axis_title_spacing: Configuration for axis title spacing.
    """

    name: str
    mode: str
    figure_size: tuple[float, float]
    dpi: int
    font_family: str
    font_size: dict[str, float] = field(default_factory=dict)
    line_width: float = 1.5
    marker_size: float = 6.0
    screen_dpi: int | None = None
    plot_style: PlotStyle = field(default_factory=PlotStyle)
    colorway: "Colorway | None" = None
    watermark: "WatermarkConfig | None" = None
    title_config: "TitleConfig | None" = None
    legend_config: "LegendConfig | None" = None
    axis_title_spacing: "AxisTitleSpacingConfig | None" = None

    @classmethod
    def from_mode_and_style(
        cls,
        name: str,
        mode: "Mode | str",
        style: "Style | str",
    ) -> "Preset":
        """
        Create a Preset from a Mode and Style.

        This is the primary constructor for creating presets in the new
        architecture, allowing flexible combinations of sizing and styling.

        Args:
            name: Name for the preset.
            mode: A Mode object or mode name ('article', 'presentation').
            style: A Style object or style name ('default').

        Returns:
            A new Preset combining the mode and style.

        Example:
            >>> from sane_figs import Preset, get_mode, get_style
            >>> preset = Preset.from_mode_and_style(
            ...     name="article-nature",
            ...     mode="article",
            ...     style="default",
            ... )
        """
        from sane_figs.core.modes import get_mode as _get_mode
        from sane_figs.core.styles import get_style as _get_style
        from sane_figs.styling.colorways import DEFAULT_COLORWAY

        # Resolve mode
        if isinstance(mode, str):
            mode_obj = _get_mode(mode)
        else:
            mode_obj = mode

        # Resolve style
        if isinstance(style, str):
            style_obj = _get_style(style)
        else:
            style_obj = style

        # Use style's colorway or default
        colorway = style_obj.colorway if style_obj.colorway is not None else DEFAULT_COLORWAY

        return cls(
            name=name,
            mode=mode_obj.name,
            figure_size=mode_obj.figure_size,
            dpi=mode_obj.dpi,
            screen_dpi=mode_obj.screen_dpi,
            font_family=style_obj.font_family,
            font_size=dict(mode_obj.font_sizes),
            line_width=mode_obj.line_width,
            marker_size=mode_obj.marker_size,
            plot_style=PlotStyle(
                background_color=style_obj.plot_style.background_color,
                grid_visible=style_obj.plot_style.grid_visible,
                grid_color=style_obj.plot_style.grid_color,
                grid_opacity=style_obj.plot_style.grid_opacity,
                grid_width=style_obj.plot_style.grid_width,
                axis_line_color=style_obj.plot_style.axis_line_color,
                axis_line_width=style_obj.plot_style.axis_line_width,
                show_top_spine=style_obj.plot_style.show_top_spine,
                show_right_spine=style_obj.plot_style.show_right_spine,
                tick_direction=style_obj.plot_style.tick_direction,
                tick_length=style_obj.plot_style.tick_length,
                tick_color=style_obj.plot_style.tick_color,
                title_weight=style_obj.plot_style.title_weight,
                legend_frame_opacity=style_obj.plot_style.legend_frame_opacity,
                legend_edge_color=style_obj.plot_style.legend_edge_color,
            ),
            colorway=colorway,
            watermark=style_obj.watermark,
            title_config=style_obj.title_config,
            legend_config=style_obj.legend_config,
            axis_title_spacing=style_obj.axis_title_spacing,
        )

    def get_display_dpi(self) -> int:
        """DPI for HTML/screen rendering (Plotly, Altair).

        Returns screen_dpi if set, otherwise defaults to 100 (standard screen DPI).
        Print/image outputs should use the dpi field directly.
        """
        return self.screen_dpi if self.screen_dpi is not None else 100

    def to_yaml_dict(self) -> dict:
        """
        Convert the preset to a dictionary suitable for YAML serialization.

        Returns:
            Dictionary representation in the new format with mode/style sections.
        """
        result = {"name": self.name}

        # Mode section
        result["mode"] = {
            "name": self.mode,
            "figure_size": list(self.figure_size),
            "dpi": self.dpi,
            "screen_dpi": self.screen_dpi,
            "font_sizes": dict(self.font_size),
            "line_width": self.line_width,
            "marker_size": self.marker_size,
        }

        # Style section
        style_dict = {
            "name": f"{self.mode}-style",
            "font_family": self.font_family,
        }

        # Add colorway if present
        if self.colorway is not None:
            style_dict["colorway"] = {"name": self.colorway.name}

        # Add plot_style
        style_dict["plot_style"] = {
            "background_color": self.plot_style.background_color,
            "grid_visible": self.plot_style.grid_visible,
            "grid_color": self.plot_style.grid_color,
            "grid_opacity": self.plot_style.grid_opacity,
            "grid_width": self.plot_style.grid_width,
            "axis_line_color": self.plot_style.axis_line_color,
            "axis_line_width": self.plot_style.axis_line_width,
            "show_top_spine": self.plot_style.show_top_spine,
            "show_right_spine": self.plot_style.show_right_spine,
            "tick_direction": self.plot_style.tick_direction,
            "tick_length": self.plot_style.tick_length,
            "tick_color": self.plot_style.tick_color,
            "title_weight": self.plot_style.title_weight,
            "legend_frame_opacity": self.plot_style.legend_frame_opacity,
            "legend_edge_color": self.plot_style.legend_edge_color,
        }

        # Add title config if present
        if self.title_config is not None:
            style_dict["title"] = {"alignment": self.title_config.alignment}

        # Add legend config if present
        if self.legend_config is not None:
            style_dict["legend"] = {
                "position": self.legend_config.position,
                "alignment": self.legend_config.alignment,
                "x_offset": self.legend_config.x_offset,
                "y_offset": self.legend_config.y_offset,
            }

        # Add axis title spacing if present
        if self.axis_title_spacing is not None:
            style_dict["axis_title_spacing"] = {
                "x_spacing": self.axis_title_spacing.x_spacing,
                "y_spacing": self.axis_title_spacing.y_spacing,
                "plotly_multiplier": self.axis_title_spacing.plotly_multiplier,
                "altair_multiplier": self.axis_title_spacing.altair_multiplier,
                "matplotlib_multiplier": self.axis_title_spacing.matplotlib_multiplier,
            }

        # Add watermark if present
        if self.watermark is not None:
            wm = self.watermark
            style_dict["watermark"] = {
                "type": "image" if wm.image_path else "text",
            }
            if wm.text:
                style_dict["watermark"]["text"] = wm.text
            if wm.image_path:
                style_dict["watermark"]["image_path"] = wm.image_path
            style_dict["watermark"].update({
                "position": wm.position,
                "opacity": wm.opacity,
                "scale": wm.scale,
                "margin": list(wm.margin),
                "font_size": wm.font_size,
                "font_family": wm.font_family,
                "font_weight": wm.font_weight,
                "font_color": wm.font_color,
            })

        result["style"] = style_dict

        return result


# Preset registry
_PRESET_REGISTRY: dict[str, Preset] = {}


def register_preset(preset: Preset) -> None:
    """
    Register a preset in the registry.

    Args:
        preset: The Preset object to register.

    Raises:
        ValueError: If a preset with the same name is a built-in preset
            ('article' or 'presentation').
    """
    # Prevent re-registration of built-in presets
    built_in = ["article", "presentation", "ulaval", "modeleau", "marimo", "latex"]
    if preset.name in built_in and preset.name in _PRESET_REGISTRY:
        raise ValueError(
            f"Cannot re-register built-in preset '{preset.name}'. "
            "Use a different name."
        )
    _PRESET_REGISTRY[preset.name] = preset


def unregister_preset(name: str) -> None:
    """
    Unregister a preset by name.

    Args:
        name: The name of the preset to unregister.

    Raises:
        ValueError: If the preset is not found or is a built-in preset.
    """
    if name not in _PRESET_REGISTRY:
        raise ValueError(f"Preset '{name}' not found.")

    # Prevent unregistering built-in presets
    built_in = ["article", "presentation", "ulaval", "modeleau", "marimo", "latex"]
    if name in built_in:
        raise ValueError(f"Cannot unregister built-in preset '{name}'.")

    del _PRESET_REGISTRY[name]


def get_preset(mode: str | Preset) -> Preset:
    """
    Get a preset by mode name.

    Args:
        mode: The mode name ('article', 'presentation', or any registered preset name),
            or a Preset object (which will be returned as-is).

    Returns:
        The Preset object.

    Raises:
        ValueError: If the mode is not recognized.
    """
    # If a Preset object is passed, return it directly
    if isinstance(mode, Preset):
        return mode

    if mode not in _PRESET_REGISTRY:
        raise ValueError(
            f"Unknown preset '{mode}'. Available presets: {list(_PRESET_REGISTRY.keys())}"
        )
    return _PRESET_REGISTRY[mode]


def list_presets() -> list[str]:
    """
    List all available preset names.

    Returns:
        List of preset names.
    """
    return list(_PRESET_REGISTRY.keys())


def load_preset_from_file(file_path: str | Path) -> Preset:
    """
    Load a preset from a YAML file and register it.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The loaded Preset object.

    Raises:
        FileNotFoundError: If the file is not found.
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    from sane_figs.core.yaml_parser import load_preset_from_yaml

    preset = load_preset_from_yaml(file_path)
    register_preset(preset)
    return preset


def load_presets_from_file(file_path: str | Path) -> list[Preset]:
    """
    Load multiple presets from a YAML file and register them.

    Args:
        file_path: Path to the YAML file.

    Returns:
        List of loaded Preset objects.

    Raises:
        FileNotFoundError: If the file is not found.
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    from sane_figs.core.yaml_parser import load_presets_from_yaml

    presets = load_presets_from_yaml(file_path)
    for preset in presets:
        register_preset(preset)
    return presets


def load_config() -> None:
    """
    Load all presets and colorways from discovered configuration files.

    This function searches for configuration files in standard locations
    and loads all presets and colorways found.
    """
    from sane_figs.core.config_discovery import (
        load_all_discovered_colorways,
        load_all_discovered_presets,
    )
    from sane_figs.styling.colorways import register_colorway

    # Load presets
    presets = load_all_discovered_presets()
    for preset in presets:
        try:
            register_preset(preset)
        except ValueError:
            # Skip if already registered
            pass

    # Load colorways
    colorways = load_all_discovered_colorways()
    for colorway in colorways:
        try:
            register_colorway(colorway)
        except ValueError:
            # Skip if already registered
            pass


# Default legend configuration applied to all built-in presets
_DEFAULT_LEGEND_CONFIG = LegendConfig(position="inside_upper_right")


# Helper function to create built-in presets using the new architecture
def _create_builtin_preset(
    name: str,
    mode_name: str,
    figure_size: tuple[float, float],
    dpi: int,
    font_family: str,
    font_sizes: dict[str, float],
    line_width: float,
    marker_size: float,
    colorway: "Colorway | None" = None,
    screen_dpi: int | None = None,
) -> Preset:
    """Create a built-in preset with consistent styling."""
    from sane_figs.styling.colorways import DEFAULT_COLORWAY

    effective_colorway = colorway if colorway is not None else DEFAULT_COLORWAY

    return Preset(
        name=name,
        mode=mode_name,
        figure_size=figure_size,
        dpi=dpi,
        screen_dpi=screen_dpi,
        font_family=font_family,
        font_size=font_sizes,
        line_width=line_width,
        marker_size=marker_size,
        plot_style=PlotStyle(),
        colorway=effective_colorway,
        watermark=None,
        title_config=TitleConfig(alignment="center"),
        legend_config=_DEFAULT_LEGEND_CONFIG,
        axis_title_spacing=AxisTitleSpacingConfig(),
    )


# Built-in presets
# These are registered when the module is imported

# Article Mode Preset
# Optimized for print publication at single-column journal width.
_ARTICLE_PRESET = _create_builtin_preset(
    name="article",
    mode_name="article",
    figure_size=(3.5, 2.625),  # Standard single-column journal width, 4:3 aspect
    dpi=300,  # Print quality
    font_family="sans-serif",
    font_sizes={
        "title": 9.0,
        "label": 8.0,
        "legend": 7.0,
        "tick": 7.0,
        "annotation": 7.0,
    },
    line_width=1.0,
    marker_size=4.0,
    colorway=DEFAULT_COLORWAY,
    screen_dpi=100,
)

# Presentation Mode Preset
# Optimized for figures on 16:9 widescreen slides.
_PRESENTATION_PRESET = _create_builtin_preset(
    name="presentation",
    mode_name="presentation",
    figure_size=(10.0, 5.6),  # ~75% of 16:9 slide area
    dpi=300,  # High quality for export
    font_family="sans-serif",
    font_sizes={
        "title": 24.0,
        "label": 20.0,
        "legend": 18.0,
        "tick": 18.0,
        "annotation": 18.0,
    },
    line_width=2.5,
    marker_size=9.0,
    colorway=VIBRANT_COLORWAY,
    screen_dpi=100,
)

# ULaval Preset
# Consistent with Université Laval brand identity
_ULAVAL_PRESET = _create_builtin_preset(
    name="ulaval",
    mode_name="ulaval",
    figure_size=(6.5, 4.0),
    dpi=300,
    font_family="Overpass",
    font_sizes={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.5,
    marker_size=6.0,
    colorway=ULAVAL_COLORWAY,
    screen_dpi=100,
)

# ModelEAU Preset
# Consistent with ModelEAU brand identity
_MODELEAU_PRESET = _create_builtin_preset(
    name="modeleau",
    mode_name="modeleau",
    figure_size=(6.5, 4.0),
    dpi=300,
    font_family="sans-serif",
    font_sizes={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.5,
    marker_size=6.0,
    colorway=MODELEAU_COLORWAY,
    screen_dpi=100,
)

# Marimo Preset
# Consistent with Marimo notebook aesthetics
_MARIMO_PRESET = _create_builtin_preset(
    name="marimo",
    mode_name="marimo",
    figure_size=(6.5, 4.0),
    dpi=100,  # Screen resolution
    font_family="Inter, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif",
    font_sizes={
        "title": 14.0,
        "label": 12.0,
        "legend": 11.0,
        "tick": 11.0,
        "annotation": 11.0,
    },
    line_width=2.0,
    marker_size=8.0,
    colorway=MARIMO_COLORWAY,
    screen_dpi=100,
)

# LaTeX Preset
# Consistent with LaTeX typesetting (using Computer Modern)
_LATEX_PRESET = _create_builtin_preset(
    name="latex",
    mode_name="latex",
    figure_size=(5.5, 3.5),  # Typical LaTeX document figure width
    dpi=300,
    font_family="serif",  # Matplotlib adapter will handle this as 'cm'
    font_sizes={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.0,
    marker_size=5.0,
    colorway=DEFAULT_COLORWAY,
    screen_dpi=100,
)

# Register built-in presets
register_preset(_ARTICLE_PRESET)
register_preset(_PRESENTATION_PRESET)
register_preset(_ULAVAL_PRESET)
register_preset(_MODELEAU_PRESET)
register_preset(_MARIMO_PRESET)
register_preset(_LATEX_PRESET)

# Export for backward compatibility
ARTICLE_PRESET = _ARTICLE_PRESET
PRESENTATION_PRESET = _PRESENTATION_PRESET
ULAVAL_PRESET = _ULAVAL_PRESET
MODELEAU_PRESET = _MODELEAU_PRESET
MARIMO_PRESET = _MARIMO_PRESET
LATEX_PRESET = _LATEX_PRESET
