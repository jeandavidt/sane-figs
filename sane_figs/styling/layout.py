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

TickDirectionType = Literal["outside", "inside", "both"]


@dataclass
class PlotStyle:
    """Shared visual "chrome" for a plot.

    Every property that was previously hard-coded inside individual adapters
    now lives here so that all four backends (Matplotlib, Seaborn, Altair,
    Plotly) render identically from a single source of truth.

    Attributes:
        background_color: Axes / plot-area background colour.
        grid_visible: Whether to show grid lines.
        grid_color: Grid line colour (before opacity is applied).
        grid_opacity: Grid line transparency (0 = invisible, 1 = solid).
        grid_width: Grid line width in points.
        axis_line_color: Colour for the left / bottom axis lines (spines).
        axis_line_width: Width of the left / bottom spines in points.
        show_top_spine: Whether to draw the top spine.
        show_right_spine: Whether to draw the right spine.
        tick_direction: Tick mark direction relative to the axis.
        tick_length: Tick mark length in points.
        tick_color: Tick mark colour.
        title_weight: Font weight for the axes title.
        legend_frame_opacity: Background opacity of the legend box (0–1).
        legend_edge_color: Colour of the legend frame edge.
    """

    background_color: str = "white"
    grid_visible: bool = True
    grid_color: str = "black"
    grid_opacity: float = 0.3
    grid_width: float = 0.5
    axis_line_color: str = "black"
    axis_line_width: float = 0.8
    show_top_spine: bool = False
    show_right_spine: bool = False
    tick_direction: TickDirectionType = "outside"
    tick_length: float = 4.0
    tick_color: str = "black"
    title_weight: str = "bold"
    legend_frame_opacity: float = 0.9
    legend_edge_color: str = "inherit"


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
