"""Styling module for sane-figs."""

from sane_figs.styling.colorways import (
    Colorway,
    COLORBLIND_SAFE_COLORWAY,
    DEFAULT_COLORWAY,
    NATURE_COLORWAY,
    PASTEL_COLORWAY,
    VIBRANT_COLORWAY,
    get_colorway,
    list_colorways,
    register_colorway,
)
from sane_figs.styling.watermarks import (
    WatermarkConfig,
    create_image_watermark,
    create_text_watermark,
)
from sane_figs.styling.layout import (
    TitleConfig,
    LegendConfig,
    AxisTitleSpacingConfig,
)

__all__ = [
    "Colorway",
    "DEFAULT_COLORWAY",
    "NATURE_COLORWAY",
    "VIBRANT_COLORWAY",
    "PASTEL_COLORWAY",
    "COLORBLIND_SAFE_COLORWAY",
    "get_colorway",
    "list_colorways",
    "register_colorway",
    "WatermarkConfig",
    "create_text_watermark",
    "create_image_watermark",
    "TitleConfig",
    "LegendConfig",
    "AxisTitleSpacingConfig",
]
