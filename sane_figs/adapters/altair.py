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
        (6, 0, 0): "_handle_v6_0_plus",
        (5, 0, 0): "_handle_v5_0_plus",
        (4, 2, 0): "_handle_v4_2_plus",
        (3, 0, 0): "_handle_v3_0_plus",
    }

    # Raster file extensions that need print-DPI scale factor on export
    _RASTER_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"})

    def __init__(self) -> None:
        """Initialize the Altair adapter."""
        super().__init__("altair")
        self._altair = None
        self._original_theme = None
        self._current_theme = None
        self._theme_fn = None  # Single stable theme function
        self._base_theme_config = None  # Store the base theme config to avoid recursion
        self._watermark_config = None
        self._current_colorway = None  # Store current colorway to persist through theme updates
        self._preset = None  # Store preset for export-time DPI calculations
        self._original_chart_init = None  # For patching alt.Chart.__init__
        self._screen_dimensions = (200, 200)  # Updated in _patch_chart_init

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

        # Patch Chart.save so raster exports get the correct print-DPI
        # scale factor (this is idempotent if add_watermark already patched)
        self._patch_chart_save()

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

        # Restore original Chart.save if we patched it
        try:
            import altair as alt

            if hasattr(alt.Chart, "_original_save"):
                alt.Chart.save = alt.Chart._original_save
                del alt.Chart._original_save
        except Exception:
            pass

        # Restore original Chart.__init__ if we patched it
        if self._original_chart_init is not None:
            try:
                import altair as alt

                alt.Chart.__init__ = self._original_chart_init
                self._original_chart_init = None
            except Exception:
                pass

        # Clear stored state
        self._current_theme = None
        self._theme_fn = None
        self._base_theme_config = None
        self._current_colorway = None
        self._watermark_config = None
        self._preset = None

    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to Altair.

        Args:
            colorway: The Colorway object to apply.
        """
        if not self.is_available():
            return

        try:
            # Store the colorway so it persists through theme updates
            self._current_colorway = colorway

            # Mutate the shared config dict in place.  The single stable theme
            # function registered in _configure_theme always reads this dict, so
            # no re-registration is needed.
            if self._base_theme_config is not None:
                self._base_theme_config["config"]["range"] = {
                    "category": colorway.categorical,
                    "diverging": colorway.diverging,
                    "ordinal": colorway.qualitative,
                }
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

        # _patch_chart_save handles both watermarks and export scaling
        self._patch_chart_save()

    def _patch_chart_save(self) -> None:
        """Patch ``alt.Chart.save`` to handle watermarks and raster export scaling.

        For raster formats (.png, .jpg, …) the patch injects a ``scale_factor``
        equal to ``print_dpi / screen_dpi`` so the exported image has the same
        pixel dimensions and element sizes as Matplotlib's ``savefig`` output.
        The caller can still override ``scale_factor`` explicitly.
        """
        try:
            import altair as alt
            from pathlib import Path
            from sane_figs.utils.dpi_utils import get_export_scale_factor

            # Only patch once
            if hasattr(alt.TopLevelMixin, "_original_save"):
                return

            alt.TopLevelMixin._original_save = alt.TopLevelMixin.save

            adapter_self = self
            original_save = alt.TopLevelMixin._original_save

            # Patch to_dict globally to bypass validation for LayerChart in Altair 6
            # This is necessary because LayerChart validation incorrectly
            # flags 'mark' properties that are actually in valid locations.
            if not hasattr(alt.TopLevelMixin, "_original_to_dict"):
                alt.TopLevelMixin._original_to_dict = alt.TopLevelMixin.to_dict
                
                def patched_to_dict(self, *args, **kwargs):
                    # If it's a LayerChart, we force validate=False to avoid the buggy 
                    # "LayerChart has no parameter named 'mark'" error.
                    if isinstance(self, alt.LayerChart) and "validate" not in kwargs:
                        kwargs["validate"] = False
                    return alt.TopLevelMixin._original_to_dict(self, *args, **kwargs)

                alt.TopLevelMixin.to_dict = patched_to_dict

            def save_with_scaling(chart_self, fp, *args, **kwargs):
                """Save chart with optional watermark and print-DPI scaling."""
                target = chart_self

                # Add watermark if configured
                if adapter_self._watermark_config is not None:
                    target = adapter_self._add_watermark_to_chart_internal(
                        chart_self, adapter_self._watermark_config
                    )

                # Inject scale_factor for raster exports when not overridden
                if adapter_self._preset is not None:
                    fp_str = str(fp)
                    suffix = Path(fp_str).suffix.lower() if fp_str else ""
                    if suffix in AltairAdapter._RASTER_EXTENSIONS:
                        if "scale_factor" not in kwargs:
                            kwargs["scale_factor"] = get_export_scale_factor(
                                adapter_self._preset
                            )

                return original_save(target, fp, *args, **kwargs)

            alt.TopLevelMixin.save = save_with_scaling
            # Also patch alt.Chart.save just in case some versions don't use the mixin's implementation directly
            alt.Chart.save = save_with_scaling

        except Exception:
            pass

    def _patch_chart_init(self, width_px: int, height_px: int) -> None:
        """Patch ``alt.Chart.__init__`` to set spec-level width/height.

        ``config.view.width/height`` is only a Vega-Lite hint; embedding
        environments (Marimo, Jupyter) can override it with container sizing.
        Setting ``spec.width`` and ``spec.height`` directly takes precedence
        over all container/responsive overrides, ensuring a fixed canvas.
        """
        try:
            import altair as alt

            if self._original_chart_init is not None:
                return  # already patched

            self._original_chart_init = alt.Chart.__init__

            adapter_self = self
            original_init = self._original_chart_init

            def chart_init_with_fixed_size(chart_self, *args, **kwargs):
                original_init(chart_self, *args, **kwargs)
                if adapter_self._preset is None:
                    return
                try:
                    # Altair schema uses a sentinel Undefined for unset values.
                    # Only set if the user hasn't supplied explicit dimensions.
                    from altair.utils.schemapi import Undefined

                    w, h = adapter_self._screen_dimensions
                    if chart_self.width is Undefined:
                        chart_self.width = w
                    if chart_self.height is Undefined:
                        chart_self.height = h
                except Exception:
                    pass

            alt.Chart.__init__ = chart_init_with_fixed_size

            # Store dimensions so the closure can read updated values after
            # preset changes without needing to re-patch.
            self._screen_dimensions = (width_px, height_px)

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
            The chart with watermark added (as a layered chart), or the original
            chart if watermarking is not supported for its type.
        """
        if config is None:
            config = self._watermark_config

        if config is None:
            return chart

        # Defensive check: Faceted and Concatenated charts cannot be layered in Altair 6.
        # They must be layered BEFORE faceting/concatenating.
        # Since sane-figs adds watermarks at the very end (during save), we skip
        # them for these composite types to avoid TypeError: Faceted charts cannot be layered.
        import altair as alt
        if isinstance(chart, (alt.FacetChart, alt.ConcatChart, alt.HConcatChart, alt.VConcatChart)):
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

        All visual chrome (grid, spines, background, ticks) is read from
        ``preset.plot_style`` so that every preset renders identically.

        All visual properties (dimensions, fonts, line widths, markers) are
        scaled with a single factor derived from ``screen_dpi``.  This keeps
        the font-to-canvas ratio identical to what Matplotlib produces.

        When saving to a raster format the patched ``Chart.save`` multiplies
        the entire rendering by ``print_dpi / screen_dpi`` so that the
        resulting PNG matches Matplotlib's ``savefig`` output pixel-for-pixel.

        Args:
            preset: The Preset object containing styling configuration.
        """
        from sane_figs.utils.dpi_utils import get_screen_scale, get_screen_dimensions

        try:
            ps = preset.plot_style

            # Store preset for export-time DPI calculations
            self._preset = preset

            # Single consistent scale: screen_dpi / 72
            # 1 pt = 1/72 in; screen has screen_dpi px/in  →  1 pt = scale px
            scale = get_screen_scale(preset)
            width_px, height_px = get_screen_dimensions(preset)

            # Vega-Lite `size` for point marks = actual symbol area in sq-px
            # (πr² for a circle).  Matplotlib `markersize` is the DIAMETER in
            # points.  Convert: size = π/4 * (diameter_px)².
            import math as _math
            _marker_area = _math.pi / 4.0 * (preset.marker_size * scale) ** 2

            # Create the base theme config
            base_theme_config = {
                "config": {
                    # Use padding autosize so Vega-Lite adds space for axis
                    # labels, title, and ticks around the fixed plot area.
                    # "none" would clip all text outside the view boundary.
                    "autosize": "fit",
                    "background": ps.background_color,
                    "view": {
                        "width": width_px,
                        "height": height_px,
                        # Remove border around the chart (matches spines.top/right=False)
                        "stroke": "transparent",
                    },
                    "font": preset.font_family,
                    "title": {
                        "font": preset.font_family,
                        "fontSize": preset.font_size.get("title", 14) * scale,
                        "fontWeight": ps.title_weight,
                        "anchor": "middle",  # Center-aligned title (matches Matplotlib default)
                        "offset": 10 * scale,
                    },
                    "axis": {
                        "titleFont": preset.font_family,
                        "labelFont": preset.font_family,
                        "titleFontSize": preset.font_size.get("label", 12) * scale,
                        "labelFontSize": preset.font_size.get("tick", 10) * scale,
                        # Grid
                        "grid": ps.grid_visible,
                        "gridOpacity": ps.grid_opacity,
                        "gridWidth": ps.grid_width * scale,
                        "gridColor": ps.grid_color,
                        # Ticks
                        "tickCount": 5,
                        "ticks": True,
                        "tickWidth": 0.5 * scale,
                        "tickSize": ps.tick_length * scale,
                        "tickColor": ps.tick_color,
                        # Spines / domain
                        "domain": True,
                        "domainColor": ps.axis_line_color,
                        "domainWidth": ps.axis_line_width * scale,
                    },
                    "legend": {
                        "titleFont": preset.font_family,
                        "labelFont": preset.font_family,
                        "titleFontSize": preset.font_size.get("legend", 10) * scale,
                        "labelFontSize": preset.font_size.get("legend", 10) * scale,
                        "fillColor": ps.background_color,
                        "strokeColor": ps.legend_edge_color if ps.legend_edge_color != "inherit" else ps.axis_line_color,
                        "strokeWidth": ps.axis_line_width * scale,
                        "opacity": ps.legend_frame_opacity,
                        "padding": 6,  # Inner padding (px) between items and border
                    },
                    "header": {
                        "titleFont": preset.font_family,
                        "labelFont": preset.font_family,
                    },
                    "text": {
                        "font": preset.font_family,
                    },
                    "mark": {
                        "strokeWidth": preset.line_width * scale,
                        "size": _marker_area,
                        "filled": True,
                    },
                    "point": {
                        "size": _marker_area,
                        "filled": True,
                    },
                    "circle": {
                        "size": _marker_area,
                        "filled": True,
                    },
                    "square": {
                        "size": _marker_area,
                        "filled": True,
                    },
                }
            }

            # Store the base theme config (mutable dict).
            self._base_theme_config = base_theme_config

            # Register a single stable theme function that always reads the
            # current dict.  apply_colorway() and other mutators just update
            # the dict in place — no re-registration required.
            adapter_self = self

            def _sane_figs_theme():
                return adapter_self._base_theme_config

            self._theme_fn = _sane_figs_theme
            self._current_theme = _sane_figs_theme

            self._altair.themes.register("sane_figs", _sane_figs_theme)
            self._altair.themes.enable("sane_figs")

            # Patch alt.Chart.__init__ to set spec-level width/height so the
            # chart dimensions are fixed regardless of the embedding environment.
            self._patch_chart_init(width_px, height_px)
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

    def _handle_v6_0_plus(self) -> None:
        """Handle Altair 6.0+ specific settings."""
        # Altair 6.0+ has changed how Chart and LayerChart interact with TopLevelMixin
        pass

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
            # Vega-Lite title.anchor uses "start"/"middle"/"end", not "left"/"center"/"right"
            alignment_map = {
                "left": "start",
                "center": "middle",
                "right": "end",
            }
            anchor = alignment_map.get(config.alignment, "middle")

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
        """Ensure the colorway range is present in the shared config dict.

        The single stable theme function registered in _configure_theme always
        reads self._base_theme_config, so no re-registration is needed here.
        This method only preserves the colorway range when other callers
        (e.g., apply_title_config) modify the config dict.
        """
        try:
            if self._current_colorway is not None and "range" not in self._base_theme_config["config"]:
                self._base_theme_config["config"]["range"] = {
                    "category": self._current_colorway.categorical,
                    "diverging": self._current_colorway.diverging,
                    "ordinal": self._current_colorway.qualitative,
                }
        except Exception:
            pass
