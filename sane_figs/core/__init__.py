"""Core module for sane-figs."""

from sane_figs.core.discovery import DiscoveryService, LibraryInfo
from sane_figs.core.presets import (
    ARTICLE_PRESET,
    PRESENTATION_PRESET,
    Preset,
)
from sane_figs.core.registry import StyleRegistry

__all__ = [
    "DiscoveryService",
    "LibraryInfo",
    "Preset",
    "ARTICLE_PRESET",
    "PRESENTATION_PRESET",
    "StyleRegistry",
]
