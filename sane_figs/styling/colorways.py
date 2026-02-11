"""Colorway system for sane-figs."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class Colorway:
    """
    A colorway containing publication-ready color palettes.

    Attributes:
        name: Name of the colorway.
        description: Description of the colorway.
        categorical: Colors for categorical data (distinct categories).
        sequential: Colors for sequential data (ordered values).
        diverging: Colors for diverging data (values with a meaningful midpoint).
        qualitative: Colors for qualitative data (nominal categories).
    """

    name: str
    description: str
    categorical: list[str]
    sequential: list[str]
    diverging: list[str]
    qualitative: list[str]


# Default Colorway
# Optimized for print publication with good contrast in grayscale
DEFAULT_COLORWAY = Colorway(
    name="default",
    description="Publication-ready color palette optimized for print",
    categorical=[
        "#1f77b4",  # Blue
        "#ff7f0e",  # Orange
        "#2ca02c",  # Green
        "#d62728",  # Red
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
        "#bcbd22",  # Olive
        "#17becf",  # Cyan
    ],
    sequential=[
        "#f7fbff",  # Lightest blue
        "#deebf7",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#08519c",
        "#081d58",  # Darkest blue
    ],
    diverging=[
        "#67001f",  # Dark red
        "#b2182b",
        "#d6604d",
        "#f4a582",
        "#fddbc7",
        "#f7f7f7",  # Neutral center
        "#d1e5f0",
        "#92c5de",
        "#4393c3",
        "#2166ac",
        "#053061",  # Dark blue
    ],
    qualitative=[
        "#4e79a7",  # Blue
        "#f28e2b",  # Orange
        "#e15759",  # Red
        "#76b7b2",  # Teal
        "#59a14f",  # Green
        "#edc948",  # Yellow
        "#b07aa1",  # Purple
        "#ff9da7",  # Pink
        "#9c755f",  # Brown
        "#bab0ac",  # Gray
    ],
)

# Nature Colorway
# Earth tones inspired by nature
NATURE_COLORWAY = Colorway(
    name="nature",
    description="Earth tones inspired by nature",
    categorical=[
        "#2d6a4f",  # Forest green
        "#d4a373",  # Sand
        "#bc6c25",  # Earth brown
        "#606c38",  # Olive
        "#dda15e",  # Tan
        "#283618",  # Dark green
        "#fefae0",  # Cream
        "#bc4749",  # Terracotta
        "#6a994e",  # Light green
        "#386641",  # Medium green
    ],
    sequential=[
        "#f0f4c3",  # Lightest green
        "#dce775",
        "#cddc39",
        "#afb42b",
        "#9e9d24",
        "#827717",
        "#689f38",
        "#558b2f",
        "#33691e",
        "#1b5e20",  # Darkest green
    ],
    diverging=[
        "#8b4513",  # Saddle brown
        "#a0522d",
        "#cd853f",
        "#deb887",
        "#f5deb3",
        "#ffffff",  # White center
        "#e0f2f1",
        "#b2dfdb",
        "#80cbc4",
        "#4db6ac",
        "#009688",  # Teal
    ],
    qualitative=[
        "#264653",  # Dark blue-green
        "#2a9d8f",  # Teal
        "#e9c46a",  # Yellow
        "#f4a261",  # Orange
        "#e76f51",  # Burnt orange
        "#6b705c",  # Gray-green
        "#a5a58d",  # Sage
        "#cb997e",  # Light brown
        "#ddbea9",  # Tan
        "#ffe8d6",  # Peach
    ],
)

# Vibrant Colorway
# High contrast colors optimized for presentations
VIBRANT_COLORWAY = Colorway(
    name="vibrant",
    description="High contrast colors optimized for presentations",
    categorical=[
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
        "#FFFF00",  # Yellow
        "#FF00FF",  # Magenta
        "#00FFFF",  # Cyan
        "#FF8000",  # Orange
        "#8000FF",  # Purple
        "#00FF80",  # Spring green
        "#FF0080",  # Hot pink
    ],
    sequential=[
        "#FFFFE0",  # Light yellow
        "#FFFF00",
        "#FFD700",
        "#FFA500",
        "#FF8C00",
        "#FF4500",
        "#FF0000",
        "#DC143C",
        "#B22222",
        "#8B0000",  # Dark red
    ],
    diverging=[
        "#0000FF",  # Blue
        "#1E90FF",
        "#00BFFF",
        "#87CEEB",
        "#E0FFFF",
        "#FFFFFF",  # White center
        "#FFE4E1",
        "#FFB6C1",
        "#FF69B4",
        "#FF1493",
        "#FF0000",  # Red
    ],
    qualitative=[
        "#E63946",  # Red
        "#F1FAEE",  # White
        "#A8DADC",  # Light blue
        "#457B9D",  # Medium blue
        "#1D3557",  # Dark blue
        "#2A9D8F",  # Teal
        "#E9C46A",  # Yellow
        "#F4A261",  # Orange
        "#E76F51",  # Burnt orange
        "#264653",  # Dark teal
    ],
)

# Pastel Colorway
# Soft, professional colors
PASTEL_COLORWAY = Colorway(
    name="pastel",
    description="Soft, professional colors",
    categorical=[
        "#AEC6CF",  # Pastel blue
        "#FFB347",  # Pastel orange
        "#77DD77",  # Pastel green
        "#FF6961",  # Pastel red
        "#C3B1E1",  # Pastel purple
        "#F49AC2",  # Pastel pink
        "#FDFD96",  # Pastel yellow
        "#B39EB5",  # Pastel violet
        "#FFB7B2",  # Pastel coral
        "#B5EAD7",  # Pastel mint
    ],
    sequential=[
        "#F0F8FF",  # Alice blue
        "#E6F3FF",
        "#CCE7FF",
        "#99D6FF",
        "#66C5FF",
        "#33B4FF",
        "#00A3FF",
        "#0092E6",
        "#0081CC",
        "#0070B3",  # Medium blue
    ],
    diverging=[
        "#FFB3BA",  # Pastel red
        "#FFDFBA",
        "#FFFFBA",
        "#BAFFC9",
        "#BAE1FF",
        "#FFFFFF",  # White center
        "#E0F2F1",
        "#B2DFDB",
        "#80CBC4",
        "#4DB6AC",
        "#009688",  # Teal
    ],
    qualitative=[
        "#FFB5E8",  # Pastel pink
        "#B5DEFF",  # Pastel blue
        "#DCD3FF",  # Pastel purple
        "#AFF8DB",  # Pastel mint
        "#FFC8A2",  # Pastel peach
        "#FFF5BA",  # Pastel yellow
        "#FF9AA2",  # Pastel salmon
        "#E2F0CB",  # Pastel lime
        "#B5EAD7",  # Pastel mint
        "#C7CEEA",  # Pastel periwinkle
    ],
)

# Colorblind-Safe Colorway
# Specifically designed for colorblind accessibility using CUD principles
COLORBLIND_SAFE_COLORWAY = Colorway(
    name="colorblind-safe",
    description="Designed for colorblind accessibility using CUD principles",
    categorical=[
        "#E69F00",  # Orange
        "#56B4E9",  # Sky blue
        "#009E73",  # Bluish green
        "#F0E442",  # Yellow
        "#0072B2",  # Blue
        "#D55E00",  # Vermilion
        "#CC79A7",  # Reddish purple
        "#000000",  # Black
    ],
    sequential=[
        "#F7FCF5",  # Lightest green
        "#E5F5E0",
        "#C7E9C0",
        "#A1D99B",
        "#74C476",
        "#41AB5D",
        "#238B45",
        "#006D2C",
        "#00441B",  # Darkest green
    ],
    diverging=[
        "#B2182B",  # Dark red
        "#D6604D",
        "#F4A582",
        "#FDDBC7",
        "#F7F7F7",  # Neutral center
        "#D1E5F0",
        "#92C5DE",
        "#4393C3",
        "#2166AC",
        "#053061",  # Dark blue
    ],
    qualitative=[
        "#E69F00",  # Orange
        "#56B4E9",  # Sky blue
        "#009E73",  # Bluish green
        "#F0E442",  # Yellow
        "#0072B2",  # Blue
        "#D55E00",  # Vermilion
        "#CC79A7",  # Reddish purple
        "#000000",  # Black
    ],
)

# ULaval Colorway
# Université Laval official colors
ULAVAL_COLORWAY = Colorway(
    name="ulaval",
    description="Université Laval official colors",
    categorical=[
        "#e30513",  # Laval Red
        "#ffc103",  # Laval Yellow
        "#515151",  # Laval Dark Grey
        "#7f7f7f",  # Laval Medium Grey
        "#d9d9d9",  # Laval Light Grey
        "#000000",  # Black
    ],
    sequential=[
        "#fce6e7",  # Lightest red
        "#f9cdce",
        "#f6b4b5",
        "#f39b9c",
        "#f08283",
        "#ed696a",
        "#ea5051",
        "#e73738",
        "#e30513",  # Laval Red
    ],
    diverging=[
        "#515151",  # Dark Grey
        "#7f7f7f",
        "#d9d9d9",
        "#f0f0f0",  # Light grey
        "#ffffff",  # White
        "#fff6d9",
        "#ffedb3",
        "#ffe48d",
        "#ffdb66",
        "#ffc103",  # Laval Yellow
    ],
    qualitative=[
        "#e30513",  # Laval Red
        "#ffc103",  # Laval Yellow
        "#515151",  # Laval Dark Grey
        "#7f7f7f",  # Laval Medium Grey
        "#d9d9d9",  # Laval Light Grey
    ],
)

# ModelEAU Colorway
# ModelEAU research group colors (Placeholder Blue/Black)
MODELEAU_COLORWAY = Colorway(
    name="modeleau",
    description="ModelEAU research group colors",
    categorical=[
        "#0055A4",  # Royal Blue (Placeholder)
        "#000000",  # Black
        "#808080",  # Grey
        "#ADD8E6",  # Light Blue
    ],
    sequential=[
        "#E6F3FF",
        "#CCE7FF",
        "#99D6FF",
        "#66C5FF",
        "#33B4FF",
        "#00A3FF",
        "#0092E6",
        "#0055A4",  # Dark Blue
    ],
    diverging=[
        "#808080",  # Grey
        "#D3D3D3",
        "#E6F3FF",
        "#FFFFFF",
        "#E6F3FF",
        "#99D6FF",
        "#0055A4",  # Blue
    ],
    qualitative=[
        "#0055A4",
        "#000000",
        "#808080",
        "#ADD8E6",
    ],
)

# Marimo Colorway
# Marimo notebook aesthetics (Moss Green accent)
MARIMO_COLORWAY = Colorway(
    name="marimo",
    description="Marimo notebook aesthetics",
    categorical=[
        "#578926",  # primary (moss green)
        "#4b5563",  # gray-600
        "#0891b2",  # cyan-600
        "#d97706",  # amber-600
        "#db2777",  # pink-600
        "#4f46e5",  # indigo-600
        "#059669",  # emerald-600
        "#dc2626",  # red-600
    ],
    sequential=[
        "#f0fdf4",  # green-50
        "#dcfce7",  # green-100
        "#bbf7d0",  # green-200
        "#86efac",  # green-300
        "#4ade80",  # green-400
        "#22c55e",  # green-500
        "#16a34a",  # green-600
        "#15803d",  # green-700
        "#166534",  # green-800
        "#14532d",  # green-900
    ],
    diverging=[
        "#991b1b",  # red-800
        "#dc2626",  # red-600
        "#f87171",  # red-400
        "#fecaca",  # red-200
        "#f9fafb",  # gray-50 (center)
        "#bbf7d0",  # green-200
        "#4ade80",  # green-400
        "#16a34a",  # green-600
        "#166534",  # green-800
    ],
    qualitative=[
        "#578926",  # primary
        "#374151",  # gray-700
        "#6b7280",  # gray-500
        "#9ca3af",  # gray-400
    ],
)

# Registry of all colorways
_COLORWAY_REGISTRY: dict[str, Colorway] = {
    "default": DEFAULT_COLORWAY,
    "nature": NATURE_COLORWAY,
    "vibrant": VIBRANT_COLORWAY,
    "pastel": PASTEL_COLORWAY,
    "colorblind-safe": COLORBLIND_SAFE_COLORWAY,
    "ulaval": ULAVAL_COLORWAY,
    "modeleau": MODELEAU_COLORWAY,
    "marimo": MARIMO_COLORWAY,
}


def get_colorway(name: str) -> Colorway:
    """
    Get a colorway by name.

    Args:
        name: The name of the colorway.

    Returns:
        The Colorway object.

    Raises:
        ValueError: If the colorway name is not found.
    """
    if name not in _COLORWAY_REGISTRY:
        raise ValueError(
            f"Unknown colorway '{name}'. Available colorways: {list(_COLORWAY_REGISTRY.keys())}"
        )
    return _COLORWAY_REGISTRY[name]


def list_colorways() -> list[str]:
    """
    List all available colorways.

    Returns:
        List of colorway names.
    """
    return list(_COLORWAY_REGISTRY.keys())


def register_colorway(colorway: Colorway) -> None:
    """
    Register a custom colorway.

    Args:
        colorway: The Colorway object to register.

    Raises:
        ValueError: If a colorway with the same name already exists.
    """
    if colorway.name in _COLORWAY_REGISTRY:
        raise ValueError(
            f"Colorway '{colorway.name}' already exists. Use a different name."
        )
    _COLORWAY_REGISTRY[colorway.name] = colorway


def unregister_colorway(name: str) -> None:
    """
    Unregister a colorway by name.

    Args:
        name: The name of the colorway to unregister.

    Raises:
        ValueError: If the colorway is not found or is a built-in colorway.
    """
    if name not in _COLORWAY_REGISTRY:
        raise ValueError(f"Colorway '{name}' not found.")

    # Prevent unregistering built-in colorways
    built_in = ["default", "nature", "vibrant", "pastel", "colorblind-safe", "ulaval", "modeleau", "marimo"]
    if name in built_in:
        raise ValueError(f"Cannot unregister built-in colorway '{name}'.")

    del _COLORWAY_REGISTRY[name]
