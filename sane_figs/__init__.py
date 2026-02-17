"""
Sane-Figs: Publication-ready figures for Matplotlib, Seaborn, Plotly, and Altair.

This package automatically applies publication-ready styling to figures generated
with popular Python visualization libraries.

New API (Mode/Style separation):
    >>> import sane_figs
    >>>
    >>> # Global setup with mode and style
    >>> sane_figs.setup(mode='article', style='default')
    >>>
    >>> # Load from YAML file
    >>> sane_figs.setup(filepath='custom.yaml')
    >>>
    >>> # Context manager usage
    >>> with sane_figs.setup(mode='presentation'):
    ...     plt.plot([1, 2, 3])
    >>>
    >>> # Save settings
    >>> sane_figs.save_settings('my_config.yaml')
"""

from pathlib import Path
from typing import TYPE_CHECKING

try:
    from importlib.metadata import version as _pkg_version
    __version__ = _pkg_version("sane-figs")
except Exception:
    __version__ = "dev"  # fallback for editable/dev installs
__author__ = "Jean-David T."
__license__ = "MIT"

# Core classes (new architecture)
from sane_figs.core.modes import Mode, get_mode, list_modes
from sane_figs.core.styles import Style, get_style, list_styles
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
from sane_figs.styling.layout import PlotStyle
from sane_figs.styling.watermarks import (
    WatermarkConfig,
    create_image_watermark,
    create_text_watermark,
)
from sane_figs.utils.dpi_utils import (
    detect_screen_dpi,
    get_screen_scale,
    get_export_scale_factor,
    get_export_dimensions,
    get_screen_dimensions,
)

# Import main functions after they are defined
from sane_figs.core.discovery import DiscoveryService
from sane_figs.core.registry import StyleRegistry
from sane_figs.core.setup import SetupContext, save_settings

# Global instances
_discovery_service = DiscoveryService()
_style_registry = StyleRegistry()


def setup(
    filepath: str | Path | None = None,
    mode: str | Mode = "article",
    style: str | Style = "default",
    font_family: str | None = None,
    figsize: tuple[float, float] | list[float] | None = None,
    libraries: list[str] | None = None,
    colorway: str | Colorway | None = None,
    watermark: str | WatermarkConfig | None = None,
    legend_config=None,
):
    """
    Apply publication-ready styling globally or return a context manager.

    This is the main entry point for configuring sane-figs. It can be used
    in two ways:

    1. **Global setup** (affects all subsequent plots):
       >>> import sane_figs
       >>> sane_figs.setup(mode='article', style='default')
       >>> # All plots from here will use article sizing with default styling

    2. **Context manager** (styling only applies within the block):
       >>> with sane_figs.setup(mode='article', style='nature'):
       ...     # Only plots in this block use article + nature styling
       ...     plt.plot([1, 2, 3], [1, 4, 9])

    Args:
        filepath: Path to a YAML configuration file. If provided, other
            parameters are applied on top of the loaded configuration.
        mode: The mode to use for sizing ('article', 'presentation') or a
            Mode object. Can also be a Preset name for backward compatibility.
        style: The style to use for visual appearance ('default') or a
            Style object.
        font_family: Font family to use (e.g., 'sans-serif', 'serif').
            Overrides the style's font family.
        figsize: Figure size as (width, height) in inches. Overrides the
            mode's figure size.
        libraries: List of library names to apply styling to. If None,
            applies to all available libraries.
        colorway: Colorway name or Colorway object to use. If None, uses
            the default colorway for the mode.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override the preset's legend
            positioning.

    Returns:
        None when used for global setup, or a SetupContext when used as
        a context manager.

    Raises:
        ValueError: If the mode or style is not recognized.
        FileNotFoundError: If the filepath is not found.

    Examples:
        # Global setup with mode and style
        >>> sane_figs.setup(mode='article', style='nature')

        # Load from YAML file
        >>> sane_figs.setup(filepath='my_config.yaml')

        # Override specific settings
        >>> sane_figs.setup(mode='article', font_family='Arial', figsize=[10, 6])

        # Context manager usage
        >>> with sane_figs.setup(mode='presentation'):
        ...     plt.plot([1, 2, 3])

        # Style specific libraries only
        >>> sane_figs.setup(mode='article', libraries=['matplotlib', 'seaborn'])
    """
    from sane_figs.core.setup import setup as _setup

    return _setup(
        filepath=filepath,
        mode=mode,
        style=style,
        font_family=font_family,
        figsize=figsize,
        libraries=libraries,
        colorway=colorway,
        watermark=watermark,
        legend_config=legend_config,
        discovery_service=_discovery_service,
        style_registry=_style_registry,
    )


# Make setup work as a context manager by adding __enter__ when called
# The actual context manager logic is in SetupContext returned by _setup
class _SetupWrapper:
    """Wrapper that allows setup() to work as both function and context manager."""

    def __init__(self, setup_func):
        self._setup_func = setup_func

    def __call__(self, *args, **kwargs):
        result = self._setup_func(*args, **kwargs)
        # If result is None (global setup), return None
        # If result is a SetupContext, return it for context manager usage
        return result

    def __enter__(self):
        # This shouldn't be called directly on the wrapper
        raise RuntimeError(
            "Use 'with sane_figs.setup(...)' instead of 'with sane_figs.setup'"
        )

    def __exit__(self, *args):
        pass


# Wrap setup to support context manager syntax
# We need to handle the case where setup() is called in a 'with' statement
# The setup function itself returns either None or a SetupContext
# To support 'with sane_figs.setup(...)', we need a special wrapper

_original_setup = setup


def _context_manager_setup(*args, **kwargs):
    """Internal setup that always returns a context manager."""
    from sane_figs.core.setup import setup as _setup

    result = _setup(
        *args,
        **kwargs,
        discovery_service=_discovery_service,
        style_registry=_style_registry,
        _as_context_manager=True,
    )
    return result


# Monkey-patch setup to handle context manager usage
def _patched_setup(*args, **kwargs):
    """Setup function that works both globally and as context manager."""
    # Check if we're being called in a context manager context
    # by looking at the caller's frame
    import inspect

    # Always call the real setup
    result = _original_setup(*args, **kwargs)

    # If the result is None (applied immediately), we need to return
    # something that can work as a dummy context manager
    if result is None:
        # Return a dummy context manager for cases where user writes:
        # with sane_figs.setup(...) when it's actually global
        class _DummyContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return _DummyContext()

    return result


# Replace the setup function with the patched version
setup = _patched_setup


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
    Context manager for applying publication-ready styling (legacy).

    .. deprecated::
        Use setup() as a context manager instead:
        >>> with sane_figs.setup(mode='article'):
        ...     # your code

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        libraries: List of library names to apply styling to.
        colorway: Colorway name or Colorway object to use.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override preset legend positioning.
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


# YAML helper functions
def create_sample_preset_yaml(file_path: str | Path) -> Path:
    """
    Create a sample YAML preset template file that users can customize.

    This function generates a well-documented YAML file with the new format
    supporting mode and style sections. Users can modify this file and load
    it back using load_preset_from_file().

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

    Args:
        file_path: Path where the sample YAML file will be saved.

    Returns:
        The Path to the created file.
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
    """
    from sane_figs.core.yaml_parser import load_colorways_from_yaml as _load_colorways_from_yaml

    return _load_colorways_from_yaml(file_path)


def list_colorways() -> list[str]:
    """
    List all available colorways.

    Returns:
        List of colorway names.
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
    """
    from sane_figs.styling.colorways import get_colorway

    return get_colorway(name)


def register_colorway(colorway: Colorway) -> None:
    """
    Register a custom colorway.

    Args:
        colorway: The Colorway object to register.
    """
    from sane_figs.styling.colorways import register_colorway

    register_colorway(colorway)


__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Core classes (new architecture)
    "Mode",
    "Style",
    "Preset",
    # Core functions (new architecture)
    "get_mode",
    "list_modes",
    "get_style",
    "list_styles",
    # Legacy preset exports
    "ARTICLE_PRESET",
    "PRESENTATION_PRESET",
    # Colorways
    "Colorway",
    "DEFAULT_COLORWAY",
    "NATURE_COLORWAY",
    "VIBRANT_COLORWAY",
    "PASTEL_COLORWAY",
    "COLORBLIND_SAFE_COLORWAY",
    # Styling classes
    "PlotStyle",
    "WatermarkConfig",
    # Main functions
    "setup",
    "reset",
    "publication_style",
    "save_settings",
    "SetupContext",
    # Preset functions
    "get_preset",
    "list_presets",
    "register_preset",
    "unregister_preset",
    "load_preset_from_file",
    "load_presets_from_file",
    "load_config",
    # Colorway functions
    "list_colorways",
    "get_colorway",
    "register_colorway",
    "load_colorway_from_yaml",
    "load_colorways_from_yaml",
    # Watermark functions
    "create_text_watermark",
    "create_image_watermark",
    # YAML helper functions
    "create_sample_preset_yaml",
    "create_sample_colorway_yaml",
    # Per-library functions
    "setup_matplotlib",
    "setup_seaborn",
    "setup_plotly",
    "setup_altair",
    # DPI utilities
    "detect_screen_dpi",
    "get_screen_scale",
    "get_export_scale_factor",
    "get_export_dimensions",
    "get_screen_dimensions",
]
