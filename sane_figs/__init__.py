"""
Sane-Figs: Publication-ready figures for Matplotlib, Seaborn, Plotly, and Altair.

This package automatically applies publication-ready styling to figures generated
with popular Python visualization libraries.
"""

from pathlib import Path

__version__ = "0.1.0"
__author__ = "Jean-David T."
__license__ = "MIT"

from sane_figs.core.presets import (
    ARTICLE_PRESET,
    PRESENTATION_PRESET,
    Preset,
    get_preset,
    list_presets,
    load_config,
    load_preset_from_file,
    load_presets_from_file,
    register_preset,
    unregister_preset,
)
from sane_figs.styling.colorways import (
    Colorway,
    DEFAULT_COLORWAY,
    NATURE_COLORWAY,
    VIBRANT_COLORWAY,
    PASTEL_COLORWAY,
    COLORBLIND_SAFE_COLORWAY,
)
from sane_figs.styling.watermarks import (
    WatermarkConfig,
    create_image_watermark,
    create_text_watermark,
)

# Import main functions after they are defined
from sane_figs.core.discovery import DiscoveryService
from sane_figs.core.registry import StyleRegistry

# Global instances
_discovery_service = DiscoveryService()
_style_registry = StyleRegistry()


def setup(
    mode: str = "article",
    libraries: list[str] | None = None,
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
) -> None:
    """
    Apply publication-ready styling globally to all specified libraries.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        libraries: List of library names to apply styling to. If None, applies
            to all available libraries.
        colorway: Colorway name or Colorway object to use. If None, uses the
            default colorway for the mode.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig object to override the preset's legend
            positioning. If None, the preset's legend_config is used.

    Example:
        >>> import sane_figs
        >>> sane_figs.setup(mode='article')
        >>> # All subsequent plots will have publication-ready styling
    """
    from sane_figs.core.setup import apply_global_setup

    apply_global_setup(
        mode=mode,
        libraries=libraries,
        colorway=colorway,
        watermark=watermark,
        legend_config=legend_config,
        discovery_service=_discovery_service,
        style_registry=_style_registry,
    )


def reset() -> None:
    """
    Reset all styling to default values for all libraries.

    This function removes any publication-ready styling that was applied
    via setup() and restores the default library settings.

    Example:
        >>> import sane_figs
        >>> sane_figs.setup(mode='article')
        >>> # Create styled figures...
        >>> sane_figs.reset()
        >>> # Subsequent figures will use default styling
    """
    from sane_figs.core.setup import reset_global_setup

    reset_global_setup(
        discovery_service=_discovery_service,
        style_registry=_style_registry,
    )


def publication_style(
    mode: str = "article",
    libraries: list[str] | None = None,
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
):
    """
    Context manager for applying publication-ready styling to a block of code.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        libraries: List of library names to apply styling to. If None, applies
            to all available libraries.
        colorway: Colorway name or Colorway object to use. If None, uses the
            default colorway for the mode.
        watermark: Watermark text, WatermarkConfig object, or None.

    Example:
        >>> import sane_figs
        >>> import matplotlib.pyplot as plt
        >>> with sane_figs.publication_style(mode='article'):
        ...     plt.plot([1, 2, 3], [1, 4, 9])
        ...     plt.savefig('figure.png')
    """
    from sane_figs.core.setup import PublicationStyleContext

    return PublicationStyleContext(
        mode=mode,
        libraries=libraries,
        colorway=colorway,
        watermark=watermark,
        legend_config=legend_config,
        discovery_service=_discovery_service,
        style_registry=_style_registry,
    )


def list_presets() -> list[str]:
    """
    List all available preset names.

    Returns:
        List of preset names.

    Example:
        >>> import sane_figs
        >>> sane_figs.list_presets()
        ['article', 'presentation', 'my-custom-preset']
    """
    from sane_figs.core.presets import list_presets as _list_presets

    return _list_presets()


def get_preset(name: str) -> Preset:
    """
    Get a preset by name.

    Args:
        name: The name of the preset.

    Returns:
        The Preset object.

    Raises:
        ValueError: If the preset name is not found.

    Example:
        >>> import sane_figs
        >>> preset = sane_figs.get_preset('article')
    """
    from sane_figs.core.presets import get_preset as _get_preset

    return _get_preset(name)


def register_preset(preset: Preset) -> None:
    """
    Register a custom preset.

    Args:
        preset: The Preset object to register.

    Raises:
        ValueError: If a preset with the same name already exists.

    Example:
        >>> import sane_figs
        >>> custom = sane_figs.Preset(
        ...     name='my-preset',
        ...     mode='custom',
        ...     figure_size=(8.0, 6.0),
        ...     dpi=300,
        ...     font_family='sans-serif',
        ...     font_size={'title': 16.0, 'label': 14.0},
        ... )
        >>> sane_figs.register_preset(custom)
    """
    from sane_figs.core.presets import register_preset as _register_preset

    _register_preset(preset)


def unregister_preset(name: str) -> None:
    """
    Unregister a preset by name.

    Args:
        name: The name of the preset to unregister.

    Raises:
        ValueError: If the preset is not found or is a built-in preset.

    Example:
        >>> import sane_figs
        >>> sane_figs.unregister_preset('my-preset')
    """
    from sane_figs.core.presets import unregister_preset as _unregister_preset

    _unregister_preset(name)


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

    Example:
        >>> import sane_figs
        >>> preset = sane_figs.load_preset_from_file('my_preset.yaml')
    """
    from sane_figs.core.presets import load_preset_from_file as _load_preset_from_file

    return _load_preset_from_file(file_path)


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

    Example:
        >>> import sane_figs
        >>> presets = sane_figs.load_presets_from_file('presets.yaml')
    """
    from sane_figs.core.presets import load_presets_from_file as _load_presets_from_file

    return _load_presets_from_file(file_path)


def load_config() -> None:
    """
    Load all presets and colorways from discovered configuration files.

    This function searches for configuration files in standard locations
    and loads all presets and colorways found.

    Standard locations (in order of precedence):
    1. ./sane_figs.yaml (project root)
    2. ./.sane_figs/presets.yaml (project directory)
    3. ~/.config/sane-figs/presets.yaml (user config)
    4. ~/.sane_figs.yaml (user home)

    Example:
        >>> import sane_figs
        >>> sane_figs.load_config()
    """
    from sane_figs.core.presets import load_config as _load_config

    _load_config()


def create_sample_preset_yaml(file_path: str | Path) -> Path:
    """
    Create a sample YAML preset template file that users can customize.

    This function generates a well-documented YAML file with all available
    preset options, including comments explaining each setting. Users can
    modify this file and load it back using load_preset_from_file().

    Args:
        file_path: Path where the sample YAML file will be saved.

    Returns:
        The Path to the created file.

    Example:
        >>> import sane_figs
        >>> path = sane_figs.create_sample_preset_yaml("my_preset.yaml")
        >>> # User edits my_preset.yaml...
        >>> preset = sane_figs.load_preset_from_file("my_preset.yaml")
    """
    from sane_figs.core.yaml_parser import create_sample_preset_yaml as _create_sample_preset_yaml

    return _create_sample_preset_yaml(file_path)


def create_sample_colorway_yaml(file_path: str | Path) -> Path:
    """
    Create a sample YAML colorway template file that users can customize.

    This function generates a well-documented YAML file with all available
    colorway options, including comments explaining each setting. Users can
    modify this file and load it back using load_colorway_from_yaml().

    Args:
        file_path: Path where the sample YAML file will be saved.

    Returns:
        The Path to the created file.

    Example:
        >>> import sane_figs
        >>> path = sane_figs.create_sample_colorway_yaml("my_colorway.yaml")
        >>> # User edits my_colorway.yaml...
        >>> colorway = sane_figs.load_colorway_from_yaml("my_colorway.yaml")
    """
    from sane_figs.core.yaml_parser import (
        create_sample_colorway_yaml as _create_sample_colorway_yaml,
    )

    return _create_sample_colorway_yaml(file_path)


def load_colorway_from_yaml(file_path: str | Path) -> "Colorway":
    """
    Load a single colorway from a YAML file and register it.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The loaded Colorway object.

    Raises:
        FileNotFoundError: If the file is not found.
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.

    Example:
        >>> import sane_figs
        >>> colorway = sane_figs.load_colorway_from_yaml('my_colorway.yaml')
    """
    from sane_figs.core.yaml_parser import load_colorway_from_yaml as _load_colorway_from_yaml

    return _load_colorway_from_yaml(file_path)


def load_colorways_from_yaml(file_path: str | Path) -> list["Colorway"]:
    """
    Load multiple colorways from a YAML file and register them.

    Args:
        file_path: Path to the YAML file.

    Returns:
        List of loaded Colorway objects.

    Raises:
        FileNotFoundError: If the file is not found.
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.

    Example:
        >>> import sane_figs
        >>> colorways = sane_figs.load_colorways_from_yaml('colorways.yaml')
    """
    from sane_figs.core.yaml_parser import load_colorways_from_yaml as _load_colorways_from_yaml

    return _load_colorways_from_yaml(file_path)


def list_colorways() -> list[str]:
    """
    List all available colorways.

    Returns:
        List of colorway names.

    Example:
        >>> import sane_figs
        >>> sane_figs.list_colorways()
        ['default', 'nature', 'vibrant', 'pastel', 'colorblind-safe']
    """
    from sane_figs.styling.colorways import list_colorways

    return list_colorways()


def get_colorway(name: str) -> Colorway:
    """
    Get a colorway by name.

    Args:
        name: The name of the colorway.

    Returns:
        The Colorway object.

    Raises:
        ValueError: If the colorway name is not found.

    Example:
        >>> import sane_figs
        >>> colorway = sane_figs.get_colorway('nature')
    """
    from sane_figs.styling.colorways import get_colorway

    return get_colorway(name)


def register_colorway(colorway: Colorway) -> None:
    """
    Register a custom colorway.

    Args:
        colorway: The Colorway object to register.

    Example:
        >>> import sane_figs
        >>> custom = sane_figs.Colorway(
        ...     name='my-lab',
        ...     categorical=['#FF0000', '#00FF00', '#0000FF'],
        ...     sequential=[...],
        ...     diverging=[...],
        ...     qualitative=[...]
        ... )
        >>> sane_figs.register_colorway(custom)
    """
    from sane_figs.styling.colorways import register_colorway

    register_colorway(colorway)


# Per-library setup functions
def setup_matplotlib(
    mode: str = "article",
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
) -> None:
    """
    Apply publication-ready styling to Matplotlib.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        colorway: Colorway name or Colorway object to use.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override preset legend positioning.
    """
    setup(mode=mode, libraries=["matplotlib"], colorway=colorway, watermark=watermark, legend_config=legend_config)


def setup_seaborn(
    mode: str = "article",
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
) -> None:
    """
    Apply publication-ready styling to Seaborn.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        colorway: Colorway name or Colorway object to use.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override preset legend positioning.
    """
    setup(mode=mode, libraries=["seaborn"], colorway=colorway, watermark=watermark, legend_config=legend_config)


def setup_plotly(
    mode: str = "article",
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
) -> None:
    """
    Apply publication-ready styling to Plotly.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        colorway: Colorway name or Colorway object to use.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override preset legend positioning.
    """
    setup(mode=mode, libraries=["plotly"], colorway=colorway, watermark=watermark, legend_config=legend_config)


def setup_altair(
    mode: str = "article",
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
) -> None:
    """
    Apply publication-ready styling to Altair.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        colorway: Colorway name or Colorway object to use.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override preset legend positioning.
    """
    setup(mode=mode, libraries=["altair"], colorway=colorway, watermark=watermark, legend_config=legend_config)


__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Core classes
    "Preset",
    "Colorway",
    "WatermarkConfig",
    # Presets
    "ARTICLE_PRESET",
    "PRESENTATION_PRESET",
    # Colorways
    "DEFAULT_COLORWAY",
    "NATURE_COLORWAY",
    "VIBRANT_COLORWAY",
    "PASTEL_COLORWAY",
    "COLORBLIND_SAFE_COLORWAY",
    # Main functions
    "setup",
    "reset",
    "publication_style",
    "list_colorways",
    "get_colorway",
    "register_colorway",
    "create_text_watermark",
    "create_image_watermark",
    # Preset functions
    "list_presets",
    "get_preset",
    "register_preset",
    "unregister_preset",
    "load_preset_from_file",
    "load_presets_from_file",
    "load_config",
    "create_sample_preset_yaml",
    "create_sample_colorway_yaml",
    # Colorway loading functions
    "load_colorway_from_yaml",
    "load_colorways_from_yaml",
    # Per-library functions
    "setup_matplotlib",
    "setup_seaborn",
    "setup_plotly",
    "setup_altair",
]
