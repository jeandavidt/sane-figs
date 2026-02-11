"""YAML parser for sane-figs presets and colorways."""

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
    from sane_figs.core.presets import Preset
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

    # Single preset file
    preset = _parse_preset_from_dict(data, path.parent)
    return preset


def load_presets_from_yaml(file_path: str | Path) -> list["Preset"]:
    """
    Load multiple presets from a YAML file.

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
    return [_parse_preset_from_dict(data, path.parent)]


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


def _parse_preset_from_dict(data: dict, base_path: Path) -> "Preset":
    """
    Parse a preset from a dictionary.

    Args:
        data: The dictionary containing preset data.
        base_path: Base path for resolving relative paths.

    Returns:
        The Preset object.

    Raises:
        YAMLParseError: If required fields are missing.
        YAMLValidationError: If the data is invalid.
    """
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import get_colorway
    from sane_figs.styling.watermarks import WatermarkConfig

    # Required fields
    if "name" not in data:
        raise YAMLParseError("Missing required field: 'name'")
    if "mode" not in data:
        raise YAMLParseError("Missing required field: 'mode'")

    # Parse figure settings
    figure_data = data.get("figure", {})
    if "size" not in figure_data:
        raise YAMLParseError("Missing required field: 'figure.size'")
    figure_size = tuple(figure_data["size"])
    if len(figure_size) != 2:
        raise YAMLParseError("'figure.size' must be a list of two numbers")
    dpi = figure_data.get("dpi", 300)

    # Parse typography settings
    typography_data = data.get("typography", {})
    font_family = typography_data.get("font_family", "sans-serif")
    font_sizes = typography_data.get("font_sizes", {})

    # Parse element settings
    elements_data = data.get("elements", {})
    line_width = elements_data.get("line_width", 1.5)
    marker_size = elements_data.get("marker_size", 6.0)

    # Parse colorway
    colorway = None
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

    # Parse watermark
    watermark = None
    if "watermark" in data:
        watermark_data = data["watermark"]
        watermark = _parse_watermark_from_dict(watermark_data, base_path)

    # Create preset
    preset = Preset(
        name=data["name"],
        mode=data["mode"],
        figure_size=figure_size,
        dpi=dpi,
        font_family=font_family,
        font_size=font_sizes,
        line_width=line_width,
        marker_size=marker_size,
        colorway=colorway,
        watermark=watermark,
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

    This function generates a well-documented YAML file with all available
    preset options, including comments explaining each setting. Users can
    modify this file and load it back using load_preset_from_file().

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
    import yaml

    path = Path(file_path)
    if path.suffix != ".yaml" and path.suffix != ".yml":
        path = path.with_suffix(".yaml")

    sample_content = """# Sample preset template for sane-figs
# Edit this file to create a custom preset, then load it with:
#   from sane_figs import load_preset_from_file
#   preset = load_preset_from_file("this_file.yaml")

# Required: preset name (must be unique)
name: "my-custom-preset"

# Required: preset mode (e.g., "article", "presentation", or "custom")
mode: "custom"

# Figure settings
figure:
  # Figure size as [width, height] in inches
  size: [6.4, 4.8]
  # DPI for output files (300 for print, 150 for slides)
  dpi: 300

# Typography settings
typography:
  # Font family (e.g., "sans-serif", "serif", "DejaVu Sans")
  font_family: "sans-serif"
  # Font sizes for different elements (in points)
  font_sizes:
    title: 14.0
    label: 12.0
    legend: 10.0
    tick: 10.0
    annotation: 10.0

# Line and marker settings
elements:
  # Line width for plots
  line_width: 1.5
  # Marker size for scatter plots
  marker_size: 6.0

# Colorway: either a reference to a built-in colorway or inline definition
# Option 1: Reference to built-in colorway
colorway:
  name: "default"  # Options: default, nature, vibrant, pastel, colorblind-safe

# Option 2: Inline colorway definition (uncomment to use)
# colorway:
#   name: "my-colors"
#   description: "My custom color palette"
#   colors:
#     categorical:
#       - "#E63946"
#       - "#457B9D"
#       - "#1D3557"
#     sequential:
#       - "#F1FAEE"
#       - "#A8DADC"
#       - "#457B9D"
#       - "#1D3557"
#     diverging:
#       - "#E63946"
#       - "#F4A261"
#       - "#E9C46A"
#       - "#2A9D8F"
#       - "#264653"
#     qualitative:
#       - "#E63946"
#       - "#F1FAEE"
#       - "#A8DADC"
#       - "#457B9D"
#       - "#1D3557"
#       - "#2A9D8F"
#       - "#E9C46A"
#       - "#F4A261"

# Watermark settings (optional - comment out to disable)
watermark:
  # Watermark type: "text" or "image"
  type: "text"
  # For text watermarks: the text to display
  text: "© 2025 My Lab"
  # For image watermarks: path to image file (relative to this YAML file)
  # image_path: "logo.png"
  # Position: "top-left", "top-right", "bottom-left", "bottom-right", "center"
  position: "bottom-right"
  # Opacity (0.0 to 1.0)
  opacity: 0.3
  # For image watermarks: scale factor relative to figure size
  scale: 0.1
  # Font settings (for text watermarks)
  font_size: 10.0
  font_family: "sans-serif"
  font_weight: "normal"
  font_color: "#000000"
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
    import yaml

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
