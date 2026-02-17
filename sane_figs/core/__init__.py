"""Core module for sane-figs."""

from sane_figs.core.discovery import DiscoveryService, LibraryInfo
from sane_figs.core.modes import Mode, get_mode, list_modes, register_mode, unregister_mode
from sane_figs.core.presets import (
    ARTICLE_PRESET,
    PRESENTATION_PRESET,
    Preset,
    get_preset,
    list_presets,
    register_preset,
    unregister_preset,
)
from sane_figs.core.registry import StyleRegistry
from sane_figs.core.styles import Style, get_style, list_styles, register_style, unregister_style

__all__ = [
    # Discovery
    "DiscoveryService",
    "LibraryInfo",
    # Mode
    "Mode",
    "get_mode",
    "list_modes",
    "register_mode",
    "unregister_mode",
    # Style
    "Style",
    "get_style",
    "list_styles",
    "register_style",
    "unregister_style",
    # Preset
    "Preset",
    "get_preset",
    "list_presets",
    "register_preset",
    "unregister_preset",
    "ARTICLE_PRESET",
    "PRESENTATION_PRESET",
    # Registry
    "StyleRegistry",
]
