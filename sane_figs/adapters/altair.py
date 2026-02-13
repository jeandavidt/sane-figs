"""Altair adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import TitleConfig, LegendConfig, AxisTitleSpacingConfig

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
        self._watermark_config = None

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

        # Apply title config if specified
        if preset.title_config is not None:
            self.apply_title_config(preset.title_config)

        # Apply legend config if specified
        if preset.legend_config is not None:
            self.apply_legend_config(preset.legend_config)

        # Apply axis title spacing if specified
        if preset.axis_title_spacing is not None:
            self.apply_axis_title_spacing(preset.axis_title_spacing)

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
        self._watermark_config = None

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

        This patches alt.Chart.save to automatically add watermarks before saving.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config
        self._watermark_config = config

        # Patch Chart.save to add watermark automatically
        try:
            import altair as alt
            
            # Save original save method if not already saved
            if not hasattr(alt.Chart, '_original_save'):
                alt.Chart._original_save = alt.Chart.save
            
            adapter_self = self
            original_save = alt.Chart._original_save
            
            def save_with_watermark(self, fp, *args, **kwargs):
                """Save chart with watermark added."""
                if adapter_self._watermark_config is not None:
                    # Add watermark to chart
                    chart_with_watermark = adapter_self._add_watermark_to_chart_internal(
                        self, adapter_self._watermark_config
                    )
                    # Call original save with the watermarked chart
                    return original_save(chart_with_watermark, fp, *args, **kwargs)
                else:
                    return original_save(self, fp, *args, **kwargs)
            
            alt.Chart.save = save_with_watermark
            
        except Exception:
            pass

    def _add_watermark_to_chart_internal(self, chart, config: "WatermarkConfig"):
        """
        Add a watermark to a specific Altair chart.

        This method must be called explicitly for each chart since Altair
        uses a declarative grammar that doesn't support automatic modification.

        Args:
            chart: The Altair chart to add watermark to.
            config: The WatermarkConfig object. If None, uses stored config.

        Returns:
            The chart with watermark added (as a layered chart).

        Example:
            >>> import sane_figs
            >>> import altair as alt
            >>> import pandas as pd
            >>> 
            >>> sane_figs.setup(mode='article', watermark='© My Lab')
            >>> 
            >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
            >>> chart = alt.Chart(df).mark_line().encode(x='x', y='y')
            >>> 
            >>> # Add watermark to chart
            >>> chart_with_watermark = sane_figs.get_adapter('altair').add_watermark_to_chart(chart)
            >>> chart_with_watermark.save('chart.json')
        """
        if config is None:
            config = self._watermark_config

        if config is None:
            return chart

        if config.text is not None:
            return self._add_text_watermark(chart, config)
        elif config.image_path is not None:
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

        # Get position in paper coordinates (0-1)
        x, y, align, baseline = self._get_watermark_position(config)

        # Create a DataFrame for the watermark text
        watermark_data = pd.DataFrame({
            'text': [config.text],
            'x': [x],
            'y': [y],
        })

        # Create watermark layer using encode() for position
        watermark = (
            self._altair.Chart(watermark_data)
            .mark_text(
                fontSize=config.font_size,
                font=config.font_family,
                fontWeight=config.font_weight,
                color=config.font_color,
                opacity=config.opacity,
                align=align,
                baseline=baseline,
            )
            .encode(
                x=self._altair.X('x:Q', axis=None, scale=self._altair.Scale(domain=[0, 1])),
                y=self._altair.Y('y:Q', axis=None, scale=self._altair.Scale(domain=[0, 1])),
                text='text',
            )
        )

        # Layer the watermark on top of the chart
        return self._altair.layer(chart, watermark).resolve_scale(
            x='independent',
            y='independent',
        )

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
        import base64
        from pathlib import Path

        # Get position in paper coordinates (0-1)
        x, y, align, baseline = self._get_watermark_position(config)

        # Convert image to base64 for embedding
        image_path = Path(config.image_path)
        if not image_path.exists():
            return chart

        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Determine MIME type
        suffix = image_path.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        }
        mime_type = mime_types.get(suffix, 'image/png')
        
        # Create base64 URL
        base64_data = base64.b64encode(image_data).decode('utf-8')
        url = f"data:{mime_type};base64,{base64_data}"

        # Create a DataFrame for the watermark image
        watermark_data = pd.DataFrame({
            'url': [url],
            'x': [x],
            'y': [y],
        })

        # Create watermark image layer
        watermark = (
            self._altair.Chart(watermark_data)
            .mark_image(
                width=int(config.scale * 300),  # Approximate width in pixels
                height=int(config.scale * 300),
                opacity=config.opacity,
            )
            .encode(
                x=self._altair.X('x:Q', axis=None, scale=self._altair.Scale(domain=[0, 1])),
                y=self._altair.Y('y:Q', axis=None, scale=self._altair.Scale(domain=[0, 1])),
                url='url',
            )
        )

        # Layer the watermark on top of the chart
        return self._altair.layer(chart, watermark).resolve_scale(
            x='independent',
            y='independent',
        )

    def _get_watermark_position(self, config: "WatermarkConfig") -> tuple[float, float, str, str]:
        """
        Get the position for a watermark in paper coordinates.

        Args:
            config: The WatermarkConfig object.

        Returns:
            Tuple of (x, y, align, baseline) in paper coordinates (0-1).
        """
        margin_x = config.margin[0]
        margin_y = config.margin[1]

        if config.position == "top-left":
            x, y = margin_x, 1 - margin_y
            align, baseline = "left", "top"
        elif config.position == "top-right":
            x, y = 1 - margin_x, 1 - margin_y
            align, baseline = "right", "top"
        elif config.position == "bottom-left":
            x, y = margin_x, margin_y
            align, baseline = "left", "bottom"
        elif config.position == "bottom-right":
            x, y = 1 - margin_x, margin_y
            align, baseline = "right", "bottom"
        elif config.position == "center":
            x, y = 0.5, 0.5
            align, baseline = "center", "middle"
        else:
            x, y = 1 - margin_x, margin_y
            align, baseline = "right", "bottom"

        return (x, y, align, baseline)

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
            # use screen_dpi for pixel dimensions rather than print DPI.
            # Fonts still scale with print dpi to maintain physical size intent.
            screen_dpi = preset.get_display_dpi()

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
                        "size": (preset.marker_size * dpi_scale) ** 2,
                    },
                    "point": {
                        "size": (preset.marker_size * dpi_scale) ** 2,
                    },
                    "circle": {
                        "size": (preset.marker_size * dpi_scale) ** 2,
                    },
                    "square": {
                        "size": (preset.marker_size * dpi_scale) ** 2,
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

    def apply_title_config(self, config: "TitleConfig") -> None:
        """
        Apply title alignment configuration to Altair.

        Args:
            config: The TitleConfig object containing title alignment settings.
        """
        if not self.is_available():
            return

        try:
            alignment_map = {
                "left": "left",
                "center": "center",
                "right": "right",
            }
            anchor = alignment_map.get(config.alignment, "center")

            if self._base_theme_config is not None:
                self._base_theme_config["config"]["title"]["anchor"] = anchor
                self._update_altair_theme()
        except Exception:
            pass

    def apply_legend_config(self, config: "LegendConfig") -> None:
        """
        Apply legend position configuration to Altair.

        Args:
            config: The LegendConfig object containing legend position settings.
        """
        if not self.is_available():
            return

        try:
            position_map = {
                "inside_upper_right": {"orient": "top-right"},
                "inside_upper_left": {"orient": "top-left"},
                "inside_lower_right": {"orient": "bottom-right"},
                "inside_lower_left": {"orient": "bottom-left"},
                "inside_center": {"orient": "none", "x": 0.5, "y": 0.5},
                "outside_right": {"orient": "right"},
                "outside_left": {"orient": "left"},
                "outside_top": {"orient": "top"},
                "outside_bottom": {"orient": "bottom"},
            }

            pos = position_map.get(config.position, position_map["inside_upper_right"])

            if self._base_theme_config is not None:
                legend_config = self._base_theme_config["config"]["legend"]
                # Remove old position keys before applying new ones
                for key in ("orient", "x", "y"):
                    legend_config.pop(key, None)
                legend_config.update(pos)
                # Apply offsets only when x/y are set (orient-based positions
                # don't use explicit coordinates, so offsets are not applied)
                if config.x_offset != 0 and "x" in legend_config:
                    legend_config["x"] = legend_config["x"] + config.x_offset
                if config.y_offset != 0 and "y" in legend_config:
                    legend_config["y"] = legend_config["y"] + config.y_offset
                self._update_altair_theme()
        except Exception:
            pass

    def apply_axis_title_spacing(self, config: "AxisTitleSpacingConfig") -> None:
        """
        Apply axis title spacing configuration to Altair.

        Args:
            config: The AxisTitleSpacingConfig object containing spacing settings.
        """
        if not self.is_available():
            return

        try:
            spacing_x = config.x_spacing * config.altair_multiplier
            spacing_y = config.y_spacing * config.altair_multiplier

            if self._base_theme_config is not None:
                axis_config = self._base_theme_config["config"]["axis"]
                axis_config["titlePadding"] = spacing_y
                axis_config["titleFontSize"] = (
                    axis_config.get("titleFontSize", 12) + spacing_x * 0.1
                )
                self._update_altair_theme()
        except Exception:
            pass

    def _update_altair_theme(self) -> None:
        """Update the Altair theme with the current base theme config."""
        try:

            def updated_theme():
                return self._base_theme_config

            self._altair.themes.register("sane_figs", updated_theme)
            self._altair.themes.enable("sane_figs")
            self._current_theme = updated_theme
        except Exception:
            pass
