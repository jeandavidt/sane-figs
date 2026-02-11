"""Style registry for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.adapters.base import BaseAdapter
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig


class StyleRegistry:
    """
    Registry for managing applied styles and their original settings.

    This registry keeps track of which styles have been applied to which
    adapters, allowing for proper reset functionality.
    """

    def __init__(self) -> None:
        """Initialize the style registry."""
        self._active_presets: dict[str, "Preset"] = {}
        self._active_colorways: dict[str, "Colorway"] = {}
        self._active_watermarks: dict[str, "WatermarkConfig"] = {}
        self._original_settings: dict[str, dict] = {}

    def register_preset(self, adapter_name: str, preset: "Preset") -> None:
        """
        Register a preset as active for an adapter.

        Args:
            adapter_name: Name of the adapter (e.g., 'matplotlib').
            preset: The Preset object that was applied.
        """
        self._active_presets[adapter_name] = preset

    def register_colorway(self, adapter_name: str, colorway: "Colorway") -> None:
        """
        Register a colorway as active for an adapter.

        Args:
            adapter_name: Name of the adapter.
            colorway: The Colorway object that was applied.
        """
        self._active_colorways[adapter_name] = colorway

    def register_watermark(self, adapter_name: str, watermark: "WatermarkConfig") -> None:
        """
        Register a watermark as active for an adapter.

        Args:
            adapter_name: Name of the adapter.
            watermark: The WatermarkConfig object that was applied.
        """
        self._active_watermarks[adapter_name] = watermark

    def save_original_settings(self, adapter_name: str, settings: dict) -> None:
        """
        Save the original settings for an adapter.

        Args:
            adapter_name: Name of the adapter.
            settings: Dictionary of original settings.
        """
        self._original_settings[adapter_name] = settings

    def get_original_settings(self, adapter_name: str) -> dict | None:
        """
        Get the original settings for an adapter.

        Args:
            adapter_name: Name of the adapter.

        Returns:
            Dictionary of original settings or None if not saved.
        """
        return self._original_settings.get(adapter_name)

    def get_active_preset(self, adapter_name: str) -> "Preset | None":
        """
        Get the active preset for an adapter.

        Args:
            adapter_name: Name of the adapter.

        Returns:
            The active Preset object or None if no preset is active.
        """
        return self._active_presets.get(adapter_name)

    def get_active_colorway(self, adapter_name: str) -> "Colorway | None":
        """
        Get the active colorway for an adapter.

        Args:
            adapter_name: Name of the adapter.

        Returns:
            The active Colorway object or None if no colorway is active.
        """
        return self._active_colorways.get(adapter_name)

    def get_active_watermark(self, adapter_name: str) -> "WatermarkConfig | None":
        """
        Get the active watermark for an adapter.

        Args:
            adapter_name: Name of the adapter.

        Returns:
            The active WatermarkConfig object or None if no watermark is active.
        """
        return self._active_watermarks.get(adapter_name)

    def clear_adapter(self, adapter_name: str) -> None:
        """
        Clear all registry entries for an adapter.

        Args:
            adapter_name: Name of the adapter.
        """
        self._active_presets.pop(adapter_name, None)
        self._active_colorways.pop(adapter_name, None)
        self._active_watermarks.pop(adapter_name, None)
        self._original_settings.pop(adapter_name, None)

    def clear_all(self) -> None:
        """Clear all registry entries."""
        self._active_presets.clear()
        self._active_colorways.clear()
        self._active_watermarks.clear()
        self._original_settings.clear()

    def has_active_style(self, adapter_name: str) -> bool:
        """
        Check if an adapter has an active style.

        Args:
            adapter_name: Name of the adapter.

        Returns:
            True if the adapter has an active style, False otherwise.
        """
        return adapter_name in self._active_presets

    def list_active_adapters(self) -> list[str]:
        """
        List all adapters with active styles.

        Returns:
            List of adapter names with active styles.
        """
        return list(self._active_presets.keys())
