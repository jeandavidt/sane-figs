"""Matplotlib adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig

from sane_figs.adapters.base import BaseAdapter


class MatplotlibAdapter(BaseAdapter):
    """
    Adapter for Matplotlib plotting library.

    This adapter applies publication-ready styling to Matplotlib figures
    with version-specific API handling.
    """

    # Version-specific handlers
    VERSION_HANDLERS = {
        (3, 5, 0): "_handle_v3_5_plus",
        (3, 0, 0): "_handle_v3_0_plus",
        (2, 0, 0): "_handle_v2_0_plus",
    }

    def __init__(self) -> None:
        """Initialize the Matplotlib adapter."""
        super().__init__("matplotlib")
        self._matplotlib = None
        self._pyplot = None
        self._original_rcparams = None
        self._watermark_config = None
        self._original_savefig = None

    def _import_matplotlib(self) -> bool:
        """
        Import matplotlib and pyplot.

        Returns:
            True if import was successful, False otherwise.
        """
        try:
            import matplotlib as mpl
            import matplotlib.pyplot as plt

            self._matplotlib = mpl
            self._pyplot = plt
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check if Matplotlib is available for use.

        Returns:
            True if Matplotlib is installed and can be used, False otherwise.
        """
        if self._matplotlib is None:
            return self._import_matplotlib()
        return True

    def get_version(self) -> str | None:
        """
        Get the version of the installed Matplotlib.

        Returns:
            Version string or None if Matplotlib is not installed.
        """
        if not self.is_available():
            return None
        return self._matplotlib.__version__

    def apply_style(self, preset: "Preset") -> None:
        """
        Apply publication-ready styling to Matplotlib.

        Args:
            preset: The Preset object containing styling configuration.
        """
        if not self.is_available():
            return

        # Save original rcParams
        self._original_rcparams = dict(self._matplotlib.rcParams)

        # Configure rcParams based on preset
        self._configure_rcparams(preset)

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
        Reset Matplotlib styling to its original state.
        """
        if not self.is_available():
            return

        # Restore original rcParams
        if self._original_rcparams is not None:
            self._matplotlib.rcParams.update(self._original_rcparams)

        # Restore original savefig if we patched it
        if self._original_savefig is not None:
            self._pyplot.savefig = self._original_savefig
            self._original_savefig = None

        self._watermark_config = None

    def apply_colorway(self, colorway: "Colorway") -> None:
        """
        Apply a colorway to Matplotlib.

        Args:
            colorway: The Colorway object to apply.
        """
        if not self.is_available():
            return

        # Set the color cycle to the categorical colors
        self._matplotlib.rcParams["axes.prop_cycle"] = self._matplotlib.cycler(
            "color", colorway.categorical
        )

    def add_watermark(self, config: "WatermarkConfig") -> None:
        """
        Add a watermark to Matplotlib figures.

        This patches plt.savefig to automatically add watermarks before saving.

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
            fig = self._pyplot.gcf()

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

    def _configure_rcparams(self, preset: "Preset") -> None:
        """
        Configure Matplotlib rcParams based on preset.

        Args:
            preset: The Preset object containing styling configuration.
        """
        # Figure settings
        self._matplotlib.rcParams["figure.figsize"] = preset.figure_size
        self._matplotlib.rcParams["figure.dpi"] = preset.dpi
        self._matplotlib.rcParams["savefig.dpi"] = preset.dpi
        self._matplotlib.rcParams["savefig.bbox"] = "tight"

        # Font settings
        if preset.mode == "latex":
            # Simulate LaTeX without requiring TeX installation
            self._matplotlib.rcParams["font.family"] = "serif"
            self._matplotlib.rcParams["mathtext.fontset"] = "cm"
            self._matplotlib.rcParams["font.serif"] = [
                "cmr10",
                "Computer Modern Serif",
                "DejaVu Serif",
            ]
        else:
            self._matplotlib.rcParams["font.family"] = preset.font_family

        self._matplotlib.rcParams["font.size"] = preset.font_size.get("label", 12.0)

        # Title
        self._matplotlib.rcParams["axes.titlesize"] = preset.font_size.get("title", 14.0)
        self._matplotlib.rcParams["axes.titleweight"] = "bold"

        # Axis labels
        self._matplotlib.rcParams["axes.labelsize"] = preset.font_size.get("label", 12.0)
        self._matplotlib.rcParams["axes.labelweight"] = "normal"

        # Tick labels
        self._matplotlib.rcParams["xtick.labelsize"] = preset.font_size.get("tick", 10.0)
        self._matplotlib.rcParams["ytick.labelsize"] = preset.font_size.get("tick", 10.0)

        # Legend
        self._matplotlib.rcParams["legend.fontsize"] = preset.font_size.get("legend", 10.0)
        self._matplotlib.rcParams["legend.framealpha"] = 0.9
        self._matplotlib.rcParams["legend.edgecolor"] = "inherit"

        # Lines and markers
        self._matplotlib.rcParams["lines.linewidth"] = preset.line_width
        self._matplotlib.rcParams["lines.markersize"] = preset.marker_size

        # Grid
        self._matplotlib.rcParams["axes.grid"] = True
        self._matplotlib.rcParams["grid.alpha"] = 0.3
        self._matplotlib.rcParams["grid.linewidth"] = 0.5

        # Spines
        self._matplotlib.rcParams["axes.spines.top"] = False
        self._matplotlib.rcParams["axes.spines.right"] = False

        # Use LaTeX for text rendering if available (only if explicitly requested via separate config,
        # but here we are using 'latex' mode to simulate it without tex)
        self._matplotlib.rcParams["text.usetex"] = False

    def _handle_version_specifics(self) -> None:
        """Handle version-specific Matplotlib settings."""
        version = self.get_version_tuple()
        if version is None:
            return

        from sane_figs.utils.version_utils import parse_version

        # Find the appropriate handler for this version
        for min_version, handler_name in reversed(self.VERSION_HANDLERS.items()):
            if version >= min_version:
                handler = getattr(self, handler_name, None)
                if handler is not None:
                    handler()
                break

    def _handle_v3_5_plus(self) -> None:
        """Handle Matplotlib 3.5+ specific settings."""
        # Matplotlib 3.5+ has improved legend handling
        self._matplotlib.rcParams["legend.title_fontsize"] = self._matplotlib.rcParams[
            "legend.fontsize"
        ]

    def _handle_v3_0_plus(self) -> None:
        """Handle Matplotlib 3.0+ specific settings."""
        # Matplotlib 3.0+ has improved color handling
        self._matplotlib.rcParams["image.cmap"] = "viridis"

    def _handle_v2_0_plus(self) -> None:
        """Handle Matplotlib 2.0+ specific settings."""
        # Matplotlib 2.0+ has improved default styles
        pass

    def apply_title_config(self, config: "TitleConfig") -> None:
        """
        Apply title alignment configuration to Matplotlib.

        Note: Matplotlib handles title alignment at the axes level via the ha parameter
        when calling ax.set_title(). This method sets the default behavior.

        Args:
            config: The TitleConfig object containing title alignment settings.
        """
        pass

    def apply_legend_config(self, config: "LegendConfig") -> None:
        """
        Apply legend position configuration to Matplotlib.

        Args:
            config: The LegendConfig object containing legend position settings.
        """
        if not self.is_available():
            return

        position_map = {
            "inside_upper_right": "upper right",
            "inside_upper_left": "upper left",
            "inside_lower_right": "lower right",
            "inside_lower_left": "lower left",
            "inside_center": "center",
        }

        loc = position_map.get(config.position, "upper right")

        self._matplotlib.rcParams["legend.loc"] = loc
        self._matplotlib.rcParams["legend.framealpha"] = 0.9
        self._matplotlib.rcParams["legend.edgecolor"] = "inherit"

        if config.alignment == "start":
            self._matplotlib.rcParams["legend.labelspacing"] = 0.5
        elif config.alignment == "end":
            self._matplotlib.rcParams["legend.labelspacing"] = 1.0

    def apply_axis_title_spacing(self, config: "AxisTitleSpacingConfig") -> None:
        """
        Apply axis title spacing configuration to Matplotlib.

        Matplotlib uses offset points for axis title spacing.
        The multiplier is applied to normalize across libraries.

        Args:
            config: The AxisTitleSpacingConfig object containing spacing settings.
        """
        if not self.is_available():
            return

        spacing = config.y_spacing * config.matplotlib_multiplier
        self._matplotlib.rcParams["axes.titlepad"] = spacing
