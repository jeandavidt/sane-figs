"""Discovery service for detecting installed plotting libraries."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.adapters.base import BaseAdapter


@dataclass
class LibraryInfo:
    """
    Information about an installed plotting library.

    Attributes:
        name: Name of the library.
        version: Version string of the installed library.
        available: Whether the library is available for use.
    """

    name: str
    version: str | None
    available: bool


class DiscoveryService:
    """
    Service for discovering installed plotting libraries and their versions.

    This service detects which plotting libraries are installed and provides
    access to their corresponding adapters.
    """

    # Mapping of library names to their import names and version attributes
    _LIBRARY_INFO = {
        "matplotlib": {
            "import_name": "matplotlib",
            "version_attr": "__version__",
            "adapter_module": "sane_figs.adapters.matplotlib",
            "adapter_class": "MatplotlibAdapter",
        },
        "seaborn": {
            "import_name": "seaborn",
            "version_attr": "__version__",
            "adapter_module": "sane_figs.adapters.seaborn",
            "adapter_class": "SeabornAdapter",
        },
        "plotly": {
            "import_name": "plotly",
            "version_attr": "__version__",
            "adapter_module": "sane_figs.adapters.plotly",
            "adapter_class": "PlotlyAdapter",
        },
        "altair": {
            "import_name": "altair",
            "version_attr": "__version__",
            "adapter_module": "sane_figs.adapters.altair",
            "adapter_class": "AltairAdapter",
        },
    }

    def __init__(self) -> None:
        """Initialize the discovery service."""
        self._cache: dict[str, LibraryInfo] = {}
        self._adapter_cache: dict[str, "BaseAdapter | None"] = {}

    def detect_installed_libraries(self) -> dict[str, LibraryInfo]:
        """
        Detect all installed plotting libraries.

        Returns:
            Dictionary mapping library names to LibraryInfo objects.
        """
        result = {}
        for name in self._LIBRARY_INFO:
            info = self.get_library_info(name)
            result[name] = info
        return result

    def get_library_info(self, library_name: str) -> LibraryInfo:
        """
        Get information about a specific library.

        Args:
            library_name: Name of the library (e.g., 'matplotlib').

        Returns:
            LibraryInfo object with library information.

        Raises:
            ValueError: If the library name is not recognized.
        """
        if library_name not in self._LIBRARY_INFO:
            raise ValueError(
                f"Unknown library '{library_name}'. "
                f"Available libraries: {list(self._LIBRARY_INFO.keys())}"
            )

        # Return cached result if available
        if library_name in self._cache:
            return self._cache[library_name]

        # Detect library
        lib_info = self._LIBRARY_INFO[library_name]
        version = self._get_library_version(
            lib_info["import_name"], lib_info["version_attr"]
        )
        available = version is not None

        info = LibraryInfo(name=library_name, version=version, available=available)
        self._cache[library_name] = info
        return info

    def get_library_version(self, library_name: str) -> str | None:
        """
        Get the version of a specific library.

        Args:
            library_name: Name of the library.

        Returns:
            Version string or None if the library is not installed.
        """
        info = self.get_library_info(library_name)
        return info.version

    def get_adapter(self, library_name: str) -> "BaseAdapter | None":
        """
        Get the adapter for a specific library.

        Args:
            library_name: Name of the library.

        Returns:
            BaseAdapter instance or None if the library is not available.
        """
        # Return cached adapter if available
        if library_name in self._adapter_cache:
            return self._adapter_cache[library_name]

        # Check if library is available
        info = self.get_library_info(library_name)
        if not info.available:
            self._adapter_cache[library_name] = None
            return None

        # Import and instantiate the adapter
        lib_info = self._LIBRARY_INFO[library_name]
        try:
            module = __import__(
                lib_info["adapter_module"], fromlist=[lib_info["adapter_class"]]
            )
            adapter_class = getattr(module, lib_info["adapter_class"])
            adapter = adapter_class()
            self._adapter_cache[library_name] = adapter
            return adapter
        except Exception:
            self._adapter_cache[library_name] = None
            return None

    def get_all_available_adapters(self) -> list["BaseAdapter"]:
        """
        Get all available adapters for installed libraries.

        Returns:
            List of BaseAdapter instances.
        """
        adapters = []
        for library_name in self._LIBRARY_INFO:
            adapter = self.get_adapter(library_name)
            if adapter is not None:
                adapters.append(adapter)
        return adapters

    def get_available_libraries(self) -> list[str]:
        """
        Get list of available library names.

        Returns:
            List of library names that are installed and available.
        """
        available = []
        for library_name in self._LIBRARY_INFO:
            info = self.get_library_info(library_name)
            if info.available:
                available.append(library_name)
        return available

    def _get_library_version(self, import_name: str, version_attr: str) -> str | None:
        """
        Get the version of a library by importing it.

        Args:
            import_name: Name of the module to import.
            version_attr: Attribute name containing the version.

        Returns:
            Version string or None if the library is not installed.
        """
        try:
            module = __import__(import_name)
            version = getattr(module, version_attr, None)
            return str(version) if version is not None else None
        except Exception:
            return None

    def clear_cache(self) -> None:
        """Clear the cache of library information and adapters."""
        self._cache.clear()
        self._adapter_cache.clear()
