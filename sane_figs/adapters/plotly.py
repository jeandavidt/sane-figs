"""Plotly adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig

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
        self._original_figure = None

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

        # Restore original Figure class
        if self._original_figure is not None:
            try:
                import plotly.graph_objects as go

                go.Figure = self._original_figure
            except Exception:
                pass

        # Clear stored state
        self._current_template = None

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
        Add a watermark to Plotly figures.

        Note: This sets up the watermark configuration. The actual watermark
        is added when a figure is created.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config for use when figures are created
        self._watermark_config = config

        # Wrap go.Figure to automatically add watermarks
        try:
            import plotly.graph_objects as go

            # Save original Figure class
            if self._original_figure is None:
                self._original_figure = go.Figure

            def figure_with_watermark(*args, **kwargs):
                fig = self._original_figure(*args, **kwargs)
                self.add_watermark_to_figure(fig, config)
                return fig

            go.Figure = figure_with_watermark
        except Exception:
            pass

    def add_watermark_to_figure(self, fig, config: "WatermarkConfig") -> None:
        """
        Add a watermark to a specific Plotly figure.

        Args:
            fig: The Plotly figure.
            config: The WatermarkConfig object.
        """
        if config.text is not None:
            # Text watermark
            self._add_text_watermark(fig, config)
        elif config.image_path is not None:
            # Image watermark
            self._add_image_watermark(fig, config)

    def _add_text_watermark(self, fig, config: "WatermarkConfig") -> None:
        """
        Add a text watermark to a Plotly figure.

        Args:
            fig: The Plotly figure.
            config: The WatermarkConfig object.
        """
        # Calculate position
        x_ref, y_ref, x, y = self._get_watermark_position(config)

        # Add text annotation
        fig.add_annotation(
            text=config.text,
            xref=x_ref,
            yref=y_ref,
            x=x,
            y=y,
            showarrow=False,
            font=dict(
                size=config.font_size,
                family=config.font_family,
                color=config.font_color,
            ),
            opacity=config.opacity,
            xanchor="left",
            yanchor="bottom",
        )

    def _add_image_watermark(self, fig, config: "WatermarkConfig") -> None:
        """
        Add an image watermark to a Plotly figure.

        Args:
            fig: The Plotly figure.
            config: The WatermarkConfig object.
        """
        # Calculate position
        x_ref, y_ref, x, y = self._get_watermark_position(config)

        # Add image annotation
        fig.add_layout_image(
            dict(
                source=config.image_path,
                xref=x_ref,
                yref=y_ref,
                x=x,
                y=y,
                sizex=config.scale,
                sizey=config.scale,
                sizing="stretch",
                opacity=config.opacity,
                layer="above",
            )
        )

    def _get_watermark_position(self, config: "WatermarkConfig") -> tuple[str, str, float, float]:
        """
        Get the position for a watermark in Plotly coordinates.

        Args:
            config: The WatermarkConfig object.

        Returns:
            Tuple of (x_ref, y_ref, x, y) for Plotly annotation.
        """
        margin_x = config.margin[0]
        margin_y = config.margin[1]

        if config.position == "top-left":
            x_ref, y_ref = "paper", "paper"
            x, y = margin_x, 1 - margin_y
        elif config.position == "top-right":
            x_ref, y_ref = "paper", "paper"
            x, y = 1 - margin_x, 1 - margin_y
        elif config.position == "bottom-left":
            x_ref, y_ref = "paper", "paper"
            x, y = margin_x, margin_y
        elif config.position == "bottom-right":
            x_ref, y_ref = "paper", "paper"
            x, y = 1 - margin_x, margin_y
        elif config.position == "center":
            x_ref, y_ref = "paper", "paper"
            x, y = 0.5, 0.5
        else:
            x_ref, y_ref = "paper", "paper"
            x, y = 1 - margin_x, margin_y

        return (x_ref, y_ref, x, y)

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

            # Calculate DPI scale factor
            # Plotly uses pixels for font sizes, but presets use points
            # To match Matplotlib's physical size at the given DPI:
            # size_px = size_pt * (dpi / 72.0)
            dpi_scale = preset.dpi / 72.0

            # Grid and Spines settings (mimic Matplotlib)
            grid_color = "rgba(0,0,0,0.1)"  # Light gray with transparency
            axis_line_color = "black"

            # Create layout dictionary
            layout_dict = dict(
                # Figure settings
                width=int(preset.figure_size[0] * preset.dpi),
                height=int(preset.figure_size[1] * preset.dpi),
                font=dict(
                    family=preset.font_family,
                    size=preset.font_size.get("label", 12) * dpi_scale,
                ),
                
                # Title
                title=dict(
                    font=dict(size=preset.font_size.get("title", 14) * dpi_scale)
                ),
                
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
                legend=dict(
                    font=dict(size=preset.font_size.get("legend", 10) * dpi_scale)
                ),
                
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
