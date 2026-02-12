"""Layout configuration for title alignment, legend positioning, and spacing."""

from dataclasses import dataclass
from typing import Literal


TitleAlignmentType = Literal["left", "center", "right"]

LegendPositionType = Literal[
    "inside_upper_right",
    "inside_upper_left",
    "inside_lower_right",
    "inside_lower_left",
    "inside_center",
    "outside_right",
    "outside_left",
    "outside_top",
    "outside_bottom",
]


@dataclass
class TitleConfig:
    """Configuration for plot title alignment.

    Attributes:
        alignment: Horizontal alignment of the title.
            - "left": Left-aligned title
            - "center": Center-aligned title
            - "right": Right-aligned title
    """

    alignment: TitleAlignmentType = "center"


@dataclass
class LegendConfig:
    """Configuration for legend positioning.

    Attributes:
        position: Position of the legend.
            - "inside_upper_right": Inside plot, upper right corner
            - "inside_upper_left": Inside plot, upper left corner
            - "inside_lower_right": Inside plot, lower right corner
            - "inside_lower_left": Inside plot, lower left corner
            - "inside_center": Inside plot, center
            - "outside_right": Outside plot, on the right
            - "outside_left": Outside plot, on the left
            - "outside_top": Outside plot, at the top
            - "outside_bottom": Outside plot, at the bottom
        alignment: Alignment of legend items when positioned outside.
            - "start": Left-aligned (for left-side legends)
            - "center": Center-aligned
            - "end": Right-aligned (for right-side legends)
        x_offset: Horizontal offset from the anchor position (0-1 scale or absolute).
        y_offset: Vertical offset from the anchor position (0-1 scale or absolute).
    """

    position: LegendPositionType = "inside_upper_right"
    alignment: Literal["start", "center", "end"] = "center"
    x_offset: float = 0.0
    y_offset: float = 0.0


@dataclass
class AxisTitleSpacingConfig:
    """Configuration for axis title spacing.

    Attributes:
        x_spacing: Horizontal spacing for x-axis title (in points).
        y_spacing: Vertical spacing for y-axis title (in points).
        multiplier: Library-specific multiplier to normalize spacing across libraries.
            Different libraries have different default spacings, so this allows
            normalization. For example, Plotly tends to have tighter spacing
            than Matplotlib, so a multiplier > 1 can be applied.
    """

    x_spacing: float = 8.0
    y_spacing: float = 8.0
    plotly_multiplier: float = 1.5
    altair_multiplier: float = 1.2
    matplotlib_multiplier: float = 1.0
