"""Base adapter class for sane-figs."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig


class BaseAdapter(ABC):
    """
    Abstract base class for all library adapters.

    Each adapter implements the common interface for applying publication-ready
    styling to a specific plotting library.
    """

    def __init__(self, library_name: str) -> None:
        """
        Initialize the adapter.

        Args:
            library_name: Name of the plotting library (e.g., 'matplotlib').
        """
        self.library_name = library_name
        self._version: str | None = None
        self._original_settings: dict | None = None

    @abstractmethod
    def apply_style(self, preset: "Preset") -> None:
        """
        Apply publication-ready styling to the library.

        Args:
            preset: The Preset object containing styling configuration.
        """
        pass

    @abstractmethod
    def reset_style(self) -> None:
        """
        Reset the library styling to its original state.

        This restores the settings that were in place before apply_style was called.
        """
        pass

    @abstractmethod
    def get_version(self) -> str | None:
        """
        Get the version of the installed library.

        Returns:
            Version string or None if the library is not installed.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the library is available for use.

        Returns:
            True if the library is installed and can be used, False otherwise.
        """
        pass

    @abstractmethod
    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to the library.

        Args:
            colorway: The Colorway object to apply.
        """
        pass

    @abstractmethod
    def add_watermark(self, config: "WatermarkConfig") -> None:
        """
        Add a watermark to figures created by the library.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        pass

    def get_version_tuple(self) -> tuple[int, int, int] | None:
        """
        Get the version as a tuple of integers.

        Returns:
            Tuple of (major, minor, patch) or None if version is not available.
        """
        from sane_figs.utils.version_utils import parse_version

        version = self.get_version()
        if version is None:
            return None
        return parse_version(version)

    def save_original_settings(self, settings: dict) -> None:
        """
        Save the original settings before applying new styles.

        Args:
            settings: Dictionary of original settings.
        """
        self._original_settings = settings

    def get_original_settings(self) -> dict | None:
        """
        Get the original settings.

        Returns:
            Dictionary of original settings or None if not saved.
        """
        return self._original_settings
