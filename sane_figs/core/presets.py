"""Style presets for sane-figs."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig

from sane_figs.styling.colorways import (
    ULAVAL_COLORWAY,
    MODELEAU_COLORWAY,
    MARIMO_COLORWAY,
)


@dataclass
class Preset:
    """
    A preset containing publication-ready styling configuration.

    Attributes:
        name: Name of the preset.
        mode: The mode ('article' or 'presentation').
        figure_size: Figure size as (width, height) in inches.
        dpi: Dots per inch for output.
        font_family: Font family to use.
        font_size: Dictionary of font sizes for different elements.
        line_width: Line width for plots.
        marker_size: Marker size for scatter plots.
        colorway: Colorway to use.
        watermark: Optional watermark configuration.
    """

    name: str
    mode: str
    figure_size: tuple[float, float]
    dpi: int
    font_family: str
    font_size: dict[str, float] = field(default_factory=dict)
    line_width: float = 1.5
    marker_size: float = 6.0
    colorway: "Colorway | None" = None
    watermark: "WatermarkConfig | None" = None


# Preset registry
_PRESET_REGISTRY: dict[str, Preset] = {}


def register_preset(preset: Preset) -> None:
    """
    Register a preset in the registry.

    Args:
        preset: The Preset object to register.

    Raises:
        ValueError: If a preset with the same name already exists.
    """
    if preset.name in _PRESET_REGISTRY:
        raise ValueError(
            f"Preset '{preset.name}' already exists. Use a different name or unregister first."
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
    built_in = ["article", "presentation"]
    if name in built_in:
        raise ValueError(f"Cannot unregister built-in preset '{name}'.")

    del _PRESET_REGISTRY[name]


def get_preset(mode: str) -> Preset:
    """
    Get a preset by mode name.

    Args:
        mode: The mode name ('article', 'presentation', or any registered preset name).

    Returns:
        The Preset object.

    Raises:
        ValueError: If the mode is not recognized.
    """
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
    from sane_figs.core.config_discovery import load_all_discovered_colorways, load_all_discovered_presets
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


# Built-in presets
# These are registered when the module is imported

# Article Mode Preset
# Optimized for print publication at single-column journal width.
# Font sizes are WYSIWYG at the target figure size -- no scaling math needed.
_ARTICLE_PRESET = Preset(
    name="article",
    mode="article",
    figure_size=(3.5, 2.625),  # Standard single-column journal width, 4:3 aspect
    dpi=300,  # Print quality
    font_family="sans-serif",
    font_size={
        "title": 9.0,
        "label": 8.0,
        "legend": 7.0,
        "tick": 7.0,
        "annotation": 7.0,
    },
    line_width=1.0,
    marker_size=4.0,
    colorway=None,  # Will be set to DEFAULT_COLORWAY
    watermark=None,
)

# Presentation Mode Preset
# Optimized for 16:9 widescreen slides.
# 20pt minimum ensures readability from the back of a room.
_PRESENTATION_PRESET = Preset(
    name="presentation",
    mode="presentation",
    figure_size=(13.33, 7.5),  # 16:9 widescreen slide dimensions
    dpi=150,  # Sufficient for screen/projector (~full HD output)
    font_family="sans-serif",
    font_size={
        "title": 28.0,
        "label": 24.0,
        "legend": 20.0,
        "tick": 20.0,
        "annotation": 20.0,
    },
    line_width=3.0,
    marker_size=10.0,
    colorway=None,  # Will be set to VIBRANT_COLORWAY
    watermark=None,
)

# ULaval Preset
# Consistent with Université Laval brand identity
_ULAVAL_PRESET = Preset(
    name="ulaval",
    mode="ulaval",
    figure_size=(6.5, 4.0),
    dpi=300,
    font_family="Overpass",
    font_size={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.5,
    marker_size=6.0,
    colorway=ULAVAL_COLORWAY,
    watermark=None,
)

# ModelEAU Preset
# Consistent with ModelEAU brand identity
_MODELEAU_PRESET = Preset(
    name="modeleau",
    mode="modeleau",
    figure_size=(6.5, 4.0),
    dpi=300,
    font_family="sans-serif",  # Default to sans-serif, using brand colors
    font_size={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.5,
    marker_size=6.0,
    colorway=MODELEAU_COLORWAY,
    watermark=None,
)

# Marimo Preset
# Consistent with Marimo notebook aesthetics
_MARIMO_PRESET = Preset(
    name="marimo",
    mode="marimo",
    figure_size=(6.5, 4.0),
    dpi=100,  # Screen resolution
    font_family="Inter, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif",
    font_size={
        "title": 14.0,
        "label": 12.0,
        "legend": 11.0,
        "tick": 11.0,
        "annotation": 11.0,
    },
    line_width=2.0,
    marker_size=8.0,
    colorway=MARIMO_COLORWAY,
    watermark=None,
)

# LaTeX Preset
# Consistent with LaTeX typesetting (using Computer Modern)
_LATEX_PRESET = Preset(
    name="latex",
    mode="latex",
    figure_size=(5.5, 3.5),  # Typical LaTeX document figure width
    dpi=300,
    font_family="serif",  # Matplotlib adapter will handle this as 'cm'
    font_size={
        "title": 11.0,
        "label": 10.0,
        "legend": 9.0,
        "tick": 9.0,
        "annotation": 9.0,
    },
    line_width=1.0,
    marker_size=5.0,
    colorway=None,  # Default colorway suitable for LaTeX
    watermark=None,
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
