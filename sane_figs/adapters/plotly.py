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
        self._original_write_image = None
        self._preset = None  # Store preset for export-time DPI calculations
        self._template_dimensions = None  # Store (width, height) for figure patching

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

        # Apply or clear watermark
        self.add_watermark(preset.watermark)

        # Patch write_image so raster exports get the correct print-DPI
        self._patch_write_image()

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

        # Restore original Figure.write_image if we patched it
        if self._original_write_image is not None:
            try:
                import plotly.graph_objects as go

                go.Figure.write_image = self._original_write_image
                self._original_write_image = None
            except Exception:
                pass

        # Clear stored state
        self._current_template = None
        self._watermark_config = None
        self._preset = None
        self._template_dimensions = None

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

        # Store watermark config - the patching is handled by _patch_figure_init
        # which is called from _configure_template
        self._watermark_config = config

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

        All visual chrome is read from ``preset.plot_style`` so every preset
        renders identically.

        All visual properties are scaled with a single factor derived from
        ``screen_dpi`` so that the font-to-canvas ratio matches Matplotlib.
        The patched ``write_image`` then multiplies the rendering by
        ``print_dpi / screen_dpi`` for raster exports.

        Args:
            preset: The Preset object containing styling configuration.
        """
        from sane_figs.utils.dpi_utils import get_screen_scale, get_screen_dimensions

        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            ps = preset.plot_style

            # Store preset for export-time DPI calculations
            self._preset = preset

            # Single consistent scale: screen_dpi / 72
            # 1 pt = 1/72 in; screen has screen_dpi px/in  →  1 pt = scale px
            scale = get_screen_scale(preset)
            width_px, height_px = get_screen_dimensions(preset)

            # Build a Plotly-compatible grid colour string from plot_style.
            # Plotly expects opacity baked into an rgba() value.
            grid_color = self._to_rgba(ps.grid_color, ps.grid_opacity)

            # Shared axis config driven by plot_style
            def _axis_config():
                return dict(
                    title=dict(font=dict(size=preset.font_size.get("label", 12) * scale)),
                    tickfont=dict(size=preset.font_size.get("tick", 10) * scale),
                    # Grid
                    showgrid=ps.grid_visible,
                    gridcolor=grid_color,
                    gridwidth=ps.grid_width * scale,
                    # Zero-line: disable to match matplotlib's default style
                    zeroline=False,
                    # Spines
                    showline=True,
                    linecolor=ps.axis_line_color,
                    linewidth=ps.axis_line_width * scale,
                    mirror=False,
                    # Ticks
                    ticks=ps.tick_direction if ps.tick_direction != "both" else "inside",
                    ticklen=ps.tick_length * scale,
                    tickcolor=ps.tick_color,
                    nticks=6,
                )

            # Compact margins in screen pixels (kaleido scales them along with
            # everything else when write_image(scale=…) is called).
            # Left: room for rotated y-axis label + widest tick number (~"-1.0")
            # Bottom: x-axis tick numbers + x-axis label row
            # Top: title row + a little breathing room
            # Right: small gap after the last tick
            _l = int(70 * scale)
            _b = int(50 * scale)
            _t = int(60 * scale)
            _r = int(20 * scale)

            layout_dict = dict(
                width=width_px,
                height=height_px,
                autosize=False,
                margin=dict(l=_l, r=_r, t=_t, b=_b, pad=0),
                font=dict(
                    family=preset.font_family,
                    size=preset.font_size.get("label", 12) * scale,
                ),
                paper_bgcolor=ps.background_color,
                plot_bgcolor=ps.background_color,
                title=dict(
                    font=dict(
                        size=preset.font_size.get("title", 14) * scale,
                        weight=ps.title_weight,
                    ),
                    # Center over the plot area, not the full figure (which would
                    # be off-center due to unequal left/right margins)
                    x=0.5,
                    xanchor="center",
                    xref="paper",
                ),
                xaxis=_axis_config(),
                yaxis=_axis_config(),
                legend=dict(
                    font=dict(size=preset.font_size.get("legend", 10) * scale),
                    bgcolor=ps.background_color,
                    bordercolor=(
                        ps.axis_line_color
                        if ps.legend_edge_color == "inherit"
                        else ps.legend_edge_color
                    ),
                    borderwidth=ps.axis_line_width * scale,
                    # Remove gap between trace groups so legend is compact like matplotlib
                    tracegroupgap=0,
                ),
                colorway=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            )

            template = go.layout.Template(layout=layout_dict)

            # Set trace defaults
            template.data.scatter = [
                go.Scatter(
                    line=dict(width=preset.line_width * scale),
                    marker=dict(size=preset.marker_size * scale),
                )
            ]

            self._current_template = template
            self._template_dimensions = (width_px, height_px)

            pio.templates["sane_figs"] = template
            pio.templates.default = "sane_figs"

            # Patch Figure.__init__ to apply template dimensions
            self._patch_figure_init()
        except Exception as e:
            print(f"Error configuring Plotly template: {e}")
            pass

    @staticmethod
    def _to_rgba(color: str, opacity: float) -> str:
        """Convert a named or hex colour + opacity to a Plotly ``rgba()`` string."""
        # Handle common named colours directly to avoid import overhead
        named = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "gray": (128, 128, 128),
            "grey": (128, 128, 128),
            "red": (255, 0, 0),
            "green": (0, 128, 0),
            "blue": (0, 0, 255),
        }
        low = color.lower().strip()
        if low in named:
            r, g, b = named[low]
            return f"rgba({r},{g},{b},{opacity})"
        if low.startswith("#") and len(low) in (4, 7):
            if len(low) == 4:
                r = int(low[1] * 2, 16)
                g = int(low[2] * 2, 16)
                b = int(low[3] * 2, 16)
            else:
                r = int(low[1:3], 16)
                g = int(low[3:5], 16)
                b = int(low[5:7], 16)
            return f"rgba({r},{g},{b},{opacity})"
        # Fallback: return as-is (e.g. already an rgba string)
        return color

    def _patch_write_image(self) -> None:
        """Patch ``Figure.write_image`` to apply print-DPI scaling.

        When the caller does not explicitly pass ``width``, ``height``, or
        ``scale``, this wrapper injects ``scale = print_dpi / screen_dpi``
        so the exported raster matches Matplotlib's ``savefig`` output.
        """
        try:
            import plotly.graph_objects as go
            from sane_figs.utils.dpi_utils import get_export_scale_factor

            if self._original_write_image is not None:
                return  # already patched

            self._original_write_image = go.Figure.write_image

            adapter_self = self
            original_write_image = self._original_write_image

            def write_image_with_scaling(fig_self, *args, **kwargs):
                """Write image with automatic print-DPI scaling."""
                if adapter_self._preset is not None:
                    # Only inject scale when the caller hasn't set any of
                    # width/height/scale, to avoid overriding explicit intent.
                    has_explicit_size = (
                        "width" in kwargs
                        or "height" in kwargs
                        or "scale" in kwargs
                    )
                    if not has_explicit_size:
                        kwargs["scale"] = get_export_scale_factor(
                            adapter_self._preset
                        )

                return original_write_image(fig_self, *args, **kwargs)

            go.Figure.write_image = write_image_with_scaling

        except Exception:
            pass

    def _patch_figure_init(self) -> None:
        """Patch ``Figure.__init__`` to apply template dimensions.

        Plotly templates can set width/height, but figures don't inherit these
        values - they remain None and Plotly uses responsive sizing. This patch
        ensures each figure gets the template's width/height applied.
        """
        try:
            import plotly.graph_objects as go

            if self._original_figure_init is not None:
                return  # already patched

            self._original_figure_init = go.Figure.__init__

            adapter_self = self
            original_init = self._original_figure_init

            def figure_init_with_dimensions(fig_self, *args, **kwargs):
                """Initialize figure and apply template dimensions."""
                # Call original __init__
                original_init(fig_self, *args, **kwargs)

                # Always enforce fixed dimensions and disable responsive sizing.
                # Template values don't propagate to Python layout objects at init
                # time, so we must set these explicitly on every figure.
                if adapter_self._template_dimensions is not None:
                    width, height = adapter_self._template_dimensions
                    fig_self.layout.width = width
                    fig_self.layout.height = height
                    fig_self.layout.autosize = False

                # Add watermark to the figure if configured
                if adapter_self._watermark_config is not None:
                    adapter_self._add_watermark_to_figure(fig_self, adapter_self._watermark_config)

            go.Figure.__init__ = figure_init_with_dimensions

        except Exception:
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

            # x position (0=left, 0.5=center, 1=right) in paper coordinates
            x_map = {"left": 0.0, "center": 0.5, "right": 1.0}
            xanchor_map = {"left": "left", "center": "center", "right": "right"}

            x_val = x_map.get(config.alignment, 0.5)
            xanchor = xanchor_map.get(config.alignment, "center")

            if self._current_template is not None:
                self._current_template.layout.title.x = x_val
                self._current_template.layout.title.xanchor = xanchor
                self._current_template.layout.title.xref = "paper"
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
