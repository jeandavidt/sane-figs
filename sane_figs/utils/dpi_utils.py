"""DPI utility functions for sane-figs.

Provides helpers for computing consistent scaling factors across
HTML-based (Altair, Plotly) and image-based (Matplotlib) renderers.

Design principle:
- HTML/screen rendering uses ``screen_dpi`` for *all* scaling (dimensions,
  fonts, line widths, markers).  This keeps proportions identical to the
  Matplotlib output at the same screen DPI.
- Image/print export multiplies the screen rendering by
  ``print_dpi / screen_dpi`` so that the resulting raster has the correct
  pixel dimensions and element sizes for the target print DPI.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset

# Fallback when detection fails -- CSS reference pixel is defined as 1/96 in.
_DEFAULT_SCREEN_DPI = 96


def detect_screen_dpi() -> int:
    """Attempt to detect the screen DPI of the current display.

    Tries several platform-specific methods and falls back to 96 (the CSS
    reference-pixel density) when detection is not possible.

    Returns:
        Detected (or fallback) screen DPI as an integer.
    """
    # 1. Try tkinter (most cross-platform)
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        dpi = root.winfo_fpixels("1i")
        root.destroy()
        return int(dpi)
    except Exception:
        pass

    # 2. Platform-specific fallbacks
    if sys.platform == "darwin":
        # macOS Quartz coordinate system uses 72 points per inch,
        # but Retina displays double the physical pixels.  We report
        # the logical DPI (72) since CSS pixels map to logical points.
        return 72

    if sys.platform == "win32":
        try:
            import ctypes

            hdc = ctypes.windll.user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            ctypes.windll.user32.ReleaseDC(0, hdc)
            return int(dpi)
        except Exception:
            return _DEFAULT_SCREEN_DPI

    # 3. Linux / other: default
    return _DEFAULT_SCREEN_DPI


def get_screen_scale(preset: "Preset") -> float:
    """Return the scale factor that converts typographic points to CSS pixels.

    The factor is ``screen_dpi / 72`` because 1 pt = 1/72 in and the screen
    has ``screen_dpi`` px/in.

    Args:
        preset: A Preset whose ``screen_dpi`` (or ``get_display_dpi()``) is
            used as the reference screen resolution.

    Returns:
        Scaling multiplier (dimensionless).  Multiply a point-based size by
        this value to get CSS-pixel sizes for HTML rendering.
    """
    return preset.get_display_dpi() / 72.0


def get_export_scale_factor(preset: "Preset") -> float:
    """Return the uniform multiplier to go from screen rendering to print.

    When an HTML-first library (Altair / Plotly) configures its theme for
    ``screen_dpi``, exporting to a raster image at ``print_dpi`` requires
    scaling every dimension by ``print_dpi / screen_dpi``.

    Args:
        preset: A Preset with both ``dpi`` (print) and ``screen_dpi``
            (display) configured.

    Returns:
        Scale factor (>= 1 in typical use).  For presets where
        ``dpi == screen_dpi`` (e.g. ``marimo``), this returns 1.0.
    """
    screen_dpi = preset.get_display_dpi()
    return preset.dpi / screen_dpi


def get_export_dimensions(preset: "Preset") -> tuple[int, int]:
    """Return the target raster-image dimensions in pixels for print export.

    These match what Matplotlib produces with ``savefig.dpi = preset.dpi``
    and ``figure.figsize = preset.figure_size``.

    Args:
        preset: A Preset with ``figure_size`` (inches) and ``dpi``.

    Returns:
        ``(width_px, height_px)`` tuple.
    """
    return (
        int(preset.figure_size[0] * preset.dpi),
        int(preset.figure_size[1] * preset.dpi),
    )


def get_screen_dimensions(preset: "Preset") -> tuple[int, int]:
    """Return the HTML/screen canvas dimensions in CSS pixels.

    Args:
        preset: A Preset with ``figure_size`` (inches) and ``screen_dpi``.

    Returns:
        ``(width_px, height_px)`` tuple.
    """
    screen_dpi = preset.get_display_dpi()
    return (
        int(preset.figure_size[0] * screen_dpi),
        int(preset.figure_size[1] * screen_dpi),
    )
