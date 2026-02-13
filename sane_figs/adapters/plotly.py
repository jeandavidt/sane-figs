"""Plotly adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import TitleConfig, LegendConfig, AxisTitleSpacingConfig

from sane_figs.adapters.base import BaseAdapter


class PlotlyAdapter(BaseAdapter):
    """
    Adapter for Plotly plotting library.

    This adapter applies publication-ready styling to Plotly figures
    with version-specific API handling.
    """

    # Version-specific handlers
    VERSION_HANDLERS = {
        (5, 0, 0): "_handle_v5_0_plus",
        (4, 14, 0): "_handle_v4_14_plus",
        (4, 0, 0): "_handle_v4_0_plus",
    }

    def __init__(self) -> None:
        """Initialize the Plotly adapter."""
        super().__init__("plotly")
        self._plotly = None
        self._original_template = None
        self._current_template = None
        self._watermark_config = None
        self._original_figure_init = None

    def _import_plotly(self) -> bool:
        """
        Import Plotly.

        Returns:
            True if import was successful, False otherwise.
        """
        try:
            import plotly

            self._plotly = plotly
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check if Plotly is available for use.

        Returns:
            True if Plotly is installed and can be used, False otherwise.
        """
        if self._plotly is None:
            return self._import_plotly()
        return True

    def get_version(self) -> str | None:
        """
        Get the version of the installed Plotly.

        Returns:
            Version string or None if Plotly is not installed.
        """
        if not self.is_available():
            return None
        return self._plotly.__version__

    def apply_style(self, preset: "Preset") -> None:
        """
        Apply publication-ready styling to Plotly.

        Args:
            preset: The Preset object containing styling configuration.
        """
        if not self.is_available():
            return

        # Save original template
        self._save_original_settings()

        # Configure Plotly template
        self._configure_template(preset)

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
        Reset Plotly styling to its original state.
        """
        if not self.is_available():
            return

        # Reset to original template
        if self._original_template is not None:
            try:
                import plotly.io as pio

                pio.templates.default = self._original_template
            except Exception:
                pass

        # Restore original Figure.__init__ if we patched it
        if self._original_figure_init is not None:
            try:
                import plotly.graph_objects as go

                go.Figure.__init__ = self._original_figure_init
                self._original_figure_init = None
            except Exception:
                pass

        # Clear stored state
        self._current_template = None
        self._watermark_config = None

    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to Plotly.

        Args:
            colorway: The Colorway object to apply.
        """
        if not self.is_available():
            return

        try:
            import plotly.io as pio

            # Update the current template with the colorway
            if self._current_template is not None:
                self._current_template.layout.colorway = colorway.categorical
                # Re-register the updated template
                pio.templates["sane_figs"] = self._current_template
                pio.templates.default = "sane_figs"
            else:
                # Fallback: create a new template if current_template doesn't exist
                template = pio.templates["plotly"]
                template.layout.colorway = colorway.categorical
                pio.templates["sane_figs"] = template
                pio.templates.default = "sane_figs"
        except Exception:
            pass

    def add_watermark(self, config: "WatermarkConfig") -> None:
        """
        Add a watermark to Plotly figures by patching Figure.__init__.

        This patches the Figure class to automatically add watermarks to all new figures.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config
        self._watermark_config = config

        # Patch the Figure class to add watermarks automatically
        try:
            import plotly.graph_objects as go

            # Save original __init__ if not already saved
            if self._original_figure_init is None:
                self._original_figure_init = go.Figure.__init__

            # Create a wrapper that adds watermark after initialization
            adapter_self = self
            original_init = self._original_figure_init

            def figure_init_with_watermark(fig_self, *args, **kwargs):
                """Initialize figure and add watermark."""
                # Call original __init__
                original_init(fig_self, *args, **kwargs)

                # Add watermark to the figure
                if adapter_self._watermark_config is not None:
                    adapter_self._add_watermark_to_figure(fig_self, adapter_self._watermark_config)

            # Patch Figure.__init__
            go.Figure.__init__ = figure_init_with_watermark

        except Exception as e:
            print(f"Warning: Failed to patch Plotly Figure class: {e}")
            import traceback
            traceback.print_exc()

    def _add_watermark_to_figure(self, fig, config: "WatermarkConfig") -> None:
        """
        Add watermark to a specific Plotly figure.

        Args:
            fig: The Plotly figure object.
            config: The WatermarkConfig object.
        """
        try:
            # Get position for watermark
            x, y, xanchor, yanchor = self._get_watermark_position(config)

            if config.text is not None:
                # Create text annotation
                watermark_annotation = dict(
                    name="watermark",
                    text=config.text,
                    textangle=0,
                    opacity=config.opacity,
                    font=dict(
                        family=config.font_family,
                        size=config.font_size,
                        color=config.font_color,
                    ),
                    xref="paper",
                    yref="paper",
                    x=x,
                    y=y,
                    xanchor=xanchor,
                    yanchor=yanchor,
                    showarrow=False,
                )

                # Add annotation to figure
                fig.add_annotation(watermark_annotation)

            elif config.image_path is not None:
                # Convert image to base64 data URI for Plotly
                import base64
                from pathlib import Path

                image_path = Path(config.image_path)
                if not image_path.exists():
                    return

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

                # Create base64 data URI
                base64_data = base64.b64encode(image_data).decode('utf-8')
                data_uri = f"data:{mime_type};base64,{base64_data}"

                # Add image to figure
                fig.add_layout_image(
                    source=data_uri,
                    xref="paper",
                    yref="paper",
                    x=x,
                    y=y,
                    sizex=config.scale,
                    sizey=config.scale,
                    xanchor=xanchor,
                    yanchor=yanchor,
                    sizing="contain",
                    opacity=config.opacity,
                    layer="above",
                )

        except Exception as e:
            print(f"Warning: Failed to add watermark to figure: {e}")
            import traceback
            traceback.print_exc()

    def _get_watermark_position(self, config: "WatermarkConfig") -> tuple[float, float, str, str]:
        """
        Get the position for a watermark in paper coordinates.

        Args:
            config: The WatermarkConfig object.

        Returns:
            Tuple of (x, y, xanchor, yanchor) in paper coordinates (0-1).
        """
        margin_x = config.margin[0]
        margin_y = config.margin[1]

        if config.position == "top-left":
            x, y = margin_x, 1 - margin_y
            xanchor, yanchor = "left", "top"
        elif config.position == "top-right":
            x, y = 1 - margin_x, 1 - margin_y
            xanchor, yanchor = "right", "top"
        elif config.position == "bottom-left":
            x, y = margin_x, margin_y
            xanchor, yanchor = "left", "bottom"
        elif config.position == "bottom-right":
            x, y = 1 - margin_x, margin_y
            xanchor, yanchor = "right", "bottom"
        elif config.position == "center":
            x, y = 0.5, 0.5
            xanchor, yanchor = "center", "middle"
        else:
            x, y = 1 - margin_x, margin_y
            xanchor, yanchor = "right", "bottom"

        return (x, y, xanchor, yanchor)

    def _save_original_settings(self) -> None:
        """Save the original Plotly settings."""
        try:
            import plotly.io as pio

            self._original_template = pio.templates.default
        except Exception:
            self._original_template = "plotly"

    def _configure_template(self, preset: "Preset") -> None:
        """
        Configure Plotly template based on preset.

        Args:
            preset: The Preset object containing styling configuration.
        """
        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            # For HTML/browser output Plotly uses CSS pixels, not print inches.
            # Scale figure_size (inches) by 150 px/in for a screen-friendly size.
            # Scale font sizes from points using 96/72 (1 pt → CSS px).
            screen_px_per_inch = 150
            dpi_scale = 96 / 72.0  # 1 pt → CSS px at standard screen resolution

            # Grid and Spines settings (mimic Matplotlib)
            grid_color = "rgba(0,0,0,0.1)"  # Light gray with transparency
            axis_line_color = "black"

            # Create layout dictionary
            layout_dict = dict(
                # Fixed screen-friendly pixel dimensions
                width=int(preset.figure_size[0] * screen_px_per_inch),
                height=int(preset.figure_size[1] * screen_px_per_inch),
                font=dict(
                    family=preset.font_family,
                    size=preset.font_size.get("label", 12) * dpi_scale,
                ),
                # Title
                title=dict(font=dict(size=preset.font_size.get("title", 14) * dpi_scale)),
                # Axis labels and ticks
                xaxis=dict(
                    title=dict(font=dict(size=preset.font_size.get("label", 12) * dpi_scale)),
                    tickfont=dict(size=preset.font_size.get("tick", 10) * dpi_scale),
                    # Grid
                    showgrid=True,
                    gridcolor=grid_color,
                    gridwidth=0.5 * dpi_scale,
                    # Spines (Axis Lines)
                    showline=True,
                    linecolor=axis_line_color,
                    linewidth=0.8 * dpi_scale,
                    # Mirror (off)
                    mirror=False,
                    # Ticks
                    ticks="outside",
                    ticklen=4 * dpi_scale,
                    tickcolor=axis_line_color,
                    nticks=6,
                ),
                yaxis=dict(
                    title=dict(font=dict(size=preset.font_size.get("label", 12) * dpi_scale)),
                    tickfont=dict(size=preset.font_size.get("tick", 10) * dpi_scale),
                    # Grid
                    showgrid=True,
                    gridcolor=grid_color,
                    gridwidth=0.5 * dpi_scale,
                    # Spines (Axis Lines)
                    showline=True,
                    linecolor=axis_line_color,
                    linewidth=0.8 * dpi_scale,
                    # Mirror (off)
                    mirror=False,
                    # Ticks
                    ticks="outside",
                    ticklen=4 * dpi_scale,
                    tickcolor=axis_line_color,
                    nticks=6,
                ),
                # Legend
                legend=dict(font=dict(size=preset.font_size.get("legend", 10) * dpi_scale)),
                # Colorway
                colorway=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            )

            # Create the Template object with explicit layout
            template = go.layout.Template(layout=layout_dict)

            # Set trace defaults
            template.data.scatter = [
                go.Scatter(
                    line=dict(width=preset.line_width * dpi_scale),
                    marker=dict(size=preset.marker_size * dpi_scale),
                )
            ]

            # Store the template for later modification (e.g., colorway)
            self._current_template = template

            # Register and apply template
            pio.templates["sane_figs"] = template
            pio.templates.default = "sane_figs"
        except Exception as e:
            print(f"Error configuring Plotly template: {e}")
            pass

    def _handle_version_specifics(self) -> None:
        """Handle version-specific Plotly settings."""
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
        """Handle Plotly 5.0+ specific settings."""
        # Plotly 5.0+ has improved template handling
        pass

    def _handle_v4_14_plus(self) -> None:
        """Handle Plotly 4.14+ specific settings."""
        # Plotly 4.14+ has improved color handling
        pass

    def _handle_v4_0_plus(self) -> None:
        """Handle Plotly 4.0+ specific settings."""
        # Plotly 4.0+ has improved default templates
        pass

    def apply_title_config(self, config: "TitleConfig") -> None:
        """
        Apply title alignment configuration to Plotly.

        Args:
            config: The TitleConfig object containing title alignment settings.
        """
        if not self.is_available():
            return

        try:
            import plotly.io as pio

            alignment_map = {
                "left": "left",
                "center": "center",
                "right": "right",
            }
            xanchor = alignment_map.get(config.alignment, "center")

            if self._current_template is not None:
                self._current_template.layout.title.xanchor = xanchor
                pio.templates["sane_figs"] = self._current_template
                pio.templates.default = "sane_figs"
        except Exception:
            pass

    def apply_legend_config(self, config: "LegendConfig") -> None:
        """
        Apply legend position configuration to Plotly.

        Args:
            config: The LegendConfig object containing legend position settings.
        """
        if not self.is_available():
            return

        try:
            import plotly.io as pio

            position_map = {
                "inside_upper_right": {"x": 0.98, "xanchor": "right", "y": 0.98, "yanchor": "top"},
                "inside_upper_left": {"x": 0.02, "xanchor": "left", "y": 0.98, "yanchor": "top"},
                "inside_lower_right": {
                    "x": 0.98,
                    "xanchor": "right",
                    "y": 0.02,
                    "yanchor": "bottom",
                },
                "inside_lower_left": {"x": 0.02, "xanchor": "left", "y": 0.02, "yanchor": "bottom"},
                "inside_center": {"x": 0.5, "xanchor": "center", "y": 0.5, "yanchor": "middle"},
                "outside_right": {"x": 1.02, "xanchor": "left", "y": 1.0, "yanchor": "top"},
                "outside_left": {"x": -0.02, "xanchor": "right", "y": 1.0, "yanchor": "top"},
                "outside_top": {"x": 0.5, "xanchor": "center", "y": 1.02, "yanchor": "bottom"},
                "outside_bottom": {"x": 0.5, "xanchor": "center", "y": -0.02, "yanchor": "top"},
            }

            pos = position_map.get(config.position, position_map["inside_upper_right"])

            if self._current_template is not None:
                legend_config = self._current_template.layout.legend
                legend_config.x = pos["x"] + config.x_offset
                legend_config.xanchor = pos["xanchor"]
                legend_config.y = pos["y"] + config.y_offset
                legend_config.yanchor = pos["yanchor"]

                if config.alignment == "start":
                    legend_config.x = 1.02
                    legend_config.xanchor = "right"
                elif config.alignment == "end":
                    legend_config.x = 1.02
                    legend_config.xanchor = "left"

                pio.templates["sane_figs"] = self._current_template
                pio.templates.default = "sane_figs"
        except Exception:
            pass

    def apply_axis_title_spacing(self, config: "AxisTitleSpacingConfig") -> None:
        """
        Apply axis title spacing configuration to Plotly.

        Plotly uses different spacing units than Matplotlib. We apply a multiplier
        to normalize the spacing to match Matplotlib's visual appearance.

        Args:
            config: The AxisTitleSpacingConfig object containing spacing settings.
        """
        if not self.is_available():
            return

        try:
            import plotly.io as pio

            spacing_x = config.x_spacing * config.plotly_multiplier
            spacing_y = config.y_spacing * config.plotly_multiplier

            if self._current_template is not None:
                self._current_template.layout.xaxis.title.standoff = spacing_x
                self._current_template.layout.yaxis.title.standoff = spacing_y
                pio.templates["sane_figs"] = self._current_template
                pio.templates.default = "sane_figs"
        except Exception:
            pass
