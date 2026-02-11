"""Validation utilities for sane-figs."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig


@dataclass
class ValidationError:
    """
    A validation error or warning.

    Attributes:
        field: The field that failed validation.
        message: Human-readable error message.
        severity: 'error' or 'warning'.
    """

    field: str
    message: str
    severity: str = "error"


def validate_preset(preset: "Preset") -> list[ValidationError]:
    """
    Validate a Preset object.

    Args:
        preset: The Preset object to validate.

    Returns:
        List of validation errors. Empty list if valid.
    """
    errors: list[ValidationError] = []

    # Validate name
    if not preset.name or not isinstance(preset.name, str):
        errors.append(
            ValidationError(
                field="name", message="Preset name must be a non-empty string."
            )
        )

    # Validate mode
    if not preset.mode or not isinstance(preset.mode, str):
        errors.append(
            ValidationError(field="mode", message="Preset mode must be a non-empty string.")
        )

    # Validate figure_size
    if not isinstance(preset.figure_size, (tuple, list)) or len(preset.figure_size) != 2:
        errors.append(
            ValidationError(
                field="figure_size",
                message="Figure size must be a tuple or list of two numbers.",
            )
        )
    else:
        width, height = preset.figure_size
        if not isinstance(width, (int, float)) or width <= 0:
            errors.append(
                ValidationError(
                    field="figure_size.width",
                    message=f"Figure width must be a positive number, got {width}.",
                )
            )
        if not isinstance(height, (int, float)) or height <= 0:
            errors.append(
                ValidationError(
                    field="figure_size.height",
                    message=f"Figure height must be a positive number, got {height}.",
                )
            )

    # Validate dpi
    if not isinstance(preset.dpi, int) or preset.dpi <= 0:
        errors.append(
            ValidationError(
                field="dpi", message=f"DPI must be a positive integer, got {preset.dpi}."
            )
        )

    # Validate font_family
    if not preset.font_family or not isinstance(preset.font_family, str):
        errors.append(
            ValidationError(
                field="font_family",
                message="Font family must be a non-empty string.",
            )
        )

    # Validate font_size
    if not isinstance(preset.font_size, dict):
        errors.append(
            ValidationError(
                field="font_size", message="Font sizes must be a dictionary."
            )
        )
    else:
        valid_font_keys = {"title", "label", "legend", "tick", "annotation"}
        for key, value in preset.font_size.items():
            if key not in valid_font_keys:
                errors.append(
                    ValidationError(
                        field=f"font_size.{key}",
                        message=f"Unknown font size key '{key}'. Valid keys: {valid_font_keys}",
                        severity="warning",
                    )
                )
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(
                    ValidationError(
                        field=f"font_size.{key}",
                        message=f"Font size for '{key}' must be a positive number, got {value}.",
                    )
                )

    # Validate line_width
    if not isinstance(preset.line_width, (int, float)) or preset.line_width <= 0:
        errors.append(
            ValidationError(
                field="line_width",
                message=f"Line width must be a positive number, got {preset.line_width}.",
            )
        )

    # Validate marker_size
    if not isinstance(preset.marker_size, (int, float)) or preset.marker_size <= 0:
        errors.append(
            ValidationError(
                field="marker_size",
                message=f"Marker size must be a positive number, got {preset.marker_size}.",
            )
        )

    # Validate colorway if present
    if preset.colorway is not None:
        colorway_errors = validate_colorway(preset.colorway)
        errors.extend(
            [
                ValidationError(
                    field=f"colorway.{e.field}", message=e.message, severity=e.severity
                )
                for e in colorway_errors
            ]
        )

    # Validate watermark if present
    if preset.watermark is not None:
        watermark_errors = validate_watermark(preset.watermark)
        errors.extend(
            [
                ValidationError(
                    field=f"watermark.{e.field}", message=e.message, severity=e.severity
                )
                for e in watermark_errors
            ]
        )

    return errors


def validate_colorway(colorway: "Colorway") -> list[ValidationError]:
    """
    Validate a Colorway object.

    Args:
        colorway: The Colorway object to validate.

    Returns:
        List of validation errors. Empty list if valid.
    """
    errors: list[ValidationError] = []

    # Validate name
    if not colorway.name or not isinstance(colorway.name, str):
        errors.append(
            ValidationError(
                field="name", message="Colorway name must be a non-empty string."
            )
        )

    # Validate description
    if not colorway.description or not isinstance(colorway.description, str):
        errors.append(
            ValidationError(
                field="description",
                message="Colorway description must be a non-empty string.",
            )
        )

    # Validate color lists
    color_types = {
        "categorical": colorway.categorical,
        "sequential": colorway.sequential,
        "diverging": colorway.diverging,
        "qualitative": colorway.qualitative,
    }

    for color_type, colors in color_types.items():
        if not isinstance(colors, list):
            errors.append(
                ValidationError(
                    field=color_type,
                    message=f"{color_type} colors must be a list.",
                )
            )
        else:
            for i, color in enumerate(colors):
                if not isinstance(color, str):
                    errors.append(
                        ValidationError(
                            field=f"{color_type}[{i}]",
                            message=f"Color at index {i} must be a string, got {type(color).__name__}.",
                        )
                    )
                elif not _is_valid_hex_color(color):
                    errors.append(
                        ValidationError(
                            field=f"{color_type}[{i}]",
                            message=f"Invalid hex color '{color}'. Expected format: #RRGGBB or #RRGGBBAA.",
                        )
                    )

    return errors


def validate_watermark(watermark: "WatermarkConfig") -> list[ValidationError]:
    """
    Validate a WatermarkConfig object.

    Args:
        watermark: The WatermarkConfig object to validate.

    Returns:
        List of validation errors. Empty list if valid.
    """
    errors: list[ValidationError] = []

    # Validate that either text or image_path is provided
    if watermark.image_path is None and watermark.text is None:
        errors.append(
            ValidationError(
                field="watermark",
                message="Either image_path or text must be provided for watermark.",
            )
        )

    # Validate position
    valid_positions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "center",
    ]
    if watermark.position not in valid_positions:
        errors.append(
            ValidationError(
                field="position",
                message=f"Invalid position '{watermark.position}'. Valid positions: {valid_positions}",
            )
        )

    # Validate opacity
    if not isinstance(watermark.opacity, (int, float)) or not (0.0 <= watermark.opacity <= 1.0):
        errors.append(
            ValidationError(
                field="opacity",
                message=f"Opacity must be between 0.0 and 1.0, got {watermark.opacity}.",
            )
        )

    # Validate scale
    if not isinstance(watermark.scale, (int, float)) or not (0.0 <= watermark.scale <= 1.0):
        errors.append(
            ValidationError(
                field="scale",
                message=f"Scale must be between 0.0 and 1.0, got {watermark.scale}.",
            )
        )

    # Validate margin
    if not isinstance(watermark.margin, (tuple, list)) or len(watermark.margin) != 2:
        errors.append(
            ValidationError(
                field="margin",
                message="Margin must be a tuple or list of two numbers.",
            )
        )
    else:
        margin_x, margin_y = watermark.margin
        if not isinstance(margin_x, (int, float)) or not (0.0 <= margin_x <= 1.0):
            errors.append(
                ValidationError(
                    field="margin.x",
                    message=f"Margin X must be between 0.0 and 1.0, got {margin_x}.",
                )
            )
        if not isinstance(margin_y, (int, float)) or not (0.0 <= margin_y <= 1.0):
            errors.append(
                ValidationError(
                    field="margin.y",
                    message=f"Margin Y must be between 0.0 and 1.0, got {margin_y}.",
                )
            )

    # Validate font settings
    if not isinstance(watermark.font_size, (int, float)) or watermark.font_size <= 0:
        errors.append(
            ValidationError(
                field="font_size",
                message=f"Font size must be a positive number, got {watermark.font_size}.",
            )
        )

    if not isinstance(watermark.font_family, str):
        errors.append(
            ValidationError(
                field="font_family",
                message=f"Font family must be a string, got {type(watermark.font_family).__name__}.",
            )
        )

    if not isinstance(watermark.font_weight, str):
        errors.append(
            ValidationError(
                field="font_weight",
                message=f"Font weight must be a string, got {type(watermark.font_weight).__name__}.",
            )
        )

    if not isinstance(watermark.font_color, str):
        errors.append(
            ValidationError(
                field="font_color",
                message=f"Font color must be a string, got {type(watermark.font_color).__name__}.",
            )
        )
    elif not _is_valid_hex_color(watermark.font_color):
        errors.append(
            ValidationError(
                field="font_color",
                message=f"Invalid hex color '{watermark.font_color}'. Expected format: #RRGGBB or #RRGGBBAA.",
            )
        )

    return errors


def _is_valid_hex_color(color: str) -> bool:
    """
    Check if a string is a valid hex color.

    Args:
        color: The color string to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not color.startswith("#"):
        return False

    hex_part = color[1:]
    # Allow 6-digit (#RRGGBB) or 8-digit (#RRGGBBAA) hex colors
    if len(hex_part) not in (6, 8):
        return False

    try:
        int(hex_part, 16)
        return True
    except ValueError:
        return False
