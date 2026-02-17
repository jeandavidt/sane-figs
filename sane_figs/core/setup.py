"""Setup functions for applying publication-ready styling.

This module provides the main API for configuring sane-figs:
- setup(): Apply styling globally or as a context manager
- save_settings(): Save current configuration to YAML
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Union

from sane_figs.styling.layout import PlotStyle

if TYPE_CHECKING:
    from sane_figs.core.discovery import DiscoveryService
    from sane_figs.core.modes import Mode
    from sane_figs.core.presets import Preset
    from sane_figs.core.registry import StyleRegistry
    from sane_figs.core.styles import Style
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import LegendConfig


class SetupContext:
    """
    Context manager for applying publication-ready styling to a block of code.

    The styling is applied when entering the context and reset when exiting.
    This class is returned by setup() when used as a context manager.

    Example:
        >>> import sane_figs
        >>> with sane_figs.setup(mode='article'):
        ...     # Figures created here will have article styling
        ...     plt.plot([1, 2, 3], [1, 4, 9])
        ...     plt.savefig('figure.png')
        >>> # Styling is automatically reset here
    """

    def __init__(
        self,
        preset: "Preset",
        libraries: list[str] | None,
        discovery_service: "DiscoveryService",
        style_registry: "StyleRegistry",
    ) -> None:
        """
        Initialize the context manager.

        Args:
            preset: The preset to apply.
            libraries: List of library names to apply styling to.
            discovery_service: DiscoveryService instance.
            style_registry: StyleRegistry instance.
        """
        self.preset = preset
        self.libraries = libraries
        self.discovery_service = discovery_service
        self.style_registry = style_registry
        self._active_libraries: list[str] = []

    def __enter__(self) -> "SetupContext":
        """
        Enter the context and apply publication styling.

        Returns:
            The context manager instance.
        """
        # Get available adapters
        if self.libraries is None:
            adapters = self.discovery_service.get_all_available_adapters()
        else:
            adapters = []
            for lib_name in self.libraries:
                adapter = self.discovery_service.get_adapter(lib_name)
                if adapter is not None:
                    adapters.append(adapter)

        # Track which libraries we're styling
        self._active_libraries = [adapter.library_name for adapter in adapters]

        # Apply styling to each adapter
        for adapter in adapters:
            # Save original settings
            original_settings = _get_adapter_original_settings(adapter)
            self.style_registry.save_original_settings(adapter.library_name, original_settings)

            # Apply the preset
            adapter.apply_style(self.preset)

            # Register in registry
            self.style_registry.register_preset(adapter.library_name, self.preset)
            if self.preset.colorway is not None:
                self.style_registry.register_colorway(adapter.library_name, self.preset.colorway)
            if self.preset.watermark is not None:
                self.style_registry.register_watermark(adapter.library_name, self.preset.watermark)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context and reset styling.

        Args:
            exc_type: Exception type if an exception was raised.
            exc_val: Exception value if an exception was raised.
            exc_tb: Exception traceback if an exception was raised.
        """
        # Reset styling for all libraries we styled
        for adapter_name in self._active_libraries:
            adapter = self.discovery_service.get_adapter(adapter_name)
            if adapter is not None:
                adapter.reset_style()
                self.style_registry.clear_adapter(adapter_name)


def setup(
    filepath: str | Path | None = None,
    mode: str | "Mode" = "article",
    style: str | "Style" = "default",
    font_family: str | None = None,
    figsize: tuple[float, float] | list[float] | None = None,
    libraries: list[str] | None = None,
    colorway: str | "Colorway" | None = None,
    watermark: str | "WatermarkConfig" | None = None,
    legend_config: "LegendConfig | None" = None,
    discovery_service: "DiscoveryService | None" = None,
    style_registry: "StyleRegistry | None" = None,
    _as_context_manager: bool = False,
) -> "SetupContext | None":
    """
    Apply publication-ready styling globally or return a context manager.

    This is the main entry point for configuring sane-figs. It can be used
    in two ways:

    1. Global setup (affects all subsequent plots):
       >>> import sane_figs
       >>> sane_figs.setup(mode='article')
       >>> # All plots from here will use article styling

    2. Context manager (styling only applies within the block):
       >>> with sane_figs.setup(mode='article'):
       ...     # Only plots in this block use article styling
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
        discovery_service: DiscoveryService instance for detecting libraries.
            If None, uses the global discovery service.
        style_registry: StyleRegistry instance for tracking styles.
            If None, uses the global style registry.
        _as_context_manager: Internal flag. When True, returns a context
            manager instead of applying immediately.

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
    from sane_figs.core.discovery import DiscoveryService
    from sane_figs.core.modes import Mode, get_mode
    from sane_figs.core.presets import Preset, get_preset
    from sane_figs.core.registry import StyleRegistry
    from sane_figs.core.styles import Style, get_style
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.watermarks import create_text_watermark

    # Get or create discovery service and style registry
    if discovery_service is None:
        discovery_service = DiscoveryService()
    if style_registry is None:
        style_registry = StyleRegistry()

    # Build preset from parameters
    preset: Preset

    if filepath is not None:
        # Load preset from file
        preset = _load_preset_from_file(filepath)

        # Apply overrides
        if font_family is not None:
            preset.font_family = font_family
        if figsize is not None:
            preset.figure_size = tuple(figsize)
        if colorway is not None:
            if isinstance(colorway, str):
                preset.colorway = get_colorway(colorway)
            else:
                preset.colorway = colorway
        if watermark is not None:
            if isinstance(watermark, str):
                preset.watermark = create_text_watermark(watermark)
            else:
                preset.watermark = watermark
        if legend_config is not None:
            preset.legend_config = legend_config

    else:
        # Build preset from mode and style.
        # Try mode+style first (new API). Fall back to preset-name lookup only
        # when the value passed as `mode` is not a registered mode — this
        # preserves backward compatibility with callers that pass a preset name
        # such as `setup(mode="ulaval")`.
        try:
            mode_obj = get_mode(mode) if isinstance(mode, str) else mode
            style_obj = get_style(style) if isinstance(style, str) else style

            # Create preset from mode and style
            preset = Preset.from_mode_and_style(
                name=f"{mode_obj.name}-{style_obj.name}",
                mode=mode_obj,
                style=style_obj,
            )
        except ValueError:
            # Not a valid mode/style — try as preset name (backward compatibility)
            try:
                existing_preset = get_preset(mode)
                preset = _copy_preset(existing_preset)
            except ValueError:
                raise ValueError(
                    f"'{mode}' is not a recognised mode, style, or preset name."
                )

        # Apply overrides
        if font_family is not None:
            preset.font_family = font_family
        if figsize is not None:
            preset.figure_size = tuple(figsize)
        if colorway is not None:
            if isinstance(colorway, str):
                preset.colorway = get_colorway(colorway)
            else:
                preset.colorway = colorway
        if watermark is not None:
            if isinstance(watermark, str):
                preset.watermark = create_text_watermark(watermark)
            else:
                preset.watermark = watermark
        if legend_config is not None:
            preset.legend_config = legend_config

    # If context manager mode, return the context
    if _as_context_manager:
        return SetupContext(
            preset=preset,
            libraries=libraries,
            discovery_service=discovery_service,
            style_registry=style_registry,
        )

    # Otherwise, apply immediately (global setup)
    _apply_preset(
        preset=preset,
        libraries=libraries,
        discovery_service=discovery_service,
        style_registry=style_registry,
    )
    return None


def _apply_preset(
    preset: "Preset",
    libraries: list[str] | None,
    discovery_service: "DiscoveryService",
    style_registry: "StyleRegistry",
) -> None:
    """
    Apply a preset to the specified libraries.

    Args:
        preset: The preset to apply.
        libraries: List of library names, or None for all.
        discovery_service: DiscoveryService instance.
        style_registry: StyleRegistry instance.
    """
    # Get available adapters
    if libraries is None:
        adapters = discovery_service.get_all_available_adapters()
    else:
        adapters = []
        for lib_name in libraries:
            adapter = discovery_service.get_adapter(lib_name)
            if adapter is not None:
                adapters.append(adapter)

    # Apply styling to each adapter
    for adapter in adapters:
        # Save original settings
        original_settings = _get_adapter_original_settings(adapter)
        style_registry.save_original_settings(adapter.library_name, original_settings)

        # Apply the preset
        adapter.apply_style(preset)

        # Register in registry
        style_registry.register_preset(adapter.library_name, preset)
        if preset.colorway is not None:
            style_registry.register_colorway(adapter.library_name, preset.colorway)
        if preset.watermark is not None:
            style_registry.register_watermark(adapter.library_name, preset.watermark)


def _copy_preset(preset: "Preset") -> "Preset":
    """Create a copy of a preset."""
    from dataclasses import replace

    # Copy plot_style to avoid shared state
    new_plot_style = PlotStyle(
        background_color=preset.plot_style.background_color,
        grid_visible=preset.plot_style.grid_visible,
        grid_color=preset.plot_style.grid_color,
        grid_opacity=preset.plot_style.grid_opacity,
        grid_width=preset.plot_style.grid_width,
        axis_line_color=preset.plot_style.axis_line_color,
        axis_line_width=preset.plot_style.axis_line_width,
        show_top_spine=preset.plot_style.show_top_spine,
        show_right_spine=preset.plot_style.show_right_spine,
        tick_direction=preset.plot_style.tick_direction,
        tick_length=preset.plot_style.tick_length,
        tick_color=preset.plot_style.tick_color,
        title_weight=preset.plot_style.title_weight,
        legend_frame_opacity=preset.plot_style.legend_frame_opacity,
        legend_edge_color=preset.plot_style.legend_edge_color,
    )

    return replace(
        preset,
        font_size=dict(preset.font_size),
        plot_style=new_plot_style,
    )


def _load_preset_from_file(filepath: str | Path) -> "Preset":
    """Load a preset from a YAML file."""
    from sane_figs.core.yaml_parser import load_preset_from_yaml

    return load_preset_from_yaml(filepath)


def save_settings(
    filepath: str | Path,
    preset: "Preset | None" = None,
    mode: str | "Mode" = "article",
    style: str | "Style" = "default",
    font_family: str | None = None,
    figsize: tuple[float, float] | list[float] | None = None,
    colorway: str | "Colorway" | None = None,
    watermark: str | "WatermarkConfig" | None = None,
) -> Path:
    """
    Save current or configured settings to a YAML file.

    This function saves the configuration in the new YAML format with
    separate mode and style sections for better readability and
    maintainability.

    Args:
        filepath: Path where the YAML file will be saved.
        preset: An existing Preset to save. If provided, other parameters
            are ignored.
        mode: The mode to use if not providing a preset.
        style: The style to use if not providing a preset.
        font_family: Font family override.
        figsize: Figure size override.
        colorway: Colorway override.
        watermark: Watermark override.

    Returns:
        The Path to the created file.

    Raises:
        ValueError: If the configuration is invalid.

    Examples:
        # Save current settings
        >>> sane_figs.save_settings("my_config.yaml")

        # Save with specific mode and style
        >>> sane_figs.save_settings(
        ...     "article_config.yaml",
        ...     mode="article",
        ...     style="nature",
        ... )

        # Save an existing preset
        >>> preset = sane_figs.get_preset("article")
        >>> sane_figs.save_settings("article_copy.yaml", preset=preset)
    """
    import yaml
    from sane_figs.core.modes import get_mode
    from sane_figs.core.presets import Preset
    from sane_figs.core.styles import get_style
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.watermarks import create_text_watermark

    path = Path(filepath)

    # Build preset if not provided
    if preset is None:
        mode_obj = get_mode(mode)
        style_obj = get_style(style)

        preset = Preset.from_mode_and_style(
            name=f"{mode_obj.name}-{style_obj.name}",
            mode=mode_obj,
            style=style_obj,
        )

        # Apply overrides
        if font_family is not None:
            preset.font_family = font_family
        if figsize is not None:
            preset.figure_size = tuple(figsize)
        if colorway is not None:
            if isinstance(colorway, str):
                preset.colorway = get_colorway(colorway)
            else:
                preset.colorway = colorway
        if watermark is not None:
            if isinstance(watermark, str):
                preset.watermark = create_text_watermark(watermark)
            else:
                preset.watermark = watermark

    # Convert to YAML-compatible dict
    data = preset.to_yaml_dict()

    # Write YAML file
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    return path


def reset_global_setup(
    libraries: list[str] | None = None,
    discovery_service: "DiscoveryService | None" = None,
    style_registry: "StyleRegistry | None" = None,
) -> None:
    """
    Reset all styling to original settings.

    Args:
        libraries: List of library names to reset. If None, resets all libraries.
        discovery_service: DiscoveryService instance for detecting libraries.
        style_registry: StyleRegistry instance for tracking styles.
    """
    from sane_figs.core.discovery import DiscoveryService
    from sane_figs.core.registry import StyleRegistry

    if discovery_service is None:
        discovery_service = DiscoveryService()
    if style_registry is None:
        style_registry = StyleRegistry()

    if libraries is None:
        adapter_names = style_registry.list_active_adapters()
    else:
        adapter_names = libraries

    for adapter_name in adapter_names:
        adapter = discovery_service.get_adapter(adapter_name)
        if adapter is not None:
            adapter.reset_style()
            style_registry.clear_adapter(adapter_name)


def apply_global_setup(
    mode: str = "article",
    libraries: list[str] | None = None,
    colorway: Union[str, "Colorway", None] = None,
    watermark: Union[str, "WatermarkConfig", None] = None,
    legend_config=None,
    discovery_service: Union["DiscoveryService", None] = None,
    style_registry: Union["StyleRegistry", None] = None,
) -> None:
    """
    Apply publication-ready styling globally to all specified libraries.

    .. deprecated::
        Use setup() instead. This function is kept for backward compatibility.

    Args:
        mode: The preset mode to use ('article' or 'presentation').
        libraries: List of library names to apply styling to. If None, applies
            to all available libraries.
        colorway: Colorway name or Colorway object to use. If None, uses the
            default colorway for the mode.
        watermark: Watermark text, WatermarkConfig object, or None.
        legend_config: LegendConfig to override the preset's legend positioning.
        discovery_service: DiscoveryService instance for detecting libraries.
        style_registry: StyleRegistry instance for tracking styles.
    """
    setup(
        mode=mode,
        libraries=libraries,
        colorway=colorway,
        watermark=watermark,
        legend_config=legend_config,
        discovery_service=discovery_service,
        style_registry=style_registry,
    )


class PublicationStyleContext:
    """
    Context manager for applying publication-ready styling (legacy).

    .. deprecated::
        Use setup() as a context manager instead. This class is kept for
        backward compatibility.
    """

    def __init__(
        self,
        mode: str = "article",
        libraries: list[str] | None = None,
        colorway: Union[str, "Colorway", None] = None,
        watermark: Union[str, "WatermarkConfig", None] = None,
        legend_config=None,
        discovery_service: Union["DiscoveryService", None] = None,
        style_registry: Union["StyleRegistry", None] = None,
    ) -> None:
        """Initialize the context manager."""
        self.mode = mode
        self.libraries = libraries
        self.colorway = colorway
        self.watermark = watermark
        self.legend_config = legend_config

        from sane_figs.core.discovery import DiscoveryService
        from sane_figs.core.registry import StyleRegistry

        self.discovery_service = discovery_service or DiscoveryService()
        self.style_registry = style_registry or StyleRegistry()
        self._active_libraries: list[str] = []

    def __enter__(self) -> "PublicationStyleContext":
        """Enter the context and apply publication styling."""
        # Use the new setup function internally
        self._context = setup(
            mode=self.mode,
            libraries=self.libraries,
            colorway=self.colorway,
            watermark=self.watermark,
            legend_config=self.legend_config,
            discovery_service=self.discovery_service,
            style_registry=self.style_registry,
            _as_context_manager=True,
        )
        self._context.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context and reset styling."""
        self._context.__exit__(exc_type, exc_val, exc_tb)


def _get_adapter_original_settings(adapter) -> dict:
    """
    Get the original settings from an adapter.

    Args:
        adapter: The adapter instance.

    Returns:
        Dictionary of original settings.
    """
    # Try to get original settings from the adapter
    if hasattr(adapter, "get_original_settings"):
        original = adapter.get_original_settings()
        if original is not None:
            return original

    # Return empty dict if no original settings available
    return {}
