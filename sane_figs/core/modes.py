"""Mode definitions for sane-figs.

Modes determine figure dimensions, DPI, and element sizing appropriate
for the output medium (article, presentation, etc.).
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class Mode:
    """
    A mode defining figure dimensions and element sizing.

    Modes determine the physical size and resolution of figures,
    as well as font sizes appropriate for the output medium.

    Attributes:
        name: Name of the mode.
        figure_size: Figure size as (width, height) in inches.
        dpi: Dots per inch for output files.
        screen_dpi: DPI for screen/display rendering.
        font_sizes: Dictionary of font sizes for different elements.
        line_width: Default line width for plots.
        marker_size: Default marker size for scatter plots.
    """

    name: str
    figure_size: tuple[float, float]
    dpi: int
    font_sizes: dict[str, float] = field(default_factory=dict)
    screen_dpi: int | None = None
    line_width: float = 1.5
    marker_size: float = 6.0

    def get_display_dpi(self) -> int:
        """DPI for HTML/screen rendering.

        Returns screen_dpi if set, otherwise defaults to 100.
        """
        return self.screen_dpi if self.screen_dpi is not None else 100


# Mode registry
_MODE_REGISTRY: dict[str, Mode] = {}


def register_mode(mode: Mode) -> None:
    """
    Register a mode in the registry.

    Args:
        mode: The Mode object to register.

    Raises:
        ValueError: If the mode name is a built-in mode that already exists.
    """
    built_in = ["article", "presentation"]
    if mode.name in built_in and mode.name in _MODE_REGISTRY:
        raise ValueError(
            f"Cannot re-register built-in mode '{mode.name}'. Use a different name."
        )
    _MODE_REGISTRY[mode.name] = mode


def unregister_mode(name: str) -> None:
    """
    Unregister a mode by name.

    Args:
        name: The name of the mode to unregister.

    Raises:
        ValueError: If the mode is not found or is a built-in mode.
    """
    if name not in _MODE_REGISTRY:
        raise ValueError(f"Mode '{name}' not found.")

    built_in = ["article", "presentation"]
    if name in built_in:
        raise ValueError(f"Cannot unregister built-in mode '{name}'.")

    del _MODE_REGISTRY[name]


def get_mode(name: str | Mode) -> Mode:
    """
    Get a mode by name.

    Args:
        name: The mode name or a Mode object (returned as-is).

    Returns:
        The Mode object.

    Raises:
        ValueError: If the mode is not recognized.
    """
    if isinstance(name, Mode):
        return name

    if name not in _MODE_REGISTRY:
        raise ValueError(
            f"Unknown mode '{name}'. Available modes: {list(_MODE_REGISTRY.keys())}"
        )
    return _MODE_REGISTRY[name]


def list_modes() -> list[str]:
    """
    List all available mode names.

    Returns:
        List of mode names.
    """
    return list(_MODE_REGISTRY.keys())


# Built-in modes

# Article Mode
# Optimized for print publication at single-column journal width.
_ARTICLE_MODE = Mode(
    name="article",
    figure_size=(3.5, 2.625),  # Standard single-column journal width, 4:3 aspect
    dpi=300,  # Print quality
    screen_dpi=100,
    font_sizes={
        "title": 9.0,
        "label": 8.0,
        "legend": 7.0,
        "tick": 7.0,
        "annotation": 7.0,
    },
    line_width=1.0,
    marker_size=4.0,
)

# Presentation Mode
# Optimized for figures on 16:9 widescreen slides.
_PRESENTATION_MODE = Mode(
    name="presentation",
    figure_size=(10.0, 5.6),  # ~75% of 16:9 slide area
    dpi=300,  # High quality for export
    screen_dpi=100,  # Better for notebook/web display
    font_sizes={
        "title": 24.0,
        "label": 20.0,
        "legend": 18.0,
        "tick": 18.0,
        "annotation": 18.0,
    },
    line_width=2.5,
    marker_size=9.0,
)

# Register built-in modes
register_mode(_ARTICLE_MODE)
register_mode(_PRESENTATION_MODE)

# Export for convenience
ARTICLE_MODE = _ARTICLE_MODE
PRESENTATION_MODE = _PRESENTATION_MODE
