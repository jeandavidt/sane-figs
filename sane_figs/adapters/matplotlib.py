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

        Note: This sets up the watermark configuration. The actual watermark
        is added when a figure is created.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Store watermark config for use when figures are created
        self._watermark_config = config

        # Register a callback to add watermark to new figures
        original_figure = self._pyplot.Figure

        def figure_with_watermark(*args, **kwargs):
            fig = original_figure(*args, **kwargs)
            self._add_watermark_to_figure(fig, config)
            return fig

        self._pyplot.Figure = figure_with_watermark

    def _add_watermark_to_figure(self, fig, config: "WatermarkConfig") -> None:
        """
        Add a watermark to a specific figure.

        Args:
            fig: The Matplotlib figure.
            config: The WatermarkConfig object.
        """
        from PIL import Image

        fig_width, fig_height = fig.get_size_inches()
        dpi = fig.dpi
        fig_width_px = fig_width * dpi
        fig_height_px = fig_height * dpi

        if config.image_path is not None:
            # Image watermark
            try:
                img = Image.open(config.image_path)
                img_width = int(fig_width_px * config.scale)
                img_height = int(img_width * (img.height / img.width))

                # Resize image
                img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)

                # Calculate position
                from sane_figs.styling.watermarks import get_watermark_position

                x, y = get_watermark_position(
                    config.position,
                    fig_width_px,
                    fig_height_px,
                    img_width,
                    img_height,
                    config.margin[0],
                    config.margin[1],
                )

                # Add image to figure
                from matplotlib.offsetbox import OffsetImage, AnnotationBbox

                imagebox = OffsetImage(img, zoom=1.0, alpha=config.opacity)
                ab = AnnotationBbox(
                    imagebox, (x / dpi, y / dpi), frameon=False, zorder=100
                )
                fig.add_artist(ab)
            except Exception:
                # If image loading fails, fall back to text watermark
                if config.text is not None:
                    self._add_text_watermark(fig, config, fig_width_px, fig_height_px)

        elif config.text is not None:
            # Text watermark
            self._add_text_watermark(fig, config, fig_width_px, fig_height_px)

    def _add_text_watermark(self, fig, config: "WatermarkConfig", fig_width_px: float, fig_height_px: float) -> None:
        """
        Add a text watermark to a figure.

        Args:
            fig: The Matplotlib figure.
            config: The WatermarkConfig object.
            fig_width_px: Figure width in pixels.
            fig_height_px: Figure height in pixels.
        """
        from sane_figs.styling.watermarks import get_watermark_position

        # Estimate text size (rough approximation)
        font_size = config.font_size
        text_width = len(config.text) * font_size * 0.6
        text_height = font_size * 1.2

        # Calculate position
        x, y = get_watermark_position(
            config.position,
            fig_width_px,
            fig_height_px,
            text_width,
            text_height,
            config.margin[0],
            config.margin[1],
        )

        # Convert to figure coordinates
        x_fig = x / fig.dpi
        y_fig = y / fig.dpi

        # Add text annotation
        fig.text(
            x_fig,
            y_fig,
            config.text,
            fontsize=font_size,
            fontfamily=config.font_family,
            fontweight=config.font_weight,
            color=config.font_color,
            alpha=config.opacity,
            ha="left",
            va="bottom",
            zorder=100,
        )

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
            self._matplotlib.rcParams["font.serif"] = ["cmr10", "Computer Modern Serif", "DejaVu Serif"]
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
