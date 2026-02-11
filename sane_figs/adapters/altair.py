"""Altair adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig

from sane_figs.adapters.base import BaseAdapter


class AltairAdapter(BaseAdapter):
    """
    Adapter for Altair plotting library.

    This adapter applies publication-ready styling to Altair charts
    with version-specific API handling.
    """

    # Version-specific handlers
    VERSION_HANDLERS = {
        (5, 0, 0): "_handle_v5_0_plus",
        (4, 2, 0): "_handle_v4_2_plus",
        (3, 0, 0): "_handle_v3_0_plus",
    }

    def __init__(self) -> None:
        """Initialize the Altair adapter."""
        super().__init__("altair")
        self._altair = None
        self._original_theme = None
        self._current_theme = None
        self._base_theme_config = None  # Store the base theme config to avoid recursion

    def _import_altair(self) -> bool:
        """
        Import Altair.

        Returns:
            True if import was successful, False otherwise.
        """
        try:
            import altair as alt

            self._altair = alt
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check if Altair is available for use.

        Returns:
            True if Altair is installed and can be used, False otherwise.
        """
        if self._altair is None:
            return self._import_altair()
        return True

    def get_version(self) -> str | None:
        """
        Get the version of the installed Altair.

        Returns:
            Version string or None if Altair is not installed.
        """
        if not self.is_available():
            return None
        return self._altair.__version__

    def apply_style(self, preset: "Preset") -> None:
        """
        Apply publication-ready styling to Altair.

        Args:
            preset: The Preset object containing styling configuration.
        """
        if not self.is_available():
            return

        # Save original theme
        self._save_original_settings()

        # Configure Altair theme
        self._configure_theme(preset)

        # Handle version-specific settings
        self._handle_version_specifics()

        # Apply colorway if specified
        if preset.colorway is not None:
            self.apply_colorway(preset.colorway)

        # Apply watermark if specified
        if preset.watermark is not None:
            self.add_watermark(preset.watermark)

    def reset_style(self) -> None:
        """
        Reset Altair styling to its original state.
        """
        if not self.is_available():
            return

        # Reset to original theme
        if self._original_theme is not None:
            try:
                self._altair.themes.enable(self._original_theme)
            except Exception:
                pass

        # Clear stored state
        self._current_theme = None

    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to Altair.

        Args:
            colorway: The Colorway object to apply.
        """
        if not self.is_available():
            return

        try:
            # Update the current theme with the colorway
            if self._base_theme_config is not None:
                # Create a new theme that merges the base theme with the colorway
                def merged_theme():
                    # Use the base theme config to avoid recursion
                    theme_config = self._base_theme_config.copy()
                    # Add colorway to the theme
                    theme_config["config"]["range"] = {
                        "category": colorway.categorical,
                        "diverging": colorway.diverging,
                        "ordinal": colorway.qualitative,
                    }
                    return theme_config

                # Re-register the updated theme
                self._altair.themes.register("sane_figs", merged_theme)
                self._altair.themes.enable("sane_figs")
                self._current_theme = merged_theme
            else:
                # Fallback: create a new theme if base_theme_config doesn't exist
                def colorway_theme():
                    return {
                        "config": {
                            "range": {
                                "category": colorway.categorical,
                                "diverging": colorway.diverging,
                                "ordinal": colorway.qualitative,
                            }
                        }
                    }

                self._altair.themes.register("sane_figs", colorway_theme)
                self._altair.themes.enable("sane_figs")
                self._current_theme = colorway_theme
        except Exception:
            pass

    def add_watermark(self, config: "WatermarkConfig") -> None:
        """
        Add a watermark to Altair charts.

        Note: This stores the watermark configuration. Users can add watermarks
        to their charts using the add_watermark_to_chart() method.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config for use when charts are created
        self._watermark_config = config

        # Note: We don't wrap alt.Chart because it breaks method chaining
        # Users should call add_watermark_to_chart() on their charts

    def add_watermark_to_chart(self, chart, config: "WatermarkConfig"):
        """
        Add a watermark to a specific Altair chart.

        Args:
            chart: The Altair chart.
            config: The WatermarkConfig object.

        Returns:
            The chart with watermark added.
        """
        if config.text is not None:
            # Text watermark
            return self._add_text_watermark(chart, config)
        elif config.image_path is not None:
            # Image watermark
            return self._add_image_watermark(chart, config)
        return chart

    def _add_text_watermark(self, chart, config: "WatermarkConfig"):
        """
        Add a text watermark to an Altair chart.

        Args:
            chart: The Altair chart.
            config: The WatermarkConfig object.

        Returns:
            The chart with watermark added.
        """
        import pandas as pd

        # Calculate position
        x, y, x_anchor, y_anchor = self._get_watermark_position(config)

        # Create a text layer for the watermark
        watermark_data = pd.DataFrame(
            {
                "x": [x],
                "y": [y],
                "text": [config.text],
            }
        )

        watermark = (
            self._altair.Chart(watermark_data)
            .mark_text(
                fontSize=config.font_size,
                font=config.font_family,
                fontWeight=config.font_weight,
                color=config.font_color,
                opacity=config.opacity,
                dx=0,
                dy=0,
            )
            .encode(
                x=self._altair.X("x", axis=None),
                y=self._altair.Y("y", axis=None),
                text="text",
            )
        )

        # Combine with original chart
        return (chart + watermark).resolve_scale(x="independent", y="independent")

    def _add_image_watermark(self, chart, config: "WatermarkConfig"):
        """
        Add an image watermark to an Altair chart.

        Args:
            chart: The Altair chart.
            config: The WatermarkConfig object.

        Returns:
            The chart with watermark added.
        """
        import pandas as pd

        # Calculate position
        x, y, x_anchor, y_anchor = self._get_watermark_position(config)

        # Create an image layer for the watermark
        watermark_data = pd.DataFrame(
            {
                "x": [x],
                "y": [y],
                "url": [config.image_path],
            }
        )

        watermark = (
            self._altair.Chart(watermark_data)
            .mark_image(
                width=config.scale * 100,  # Approximate width
                height=config.scale * 100,  # Approximate height
                opacity=config.opacity,
            )
            .encode(
                x=self._altair.X("x", axis=None),
                y=self._altair.Y("y", axis=None),
                url="url",
            )
        )

        # Combine with original chart
        return (chart + watermark).resolve_scale(x="independent", y="independent")

    def _get_watermark_position(self, config: "WatermarkConfig") -> tuple[float, float, str, str]:
        """
        Get the position for a watermark in Altair coordinates.

        Args:
            config: The WatermarkConfig object.

        Returns:
            Tuple of (x, y, x_anchor, y_anchor) for Altair text/image.
        """
        margin_x = config.margin[0]
        margin_y = config.margin[1]

        if config.position == "top-left":
            x, y = margin_x, 1 - margin_y
            x_anchor, y_anchor = "left", "top"
        elif config.position == "top-right":
            x, y = 1 - margin_x, 1 - margin_y
            x_anchor, y_anchor = "right", "top"
        elif config.position == "bottom-left":
            x, y = margin_x, margin_y
            x_anchor, y_anchor = "left", "bottom"
        elif config.position == "bottom-right":
            x, y = 1 - margin_x, margin_y
            x_anchor, y_anchor = "right", "bottom"
        elif config.position == "center":
            x, y = 0.5, 0.5
            x_anchor, y_anchor = "center", "middle"
        else:
            x, y = 1 - margin_x, margin_y
            x_anchor, y_anchor = "right", "bottom"

        return (x, y, x_anchor, y_anchor)

    def _save_original_settings(self) -> None:
        """Save the original Altair settings."""
        try:
            # Get current theme
            self._original_theme = self._altair.themes.active
        except Exception:
            self._original_theme = "default"

    def _configure_theme(self, preset: "Preset") -> None:
        """
        Configure Altair theme based on preset.

        Args:
            preset: The Preset object containing styling configuration.
        """
        try:
            # Convert point sizes to pixels for Altair
            # Altair uses pixels for font sizes, while preset uses points
            # Conversion: pixels = points * (DPI / 72)
            dpi_scale = preset.dpi / 72.0

            # For Altair charts (which are displayed primarily on screens),
            # use a screen-appropriate DPI (96-100) instead of print DPI
            # to calculate pixel dimensions, while keeping the aspect ratio
            screen_dpi = 100
            
            # Create the base theme config
            base_theme_config = {
                "config": {
                    "view": {
                        "width": int(preset.figure_size[0] * screen_dpi),
                        "height": int(preset.figure_size[1] * screen_dpi),
                        # Remove border around the chart (matches spines.top/right=False)
                        "stroke": "transparent",
                    },
                    "font": preset.font_family,
                    "title": {
                        "font": preset.font_family,
                        "fontSize": preset.font_size.get("title", 14) * dpi_scale,
                        "fontWeight": "bold",
                        "anchor": "start",  # Match Matplotlib's left-aligned title
                        "offset": 10,
                    },
                    "axis": {
                        "titleFont": preset.font_family,
                        "labelFont": preset.font_family,
                        "titleFontSize": preset.font_size.get("label", 12) * dpi_scale,
                        "labelFontSize": preset.font_size.get("tick", 10) * dpi_scale,
                        
                        # Grid settings (matches axes.grid=True)
                        "grid": True,
                        "gridOpacity": 0.3,
                        "gridWidth": 0.5 * dpi_scale,
                        "gridColor": "black",

                        # Tick settings
                        "tickCount": 5,  # Heuristic for sparse ticks
                        "ticks": True,
                        "tickWidth": 0.5 * dpi_scale,
                        "tickSize": 4 * dpi_scale,
                        
                        # Axis Line settings (spines)
                        "domain": True,  # Show axis line
                        "domainColor": "black",
                        "domainWidth": 0.8 * dpi_scale,
                    },
                    "legend": {
                        "titleFont": preset.font_family,
                        "labelFont": preset.font_family,
                        "titleFontSize": preset.font_size.get("legend", 10) * dpi_scale,
                        "labelFontSize": preset.font_size.get("legend", 10) * dpi_scale,
                    },
                    "header": {
                         "titleFont": preset.font_family,
                         "labelFont": preset.font_family,
                    },
                    "text": {
                        "font": preset.font_family,
                    },
                    "mark": {
                        "strokeWidth": preset.line_width * dpi_scale,
                        "size": (preset.marker_size * dpi_scale)**2,
                    },
                    "point": {
                        "size": (preset.marker_size * dpi_scale)**2,
                    },
                    "circle": {
                        "size": (preset.marker_size * dpi_scale)**2,
                    },
                    "square": {
                        "size": (preset.marker_size * dpi_scale)**2,
                    },
                }
            }

            # Store the base theme config to avoid recursion
            self._base_theme_config = base_theme_config

            # Create a custom theme function that returns the base config
            def custom_theme():
                return base_theme_config

            # Store the theme for later modification (e.g., colorway)
            self._current_theme = custom_theme

            # Register and enable the custom theme
            self._altair.themes.register("sane_figs", custom_theme)
            self._altair.themes.enable("sane_figs")
        except Exception:
            pass

    def _handle_version_specifics(self) -> None:
        """Handle version-specific Altair settings."""
        version = self.get_version_tuple()
        if version is None:
            return

        # Find the appropriate handler for this version
        for min_version, handler_name in reversed(self.VERSION_HANDLERS.items()):
            if version >= min_version:
                handler = getattr(self, handler_name, None)
                if handler is not None:
                    handler()
                break

    def _handle_v5_0_plus(self) -> None:
        """Handle Altair 5.0+ specific settings."""
        # Altair 5.0+ has improved theme handling
        pass

    def _handle_v4_2_plus(self) -> None:
        """Handle Altair 4.2+ specific settings."""
        # Altair 4.2+ has improved color handling
        pass

    def _handle_v3_0_plus(self) -> None:
        """Handle Altair 3.0+ specific settings."""
        # Altair 3.0+ has improved default themes
        pass
