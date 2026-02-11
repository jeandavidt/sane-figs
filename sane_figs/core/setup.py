"""Setup functions for applying publication-ready styling."""

from contextlib import contextmanager
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from sane_figs.core.discovery import DiscoveryService
    from sane_figs.core.presets import Preset
    from sane_figs.core.registry import StyleRegistry
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig


def apply_global_setup(
    mode: str = "article",
    libraries: list[str] | None = None,
    colorway: Union[str, "Colorway", None] = None,
    watermark: Union[str, "WatermarkConfig", None] = None,
    discovery_service: Union["DiscoveryService", None] = None,
    style_registry: Union["StyleRegistry", None] = None,
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
        discovery_service: DiscoveryService instance for detecting libraries.
        style_registry: StyleRegistry instance for tracking styles.
    """
    from sane_figs.core.presets import get_preset
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.watermarks import create_text_watermark

    # Get the preset
    preset = get_preset(mode)

    # Handle colorway
    if colorway is None:
        # Use default colorway for the mode
        from sane_figs.styling.colorways import (
            DEFAULT_COLORWAY,
            VIBRANT_COLORWAY,
        )

        if preset.colorway is not None:
            preset_colorway = preset.colorway
        else:
            preset_colorway = VIBRANT_COLORWAY if mode == "presentation" else DEFAULT_COLORWAY
    elif isinstance(colorway, str):
        preset_colorway = get_colorway(colorway)
    else:
        preset_colorway = colorway

    # Update preset with colorway
    preset.colorway = preset_colorway

    # Handle watermark
    if watermark is not None:
        if isinstance(watermark, str):
            preset_watermark = create_text_watermark(watermark)
        else:
            preset_watermark = watermark
        preset.watermark = preset_watermark

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


def reset_global_setup(
    libraries: list[str] | None = None,
    discovery_service: Union["DiscoveryService", None] = None,
    style_registry: Union["StyleRegistry", None] = None,
) -> None:
    """
    Reset all styling to original settings.

    Args:
        libraries: List of library names to reset. If None, resets all libraries.
        discovery_service: DiscoveryService instance for detecting libraries.
        style_registry: StyleRegistry instance for tracking styles.
    """
    if libraries is None:
        adapter_names = style_registry.list_active_adapters()
    else:
        adapter_names = libraries

    for adapter_name in adapter_names:
        adapter = discovery_service.get_adapter(adapter_name)
        if adapter is not None:
            adapter.reset_style()
            style_registry.clear_adapter(adapter_name)


class PublicationStyleContext:
    """
    Context manager for applying publication-ready styling to a block of code.

    The styling is applied when entering the context and reset when exiting.
    """

    def __init__(
        self,
        mode: str = "article",
        libraries: list[str] | None = None,
        colorway: Union[str, "Colorway", None] = None,
        watermark: Union[str, "WatermarkConfig", None] = None,
        discovery_service: Union["DiscoveryService", None] = None,
        style_registry: Union["StyleRegistry", None] = None,
    ) -> None:
        """
        Initialize the context manager.

        Args:
            mode: The preset mode to use ('article' or 'presentation').
            libraries: List of library names to apply styling to.
            colorway: Colorway name or Colorway object to use.
            watermark: Watermark text, WatermarkConfig object, or None.
            discovery_service: DiscoveryService instance.
            style_registry: StyleRegistry instance.
        """
        self.mode = mode
        self.libraries = libraries
        self.colorway = colorway
        self.watermark = watermark
        self.discovery_service = discovery_service
        self.style_registry = style_registry
        self._active_libraries: list[str] = []

    def __enter__(self) -> "PublicationStyleContext":
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

            # Get and apply preset
            from sane_figs.core.presets import get_preset
            from sane_figs.styling.colorways import get_colorway
            from sane_figs.styling.watermarks import create_text_watermark

            preset = get_preset(self.mode)

            # Handle colorway
            if self.colorway is None:
                from sane_figs.styling.colorways import (
                    DEFAULT_COLORWAY,
                    VIBRANT_COLORWAY,
                )

                if preset.colorway is not None:
                     preset_colorway = preset.colorway
                else:
                     preset_colorway = (
                        VIBRANT_COLORWAY
                        if self.mode == "presentation"
                        else DEFAULT_COLORWAY
                    )
            elif isinstance(self.colorway, str):
                preset_colorway = get_colorway(self.colorway)
            else:
                preset_colorway = self.colorway

            preset.colorway = preset_colorway

            # Handle watermark
            if self.watermark is not None:
                if isinstance(self.watermark, str):
                    preset_watermark = create_text_watermark(self.watermark)
                else:
                    preset_watermark = self.watermark
                preset.watermark = preset_watermark

            # Apply the preset
            adapter.apply_style(preset)

            # Register in registry
            self.style_registry.register_preset(adapter.library_name, preset)
            if preset.colorway is not None:
                self.style_registry.register_colorway(adapter.library_name, preset.colorway)
            if preset.watermark is not None:
                self.style_registry.register_watermark(
                    adapter.library_name, preset.watermark
                )

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
