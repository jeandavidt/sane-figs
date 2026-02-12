"""Seaborn adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig
    from sane_figs.styling.layout import TitleConfig, LegendConfig, AxisTitleSpacingConfig

from sane_figs.adapters.base import BaseAdapter


class SeabornAdapter(BaseAdapter):
    """
    Adapter for Seaborn plotting library.

    This adapter applies publication-ready styling to Seaborn figures.
    Seaborn builds on Matplotlib, so this adapter works in conjunction
    with the Matplotlib adapter.
    """

    # Version-specific handlers
    VERSION_HANDLERS = {
        (0, 12, 0): "_handle_v0_12_plus",
        (0, 11, 0): "_handle_v0_11_plus",
        (0, 9, 0): "_handle_v0_9_plus",
    }

    def __init__(self) -> None:
        """Initialize the Seaborn adapter."""
        super().__init__("seaborn")
        self._seaborn = None
        self._original_theme = None
        self._original_context = None
        self._watermark_config = None
        self._original_savefig = None
        self._pyplot = None

    def _import_seaborn(self) -> bool:
        """
        Import Seaborn.

        Returns:
            True if import was successful, False otherwise.
        """
        try:
            import seaborn as sns
            import matplotlib.pyplot as plt

            self._seaborn = sns
            self._pyplot = plt
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check if Seaborn is available for use.

        Returns:
            True if Seaborn is installed and can be used, False otherwise.
        """
        if self._seaborn is None:
            return self._import_seaborn()
        return True

    def get_version(self) -> str | None:
        """
        Get the version of the installed Seaborn.

        Returns:
            Version string or None if Seaborn is not installed.
        """
        if not self.is_available():
            return None
        return self._seaborn.__version__

    def apply_style(self, preset: "Preset") -> None:
        """
        Apply publication-ready styling to Seaborn.

        Args:
            preset: The Preset object containing styling configuration.
        """
        if not self.is_available():
            return

        # Save original settings
        self._save_original_settings()

        # Configure Seaborn theme and context
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
        Reset Seaborn styling to its original state.
        """
        if not self.is_available():
            return

        # Reset to original theme
        if self._original_theme is not None:
            self._seaborn.set_theme(style=self._original_theme)

        # Reset to original context
        if self._original_context is not None:
            self._seaborn.set_context(self._original_context)

        # Reset color palette
        self._seaborn.set_palette(self._seaborn.color_palette())

        # Restore original savefig if we patched it
        if self._original_savefig is not None and self._pyplot is not None:
            self._pyplot.savefig = self._original_savefig
            self._original_savefig = None

        self._watermark_config = None

    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to Seaborn.

        Args:
            colorway: The Colorway object to apply.
        """
        if not self.is_available():
            return

        # Set the color palette to the categorical colors
        self._seaborn.set_palette(colorway.categorical)

    def add_watermark(self, config: "WatermarkConfig") -> None:
        """
        Add a watermark to Seaborn figures.

        Seaborn uses Matplotlib under the hood, so we patch plt.savefig
        to automatically add watermarks before saving.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config
        self._watermark_config = config

        # Save original savefig if not already saved
        if self._original_savefig is None:
            self._original_savefig = self._pyplot.savefig

        # Create a wrapped savefig that adds watermark
        adapter_self = self
        original_savefig = self._original_savefig

        def savefig_with_watermark(fname, **kwargs):
            """Save figure with watermark added."""
            # Get current figure
            fig = adapter_self._pyplot.gcf()
            
            # Add watermark to the figure
            if adapter_self._watermark_config is not None:
                adapter_self._add_watermark_to_figure(fig, adapter_self._watermark_config)
            
            # Call original savefig
            return original_savefig(fname, **kwargs)

        # Patch savefig
        self._pyplot.savefig = savefig_with_watermark

    def _add_watermark_to_figure(self, fig, config: "WatermarkConfig") -> None:
        """
        Add a watermark to a specific figure.

        Args:
            fig: The Matplotlib figure.
            config: The WatermarkConfig object.
        """
        if config.text is not None:
            self._add_text_watermark(fig, config)
        elif config.image_path is not None:
            self._add_image_watermark(fig, config)

    def _add_text_watermark(self, fig, config: "WatermarkConfig") -> None:
        """
        Add a text watermark to a figure using figure coordinates.

        Args:
            fig: The Matplotlib figure.
            config: The WatermarkConfig object.
        """
        # Calculate position in figure coordinates (0-1)
        x, y, ha, va = self._get_watermark_position(config)

        # Add text watermark using figure coordinates
        fig.text(
            x,
            y,
            config.text,
            transform=fig.transFigure,
            fontsize=config.font_size,
            fontfamily=config.font_family,
            fontweight=config.font_weight,
            color=config.font_color,
            alpha=config.opacity,
            ha=ha,
            va=va,
            zorder=1000,
        )

    def _add_image_watermark(self, fig, config: "WatermarkConfig") -> None:
        """
        Add an image watermark to a figure using axes overlay approach.

        This method adds the watermark as an inset axes, which works correctly
        with bbox_inches='tight' and other savefig options.

        Args:
            fig: The Matplotlib figure.
            config: The WatermarkConfig object.
        """
        try:
            from PIL import Image
            import numpy as np

            # Load image
            img = Image.open(config.image_path)

            # Convert to RGBA if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Apply opacity by modifying alpha channel
            if config.opacity < 1.0:
                # Get the alpha channel and multiply by opacity
                alpha = img.split()[-1]
                alpha = alpha.point(lambda p: int(p * config.opacity))
                img.putalpha(alpha)

            # Convert to numpy array
            img_array = np.array(img)

            # Get image aspect ratio
            img_aspect = img.width / img.height

            # Calculate watermark size in figure coordinates
            watermark_width = config.scale
            watermark_height = watermark_width / img_aspect

            # Calculate position in figure coordinates (0-1)
            margin_x = config.margin[0]
            margin_y = config.margin[1]

            if config.position == "top-left":
                x = margin_x
                y = 1 - margin_y - watermark_height
            elif config.position == "top-right":
                x = 1 - margin_x - watermark_width
                y = 1 - margin_y - watermark_height
            elif config.position == "bottom-left":
                x = margin_x
                y = margin_y
            elif config.position == "bottom-right":
                x = 1 - margin_x - watermark_width
                y = margin_y
            elif config.position == "center":
                x = (1 - watermark_width) / 2
                y = (1 - watermark_height) / 2
            else:
                x = 1 - margin_x - watermark_width
                y = margin_y

            # Add watermark as an inset axes
            # This approach works correctly with bbox_inches='tight'
            ax_watermark = fig.add_axes([x, y, watermark_width, watermark_height],
                                       zorder=1000)
            ax_watermark.imshow(img_array, aspect='auto')
            ax_watermark.axis('off')

        except Exception as e:
            # Print error for debugging but don't crash
            import traceback
            print(f"Warning: Image watermark failed: {e}")
            traceback.print_exc()
            # Don't fall back to text - just skip the watermark if it fails

    def _get_watermark_position(self, config: "WatermarkConfig") -> tuple[float, float, str, str]:
        """
        Get the position for a watermark in figure coordinates.

        Args:
            config: The WatermarkConfig object.

        Returns:
            Tuple of (x, y, horizontal_alignment, vertical_alignment) in figure coordinates (0-1).
        """
        margin_x = config.margin[0]
        margin_y = config.margin[1]

        if config.position == "top-left":
            x, y = margin_x, 1 - margin_y
            ha, va = "left", "top"
        elif config.position == "top-right":
            x, y = 1 - margin_x, 1 - margin_y
            ha, va = "right", "top"
        elif config.position == "bottom-left":
            x, y = margin_x, margin_y
            ha, va = "left", "bottom"
        elif config.position == "bottom-right":
            x, y = 1 - margin_x, margin_y
            ha, va = "right", "bottom"
        elif config.position == "center":
            x, y = 0.5, 0.5
            ha, va = "center", "center"
        else:
            x, y = 1 - margin_x, margin_y
            ha, va = "right", "bottom"

        return (x, y, ha, va)

    def _save_original_settings(self) -> None:
        """Save the original Seaborn settings."""
        # Get current theme
        try:
            # Seaborn 0.11+ has get_theme()
            if hasattr(self._seaborn, "get_theme"):
                self._original_theme = self._seaborn.get_theme()
            else:
                self._original_theme = "darkgrid"  # Default theme
        except Exception:
            self._original_theme = "darkgrid"

        # Get current context
        try:
            # Seaborn 0.8+ has plotting_context()
            self._original_context = "notebook"  # Default context
        except Exception:
            self._original_context = "notebook"

    def _configure_theme(self, preset: "Preset") -> None:
        """
        Configure Seaborn theme and context based on preset.

        Args:
            preset: The Preset object containing styling configuration.
        """
        # Set theme based on mode
        style = "whitegrid" if preset.mode == "article" else "darkgrid"

        # Set context based on mode
        context = "paper" if preset.mode == "article" else "talk"

        # Configure additional style parameters
        style_params = {
            "axes.labelsize": preset.font_size.get("label", 12.0),
            "xtick.labelsize": preset.font_size.get("tick", 10.0),
            "ytick.labelsize": preset.font_size.get("tick", 10.0),
            "legend.fontsize": preset.font_size.get("legend", 10.0),
            "axes.titlesize": preset.font_size.get("title", 14.0),
            "lines.linewidth": preset.line_width,
            "font.family": preset.font_family,
        }

        # Handle custom font families specifically for Seaborn/Matplotlib
        if preset.mode == "latex":
            style_params["font.family"] = "serif"
            style_params["mathtext.fontset"] = "cm"
            style_params["font.serif"] = ["cmr10", "Computer Modern Serif", "DejaVu Serif"]

        # Apply settings in a single call to avoid resetting
        self._seaborn.set_theme(style=style, context=context, rc=style_params)

    def _handle_version_specifics(self) -> None:
        """Handle version-specific Seaborn settings."""
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

    def _handle_v0_12_plus(self) -> None:
        """Handle Seaborn 0.12+ specific settings."""
        # Seaborn 0.12+ has improved theme handling
        pass

    def _handle_v0_11_plus(self) -> None:
        """Handle Seaborn 0.11+ specific settings."""
        # Seaborn 0.11+ introduced set_theme()
        pass

    def _handle_v0_9_plus(self) -> None:
        """Handle Seaborn 0.9+ specific settings."""
        # Seaborn 0.9+ has improved color palette handling
        pass

    def apply_title_config(self, config: "TitleConfig") -> None:
        """
        Apply title alignment configuration to Seaborn.

        Args:
            config: The TitleConfig object containing title alignment settings.
        """
        if not self.is_available():
            return

        alignment_map = {
            "left": "left",
            "center": "center",
            "right": "right",
        }
        ha = alignment_map.get(config.alignment, "center")

        import matplotlib as mpl

        mpl.rcParams["axes.titlealignment"] = ha

    def apply_legend_config(self, config: "LegendConfig") -> None:
        """
        Apply legend position configuration to Seaborn.

        Args:
            config: The LegendConfig object containing legend position settings.
        """
        if not self.is_available():
            return

        import matplotlib as mpl

        position_map = {
            "inside_upper_right": "upper right",
            "inside_upper_left": "upper left",
            "inside_lower_right": "lower right",
            "inside_lower_left": "lower left",
            "inside_center": "center",
        }

        loc = position_map.get(config.position, "upper right")
        mpl.rcParams["legend.loc"] = loc
        mpl.rcParams["legend.framealpha"] = 0.9
        mpl.rcParams["legend.edgecolor"] = "inherit"

    def apply_axis_title_spacing(self, config: "AxisTitleSpacingConfig") -> None:
        """
        Apply axis title spacing configuration to Seaborn.

        Args:
            config: The AxisTitleSpacingConfig object containing spacing settings.
        """
        if not self.is_available():
            return

        import matplotlib as mpl

        spacing = config.y_spacing * config.matplotlib_multiplier
        mpl.rcParams["axes.titlepad"] = spacing
