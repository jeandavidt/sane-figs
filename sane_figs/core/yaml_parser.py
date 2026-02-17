"""YAML parser for sane-figs modes, styles, and presets."""

from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from sane_figs.core.validation import (
    ValidationError,
    validate_colorway,
    validate_preset,
    validate_watermark,
)

if TYPE_CHECKING:
    from sane_figs.core.modes import Mode
    from sane_figs.core.presets import Preset
    from sane_figs.core.styles import Style
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig


class YAMLParseError(Exception):
    """Exception raised when YAML parsing fails."""

    pass


class YAMLValidationError(Exception):
    """Exception raised when YAML validation fails."""

    def __init__(self, errors: list[ValidationError]) -> None:
        self.errors = errors
        messages = [f"{e.field}: {e.message}" for e in errors]
        super().__init__("\n".join(messages))


def load_preset_from_yaml(file_path: str | Path) -> "Preset":
    """
    Load a single preset from a YAML file.

    Supports both legacy format and new mode/style format.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The Preset object.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this is a multi-preset file
    if "presets" in data:
        presets = _parse_presets_from_dict(data, path.parent)
        if len(presets) == 0:
            raise YAMLParseError(f"No presets found in file: {file_path}")
        return presets[0]

    # Check if this is the new format with mode/style sections
    if "mode" in data or "style" in data:
        return _parse_preset_from_new_format(data, path.parent)

    # Legacy single preset file
    preset = _parse_preset_from_dict(data, path.parent)
    return preset


def load_presets_from_yaml(file_path: str | Path) -> list["Preset"]:
    """
    Load multiple presets from a YAML file.

    Supports both legacy format and new mode/style format.

    Args:
        file_path: Path to the YAML file.

    Returns:
        List of Preset objects.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this is a multi-preset file
    if "presets" in data:
        return _parse_presets_from_dict(data, path.parent)

    # Single preset file - return as a list
    # Check if this is the new format with mode/style sections
    if "mode" in data or "style" in data:
        return [_parse_preset_from_new_format(data, path.parent)]

    # Legacy format
    return [_parse_preset_from_dict(data, path.parent)]


def load_mode_from_yaml(file_path: str | Path) -> "Mode":
    """
    Load a mode from a YAML file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The Mode object.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this has a mode section
    if "mode" in data:
        return _parse_mode_from_dict(data["mode"])

    # Direct mode definition
    return _parse_mode_from_dict(data)


def load_style_from_yaml(file_path: str | Path) -> "Style":
    """
    Load a style from a YAML file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The Style object.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this has a style section
    if "style" in data:
        return _parse_style_from_dict(data["style"], path.parent)

    # Direct style definition
    return _parse_style_from_dict(data, path.parent)


def load_colorway_from_yaml(file_path: str | Path) -> "Colorway":
    """
    Load a single colorway from a YAML file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        The Colorway object.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this is a multi-colorway file
    if "colorways" in data:
        colorways = _parse_colorways_from_dict(data)
        if len(colorways) == 0:
            raise YAMLParseError(f"No colorways found in file: {file_path}")
        return colorways[0]

    # Single colorway file
    colorway = _parse_colorway_from_dict(data)
    return colorway


def load_colorways_from_yaml(file_path: str | Path) -> list["Colorway"]:
    """
    Load multiple colorways from a YAML file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        List of Colorway objects.

    Raises:
        YAMLParseError: If the YAML file cannot be parsed.
        YAMLValidationError: If the YAML data is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise YAMLParseError(f"YAML file is empty: {file_path}")

    # Check if this is a multi-colorway file
    if "colorways" in data:
        return _parse_colorways_from_dict(data)

    # Single colorway file - return as a list
    return [_parse_colorway_from_dict(data)]


def _parse_mode_from_dict(data: dict) -> "Mode":
    """
    Parse a mode from a dictionary.

    Supports inheritance via the 'base' field.

    Args:
        data: The dictionary containing mode data.

    Returns:
        The Mode object.

    Raises:
        YAMLParseError: If required fields are missing.
    """
    from sane_figs.core.modes import Mode, get_mode

    # Required field: name
    if "name" not in data:
        raise YAMLParseError("Missing required field: 'name' for mode")

    # Check for inheritance
    base_mode = None
    if "base" in data:
        base_name = data["base"]
        try:
            base_mode = get_mode(base_name)
        except ValueError as e:
            raise YAMLParseError(f"Invalid 'base' mode: {e}")

    # Start with base mode values if inheritance is used, otherwise use defaults
    if base_mode is not None:
        figure_size = base_mode.figure_size
        dpi = base_mode.dpi
        screen_dpi = base_mode.screen_dpi
        font_sizes = dict(base_mode.font_sizes)
        line_width = base_mode.line_width
        marker_size = base_mode.marker_size
    else:
        figure_size = None
        dpi = 300
        screen_dpi = None
        font_sizes = {}
        line_width = 1.5
        marker_size = 6.0

    # Override with values from YAML
    if "figure_size" in data:
        figure_size = tuple(data["figure_size"])
        if len(figure_size) != 2:
            raise YAMLParseError("'figure_size' must be a list of two numbers")

    if "dpi" in data:
        dpi = data["dpi"]

    if "screen_dpi" in data:
        screen_dpi = data["screen_dpi"]

    if "font_sizes" in data:
        font_sizes.update(data["font_sizes"])

    if "line_width" in data:
        line_width = data["line_width"]

    if "marker_size" in data:
        marker_size = data["marker_size"]

    # Require figure_size if not inheriting from a base mode
    if figure_size is None:
        raise YAMLParseError("Missing required field: 'figure_size' (or specify 'base' to inherit)")

    return Mode(
        name=data["name"],
        figure_size=figure_size,
        dpi=dpi,
        screen_dpi=screen_dpi,
        font_sizes=font_sizes,
        line_width=line_width,
        marker_size=marker_size,
    )


def _parse_style_from_dict(data: dict, base_path: Path) -> "Style":
    """
    Parse a style from a dictionary.

    Supports inheritance via the 'base' field.

    Args:
        data: The dictionary containing style data.
        base_path: Base path for resolving relative paths.

    Returns:
        The Style object.

    Raises:
        YAMLParseError: If required fields are missing.
    """
    from sane_figs.core.styles import Style, get_style
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.layout import PlotStyle, TitleConfig, LegendConfig, AxisTitleSpacingConfig

    # Required field: name
    if "name" not in data:
        raise YAMLParseError("Missing required field: 'name' for style")

    # Check for inheritance
    base_style = None
    if "base" in data:
        base_name = data["base"]
        try:
            base_style = get_style(base_name)
        except ValueError as e:
            raise YAMLParseError(f"Invalid 'base' style: {e}")

    # Start with base style values if inheritance is used, otherwise use defaults
    if base_style is not None:
        font_family = base_style.font_family
        colorway = base_style.colorway
        plot_style = PlotStyle(
            background_color=base_style.plot_style.background_color,
            grid_visible=base_style.plot_style.grid_visible,
            grid_color=base_style.plot_style.grid_color,
            grid_opacity=base_style.plot_style.grid_opacity,
            grid_width=base_style.plot_style.grid_width,
            axis_line_color=base_style.plot_style.axis_line_color,
            axis_line_width=base_style.plot_style.axis_line_width,
            show_top_spine=base_style.plot_style.show_top_spine,
            show_right_spine=base_style.plot_style.show_right_spine,
            tick_direction=base_style.plot_style.tick_direction,
            tick_length=base_style.plot_style.tick_length,
            tick_color=base_style.plot_style.tick_color,
            title_weight=base_style.plot_style.title_weight,
            legend_frame_opacity=base_style.plot_style.legend_frame_opacity,
            legend_edge_color=base_style.plot_style.legend_edge_color,
        )
        title_config = base_style.title_config
        legend_config = base_style.legend_config
        axis_title_spacing = base_style.axis_title_spacing
        watermark = base_style.watermark
    else:
        font_family = "sans-serif"
        colorway = None
        plot_style = PlotStyle()
        title_config = None
        legend_config = None
        axis_title_spacing = None
        watermark = None

    # Override with values from YAML
    if "font_family" in data:
        font_family = data["font_family"]

    # Parse colorway
    if "colorway" in data:
        colorway_data = data["colorway"]
        if isinstance(colorway_data, str):
            colorway = get_colorway(colorway_data)
        elif isinstance(colorway_data, dict):
            if "name" in colorway_data and "description" not in colorway_data:
                # Reference to built-in colorway
                colorway = get_colorway(colorway_data["name"])
            else:
                # Inline colorway definition
                colorway = _parse_colorway_from_dict(colorway_data)

    # Parse plot_style overrides
    if "plot_style" in data:
        ps_data = data["plot_style"]
        if isinstance(ps_data, dict):
            for key in (
                "background_color", "grid_visible", "grid_color", "grid_opacity",
                "grid_width", "axis_line_color", "axis_line_width",
                "show_top_spine", "show_right_spine", "tick_direction",
                "tick_length", "tick_color", "title_weight",
                "legend_frame_opacity", "legend_edge_color",
            ):
                if key in ps_data:
                    setattr(plot_style, key, ps_data[key])

    # Parse title configuration
    if "title" in data:
        title_data = data["title"]
        alignment = title_data.get("alignment", "center")
        title_config = TitleConfig(alignment=alignment)

    # Parse legend configuration
    if "legend" in data:
        legend_data = data["legend"]
        position = legend_data.get("position", "inside_upper_right")
        alignment = legend_data.get("alignment", "center")
        x_offset = legend_data.get("x_offset", 0.0)
        y_offset = legend_data.get("y_offset", 0.0)
        legend_config = LegendConfig(
            position=position,
            alignment=alignment,
            x_offset=x_offset,
            y_offset=y_offset,
        )

    # Parse axis title spacing configuration
    if "axis_title_spacing" in data:
        spacing_data = data["axis_title_spacing"]
        x_spacing = spacing_data.get("x_spacing", 8.0)
        y_spacing = spacing_data.get("y_spacing", 8.0)
        plotly_multiplier = spacing_data.get("plotly_multiplier", 1.5)
        altair_multiplier = spacing_data.get("altair_multiplier", 1.2)
        matplotlib_multiplier = spacing_data.get("matplotlib_multiplier", 1.0)
        axis_title_spacing = AxisTitleSpacingConfig(
            x_spacing=x_spacing,
            y_spacing=y_spacing,
            plotly_multiplier=plotly_multiplier,
            altair_multiplier=altair_multiplier,
            matplotlib_multiplier=matplotlib_multiplier,
        )

    # Parse watermark
    if "watermark" in data:
        watermark_data = data["watermark"]
        watermark = _parse_watermark_from_dict(watermark_data, base_path)

    return Style(
        name=data["name"],
        font_family=font_family,
        colorway=colorway,
        plot_style=plot_style,
        title_config=title_config,
        legend_config=legend_config,
        axis_title_spacing=axis_title_spacing,
        watermark=watermark,
    )


def _parse_preset_from_new_format(data: dict, base_path: Path) -> "Preset":
    """
    Parse a preset from the new format with mode and style sections.

    Args:
        data: The dictionary containing preset data with 'mode' and/or 'style' keys.
        base_path: Base path for resolving relative paths.

    Returns:
        The Preset object.

    Raises:
        YAMLParseError: If the data is invalid.
        YAMLValidationError: If the preset is invalid.
    """
    from sane_figs.core.modes import Mode, get_mode
    from sane_figs.core.presets import Preset
    from sane_figs.core.styles import Style, get_style
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.layout import PlotStyle, TitleConfig, LegendConfig, AxisTitleSpacingConfig

    # Parse mode section
    mode_obj = None
    if "mode" in data:
        mode_data = data["mode"]
        if isinstance(mode_data, str):
            # Simple reference to a named mode
            mode_obj = get_mode(mode_data)
        elif isinstance(mode_data, dict):
            mode_obj = _parse_mode_from_dict(mode_data)
        else:
            raise YAMLParseError("'mode' must be a string or a dictionary")
    else:
        # Default to article mode
        mode_obj = get_mode("article")

    # Parse style section
    style_obj = None
    if "style" in data:
        style_data = data["style"]
        if isinstance(style_data, str):
            # Simple reference to a named style
            style_obj = get_style(style_data)
        elif isinstance(style_data, dict):
            style_obj = _parse_style_from_dict(style_data, base_path)
        else:
            raise YAMLParseError("'style' must be a string or a dictionary")
    else:
        # Default to default style
        style_obj = get_style("default")

    # Determine preset name
    preset_name = data.get("name")
    if preset_name is None:
        if isinstance(data.get("mode"), dict) and "name" in data["mode"]:
            mode_name = data["mode"]["name"]
        else:
            mode_name = mode_obj.name if mode_obj else "article"

        if isinstance(data.get("style"), dict) and "name" in data["style"]:
            style_name = data["style"]["name"]
        else:
            style_name = style_obj.name if style_obj else "default"

        preset_name = f"{mode_name}-{style_name}"

    # Build preset from mode and style
    preset = Preset.from_mode_and_style(
        name=preset_name,
        mode=mode_obj,
        style=style_obj,
    )

    # Validate preset
    errors = validate_preset(preset)
    if errors:
        raise YAMLValidationError(errors)

    return preset


def _parse_preset_from_dict(data: dict, base_path: Path) -> "Preset":
    """
    Parse a preset from a dictionary (legacy format).

    Supports inheritance via the 'base' field. When 'base' is specified,
    the preset will inherit all fields from the referenced preset and
    only override the fields defined in the YAML.

    Args:
        data: The dictionary containing preset data.
        base_path: Base path for resolving relative paths.

    Returns:
        The Preset object.

    Raises:
        YAMLParseError: If required fields are missing.
        YAMLValidationError: If the data is invalid.
    """
    from sane_figs.core.presets import Preset, get_preset
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import PlotStyle, TitleConfig, LegendConfig, AxisTitleSpacingConfig

    # Required field: name
    if "name" not in data:
        raise YAMLParseError("Missing required field: 'name'")

    # Check for inheritance
    base_preset = None
    if "base" in data:
        base_name = data["base"]
        try:
            base_preset = get_preset(base_name)
        except ValueError as e:
            raise YAMLParseError(f"Invalid 'base' preset: {e}")

    # Start with base preset values if inheritance is used, otherwise use defaults
    if base_preset is not None:
        # Inherit from base preset
        figure_size = base_preset.figure_size
        dpi = base_preset.dpi
        screen_dpi = base_preset.screen_dpi
        font_family = base_preset.font_family
        font_sizes = dict(base_preset.font_size) if base_preset.font_size else {}
        line_width = base_preset.line_width
        marker_size = base_preset.marker_size
        plot_style = PlotStyle(
            background_color=base_preset.plot_style.background_color,
            grid_visible=base_preset.plot_style.grid_visible,
            grid_color=base_preset.plot_style.grid_color,
            grid_opacity=base_preset.plot_style.grid_opacity,
            grid_width=base_preset.plot_style.grid_width,
            axis_line_color=base_preset.plot_style.axis_line_color,
            axis_line_width=base_preset.plot_style.axis_line_width,
            show_top_spine=base_preset.plot_style.show_top_spine,
            show_right_spine=base_preset.plot_style.show_right_spine,
            tick_direction=base_preset.plot_style.tick_direction,
            tick_length=base_preset.plot_style.tick_length,
            tick_color=base_preset.plot_style.tick_color,
            title_weight=base_preset.plot_style.title_weight,
            legend_frame_opacity=base_preset.plot_style.legend_frame_opacity,
            legend_edge_color=base_preset.plot_style.legend_edge_color,
        )
        colorway = base_preset.colorway
        watermark = base_preset.watermark
        title_config = base_preset.title_config
        legend_config = base_preset.legend_config
        axis_title_spacing = base_preset.axis_title_spacing
        mode = base_preset.mode
    else:
        # Default values when not inheriting
        figure_size = None
        dpi = 300
        screen_dpi = None
        font_family = "sans-serif"
        font_sizes = {}
        line_width = 1.5
        marker_size = 6.0
        plot_style = PlotStyle()
        colorway = None
        watermark = None
        title_config = None
        legend_config = None
        axis_title_spacing = None
        mode = "custom"

    # Override with values from YAML (if present)

    # Parse figure settings
    if "figure" in data:
        figure_data = data["figure"]
        if "size" in figure_data:
            figure_size = tuple(figure_data["size"])
            if len(figure_size) != 2:
                raise YAMLParseError("'figure.size' must be a list of two numbers")
        if "dpi" in figure_data:
            dpi = figure_data["dpi"]
        if "screen_dpi" in figure_data:
            screen_dpi = figure_data["screen_dpi"]

    # Require figure.size if not inheriting from a base preset
    if figure_size is None:
        raise YAMLParseError("Missing required field: 'figure.size' (or specify 'base' to inherit)")

    # Parse typography settings
    if "typography" in data:
        typography_data = data["typography"]
        if "font_family" in typography_data:
            font_family = typography_data["font_family"]
        if "font_sizes" in typography_data:
            # Merge font sizes: YAML values override base preset values
            font_sizes.update(typography_data["font_sizes"])

    # Parse element settings
    if "elements" in data:
        elements_data = data["elements"]
        if "line_width" in elements_data:
            line_width = elements_data["line_width"]
        if "marker_size" in elements_data:
            marker_size = elements_data["marker_size"]

    # Parse mode (if explicitly specified in YAML, override inherited value)
    if "mode" in data:
        mode = data["mode"]

    # Parse colorway
    if "colorway" in data:
        colorway_data = data["colorway"]
        if isinstance(colorway_data, str):
            # Reference to built-in colorway
            colorway = get_colorway(colorway_data)
        elif isinstance(colorway_data, dict):
            # Check if it's a colorway reference (just a name) or inline definition
            if (
                "name" in colorway_data
                and "description" not in colorway_data
                and "colors" not in colorway_data
            ):
                # It's a colorway reference with just a name field
                colorway = get_colorway(colorway_data["name"])
            else:
                # Inline colorway definition
                colorway = _parse_colorway_from_dict(colorway_data)

    # Parse plot_style (override specific fields)
    if "plot_style" in data:
        ps_data = data["plot_style"]
        if isinstance(ps_data, dict):
            ps_kwargs = {}
            for key in (
                "background_color", "grid_visible", "grid_color", "grid_opacity",
                "grid_width", "axis_line_color", "axis_line_width",
                "show_top_spine", "show_right_spine", "tick_direction",
                "tick_length", "tick_color", "title_weight",
                "legend_frame_opacity", "legend_edge_color",
            ):
                if key in ps_data:
                    ps_kwargs[key] = ps_data[key]
            if ps_kwargs:
                # Create new PlotStyle with overridden values
                plot_style = PlotStyle(
                    background_color=ps_kwargs.get("background_color", plot_style.background_color),
                    grid_visible=ps_kwargs.get("grid_visible", plot_style.grid_visible),
                    grid_color=ps_kwargs.get("grid_color", plot_style.grid_color),
                    grid_opacity=ps_kwargs.get("grid_opacity", plot_style.grid_opacity),
                    grid_width=ps_kwargs.get("grid_width", plot_style.grid_width),
                    axis_line_color=ps_kwargs.get("axis_line_color", plot_style.axis_line_color),
                    axis_line_width=ps_kwargs.get("axis_line_width", plot_style.axis_line_width),
                    show_top_spine=ps_kwargs.get("show_top_spine", plot_style.show_top_spine),
                    show_right_spine=ps_kwargs.get("show_right_spine", plot_style.show_right_spine),
                    tick_direction=ps_kwargs.get("tick_direction", plot_style.tick_direction),
                    tick_length=ps_kwargs.get("tick_length", plot_style.tick_length),
                    tick_color=ps_kwargs.get("tick_color", plot_style.tick_color),
                    title_weight=ps_kwargs.get("title_weight", plot_style.title_weight),
                    legend_frame_opacity=ps_kwargs.get("legend_frame_opacity", plot_style.legend_frame_opacity),
                    legend_edge_color=ps_kwargs.get("legend_edge_color", plot_style.legend_edge_color),
                )

    # Parse watermark
    if "watermark" in data:
        watermark_data = data["watermark"]
        watermark = _parse_watermark_from_dict(watermark_data, base_path)

    # Parse title configuration
    if "title" in data:
        title_data = data["title"]
        alignment = title_data.get("alignment", "center")
        title_config = TitleConfig(alignment=alignment)

    # Parse legend configuration
    if "legend" in data:
        legend_data = data["legend"]
        position = legend_data.get("position", "inside_upper_right")
        alignment = legend_data.get("alignment", "center")
        x_offset = legend_data.get("x_offset", 0.0)
        y_offset = legend_data.get("y_offset", 0.0)
        legend_config = LegendConfig(
            position=position,
            alignment=alignment,
            x_offset=x_offset,
            y_offset=y_offset,
        )

    # Parse axis title spacing configuration
    if "axis_title_spacing" in data:
        spacing_data = data["axis_title_spacing"]
        x_spacing = spacing_data.get("x_spacing", 8.0)
        y_spacing = spacing_data.get("y_spacing", 8.0)
        plotly_multiplier = spacing_data.get("plotly_multiplier", 1.5)
        altair_multiplier = spacing_data.get("altair_multiplier", 1.2)
        matplotlib_multiplier = spacing_data.get("matplotlib_multiplier", 1.0)
        axis_title_spacing = AxisTitleSpacingConfig(
            x_spacing=x_spacing,
            y_spacing=y_spacing,
            plotly_multiplier=plotly_multiplier,
            altair_multiplier=altair_multiplier,
            matplotlib_multiplier=matplotlib_multiplier,
        )

    # Create preset
    preset = Preset(
        name=data["name"],
        mode=mode,
        figure_size=figure_size,
        dpi=dpi,
        screen_dpi=screen_dpi,
        font_family=font_family,
        font_size=font_sizes,
        line_width=line_width,
        marker_size=marker_size,
        plot_style=plot_style,
        colorway=colorway,
        watermark=watermark,
        title_config=title_config,
        legend_config=legend_config,
        axis_title_spacing=axis_title_spacing,
    )

    # Validate preset
    errors = validate_preset(preset)
    if errors:
        raise YAMLValidationError(errors)

    return preset


def _parse_presets_from_dict(data: dict, base_path: Path) -> list["Preset"]:
    """
    Parse multiple presets from a dictionary.

    Args:
        data: The dictionary containing presets data.
        base_path: Base path for resolving relative paths.

    Returns:
        List of Preset objects.

    Raises:
        YAMLParseError: If the data structure is invalid.
        YAMLValidationError: If any preset is invalid.
    """
    if "presets" not in data:
        raise YAMLParseError("Missing required field: 'presets'")

    presets_data = data["presets"]
    if not isinstance(presets_data, list):
        raise YAMLParseError("'presets' must be a list")

    presets = []
    for preset_data in presets_data:
        # Check if this preset uses new format
        if "mode" in preset_data or "style" in preset_data:
            preset = _parse_preset_from_new_format(preset_data, base_path)
        else:
            preset = _parse_preset_from_dict(preset_data, base_path)
        presets.append(preset)

    return presets


def _parse_colorway_from_dict(data: dict) -> "Colorway":
    """
    Parse a colorway from a dictionary.

    Args:
        data: The dictionary containing colorway data.

    Returns:
        The Colorway object.

    Raises:
        YAMLParseError: If required fields are missing.
        YAMLValidationError: If the data is invalid.
    """
    from sane_figs.styling.colorways import Colorway

    # Required fields
    if "name" not in data:
        raise YAMLParseError("Missing required field: 'name'")
    if "description" not in data:
        raise YAMLParseError("Missing required field: 'description'")

    # Parse colors
    colors_data = data.get("colors", {})
    categorical = colors_data.get("categorical", [])
    sequential = colors_data.get("sequential", [])
    diverging = colors_data.get("diverging", [])
    qualitative = colors_data.get("qualitative", [])

    # Create colorway
    colorway = Colorway(
        name=data["name"],
        description=data["description"],
        categorical=categorical,
        sequential=sequential,
        diverging=diverging,
        qualitative=qualitative,
    )

    # Validate colorway
    errors = validate_colorway(colorway)
    if errors:
        raise YAMLValidationError(errors)

    return colorway


def _parse_colorways_from_dict(data: dict) -> list["Colorway"]:
    """
    Parse multiple colorways from a dictionary.

    Args:
        data: The dictionary containing colorways data.

    Returns:
        List of Colorway objects.

    Raises:
        YAMLParseError: If the data structure is invalid.
        YAMLValidationError: If any colorway is invalid.
    """
    if "colorways" not in data:
        raise YAMLParseError("Missing required field: 'colorways'")

    colorways_data = data["colorways"]
    if not isinstance(colorways_data, list):
        raise YAMLParseError("'colorways' must be a list")

    colorways = []
    for colorway_data in colorways_data:
        colorway = _parse_colorway_from_dict(colorway_data)
        colorways.append(colorway)

    return colorways


def _parse_watermark_from_dict(data: dict, base_path: Path) -> "WatermarkConfig":
    """
    Parse a watermark from a dictionary.

    Args:
        data: The dictionary containing watermark data.
        base_path: Base path for resolving relative paths.

    Returns:
        The WatermarkConfig object.

    Raises:
        YAMLParseError: If required fields are missing.
        YAMLValidationError: If the data is invalid.
    """
    from sane_figs.styling.watermarks import WatermarkConfig

    # Determine watermark type
    watermark_type = data.get("type", "text")

    # Parse common settings
    position = data.get("position", "bottom-right")
    opacity = data.get("opacity", 0.3)
    scale = data.get("scale", 0.1)
    margin = tuple(data.get("margin", [0.02, 0.02]))

    # Parse font settings
    font_size = data.get("font_size", 12.0)
    font_family = data.get("font_family", "sans-serif")
    font_weight = data.get("font_weight", "normal")
    font_color = data.get("font_color", "#000000")

    # Parse type-specific settings
    image_path = None
    text = None

    if watermark_type == "image":
        if "image_path" not in data:
            raise YAMLParseError("Missing required field for image watermark: 'image_path'")
        image_path = str(base_path / data["image_path"])
    elif watermark_type == "text":
        if "text" not in data:
            raise YAMLParseError("Missing required field for text watermark: 'text'")
        text = data["text"]
    else:
        raise YAMLParseError(
            f"Invalid watermark type: '{watermark_type}'. Must be 'text' or 'image'"
        )

    # Create watermark config
    watermark = WatermarkConfig(
        image_path=image_path,
        text=text,
        position=position,
        opacity=opacity,
        scale=scale,
        margin=margin,
        font_size=font_size,
        font_family=font_family,
        font_weight=font_weight,
        font_color=font_color,
    )

    # Validate watermark
    errors = validate_watermark(watermark)
    if errors:
        raise YAMLValidationError(errors)

    return watermark


def create_sample_preset_yaml(file_path: str | Path) -> Path:
    """
    Create a sample YAML preset template file that users can customize.

    This function generates a well-documented YAML file with the new format
    supporting mode and style sections, including comments explaining each
    setting. Users can modify this file and load it back using
    load_preset_from_file().

    Args:
        file_path: Path where the sample YAML file will be saved.

    Returns:
        The Path to the created file.

    Example:
        >>> from sane_figs import create_sample_preset_yaml
        >>> create_sample_preset_yaml("my_preset.yaml")
        >>> # User edits my_preset.yaml...
        >>> preset = load_preset_from_file("my_preset.yaml")
    """
    path = Path(file_path)
    if path.suffix != ".yaml" and path.suffix != ".yml":
        path = path.with_suffix(".yaml")

    sample_content = """# Sample preset template for sane-figs (new format)
# Edit this file to create a custom preset, then load it with:
#   from sane_figs import load_preset_from_file
#   preset = load_preset_from_file("this_file.yaml")

# Optional: Preset name (auto-generated from mode + style names if not specified)
name: "my-custom-preset"

# Mode section: defines figure dimensions and element sizing
mode:
  # Optional: Name of this mode (for reference)
  name: "my-mode"
  
  # Optional: Base mode to inherit from
  # When specified, all fields from the base mode are copied and can be
  # selectively overridden. Available bases: article, presentation
  base: "article"
  
  # Optional: Override figure size [width, height] in inches
  # figure_size: [3.5, 2.625]
  
  # Optional: DPI for output files (300 for print, 150 for slides)
  # dpi: 300
  
  # Optional: DPI for on-screen / HTML rendering (defaults to 100)
  # screen_dpi: 100
  
  # Optional: Font sizes for different elements (in points)
  # These are merged with base mode font sizes
  # font_sizes:
  #   title: 9.0
  #   label: 8.0
  #   legend: 7.0
  #   tick: 7.0
  #   annotation: 7.0
  
  # Optional: Line and marker sizing
  # line_width: 1.0
  # marker_size: 4.0

# Style section: defines visual appearance (colors, fonts, grid settings)
style:
  # Optional: Name of this style (for reference)
  name: "my-style"
  
  # Optional: Base style to inherit from
  # When specified, all fields from the base style are copied and can be
  # selectively overridden. Available bases: default
  base: "default"
  
  # Optional: Font family (e.g., "sans-serif", "serif", "DejaVu Sans")
  # font_family: "sans-serif"
  
  # Optional: Colorway - can reference a built-in or define inline
  # Option 1: Reference built-in colorway
  # colorway:
  #   name: "default"  # Options: default, nature, vibrant, pastel, colorblind-safe
  
  # Option 2: Define inline colorway
  # colorway:
  #   name: "my-colors"
  #   description: "My custom color palette"
  #   colors:
  #     categorical:
  #       - "#E63946"
  #       - "#457B9D"
  #     sequential:
  #       - "#F1FAEE"
  #       - "#A8DADC"
  #     diverging:
  #       - "#E63946"
  #       - "#2A9D8F"
  #     qualitative:
  #       - "#E63946"
  #       - "#F1FAEE"
  #       - "#457B9D"
  
  # Optional: Plot style settings (grid, spines, etc.)
  # plot_style:
  #   background_color: "white"
  #   grid_visible: true
  #   grid_color: "black"
  #   grid_opacity: 0.3
  #   grid_width: 0.5
  #   axis_line_color: "black"
  #   axis_line_width: 0.8
  #   show_top_spine: false
  #   show_right_spine: false
  #   tick_direction: "outside"
  #   tick_length: 4.0
  #   tick_color: "black"
  #   title_weight: "bold"
  #   legend_frame_opacity: 0.9
  #   legend_edge_color: "inherit"
  
  # Optional: Title configuration
  # title:
  #   alignment: "center"  # "left", "center", or "right"
  
  # Optional: Legend configuration
  # legend:
  #   position: "inside_upper_right"
  #   alignment: "center"
  #   x_offset: 0.0
  #   y_offset: 0.0
  
  # Optional: Axis title spacing
  # axis_title_spacing:
  #   x_spacing: 8.0
  #   y_spacing: 8.0
  #   plotly_multiplier: 1.5
  #   altair_multiplier: 1.2
  #   matplotlib_multiplier: 1.0
  
  # Optional: Watermark configuration
  # watermark:
  #   type: "text"
  #   text: "© 2025 My Lab"
  #   position: "bottom-right"
  #   opacity: 0.3
  #   font_size: 10.0
  #   font_family: "sans-serif"
  #   font_weight: "normal"
  #   font_color: "#000000"
"""

    with open(path, "w") as f:
        f.write(sample_content)

    return path


def create_sample_colorway_yaml(file_path: str | Path) -> Path:
    """
    Create a sample YAML colorway template file that users can customize.

    This function generates a well-documented YAML file with all available
    colorway options, including comments explaining each setting. Users can
    modify this file and load it back using load_colorway_from_yaml().

    Args:
        file_path: Path where the sample YAML file will be saved.

    Returns:
        The Path to the created file.

    Example:
        >>> from sane_figs import create_sample_colorway_yaml
        >>> create_sample_colorway_yaml("my_colorway.yaml")
        >>> # User edits my_colorway.yaml...
        >>> colorway = load_colorway_from_yaml("my_colorway.yaml")
    """
    path = Path(file_path)
    if path.suffix != ".yaml" and path.suffix != ".yml":
        path = path.with_suffix(".yaml")

    sample_content = """# Sample colorway template for sane-figs
# Edit this file to create a custom colorway, then load it with:
#   from sane_figs import load_colorway_from_yaml
#   colorway = load_colorway_from_yaml("this_file.yaml")

colorways:
  # Required: unique colorway name
  - name: "my-lab-colors"

    # Required: description of the colorway
    description: "My lab's official color palette"

    # Color definitions for different plot types
    colors:
      # Categorical colors for bar charts, pie charts, etc.
      # Recommended: 6-10 distinct colors
      categorical:
        - "#E63946"  # Red
        - "#F1FAEE"  # White/Cream
        - "#A8DADC"  # Light blue
        - "#457B9D"  # Medium blue
        - "#1D3557"  # Dark blue
        - "#2A9D8F"  # Teal

      # Sequential colors for heatmaps, gradient plots, etc.
      # Ordered from light to dark
      sequential:
        - "#F1FAEE"
        - "#A8DADC"
        - "#457B9D"
        - "#1D3557"

      # Diverging colors for correlation matrices, etc.
      # Ordered from one extreme through neutral to the other extreme
      diverging:
        - "#E63946"  # Negative extreme
        - "#F4A261"
        - "#E9C46A"  # Neutral
        - "#2A9D8F"
        - "#264653"  # Positive extreme

      # Qualitative colors for complex visualizations
      # Maximum distinctiveness across the full spectrum
      qualitative:
        - "#E63946"
        - "#F1FAEE"
        - "#A8DADC"
        - "#457B9D"
        - "#1D3557"
        - "#2A9D8F"
        - "#E9C46A"
        - "#F4A261"
"""

    with open(path, "w") as f:
        f.write(sample_content)

    return path
