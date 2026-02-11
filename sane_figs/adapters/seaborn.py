"""Seaborn adapter for sane-figs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway
    from sane_figs.styling.watermarks import WatermarkConfig

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

    def _import_seaborn(self) -> bool:
        """
        Import Seaborn.

        Returns:
            True if import was successful, False otherwise.
        """
        try:
            import seaborn as sns

            self._seaborn = sns
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

        Note: Seaborn uses Matplotlib under the hood, so we delegate
        watermark handling to the Matplotlib adapter.

        Args:
            config: The WatermarkConfig object containing watermark settings.
        """
        if not self.is_available():
            return

        # Seaborn uses Matplotlib, so we need to apply the watermark
        # through Matplotlib's figure creation
        try:
            import matplotlib.pyplot as plt

            # Store watermark config for use when figures are created
            self._watermark_config = config

            # Register a callback to add watermark to new figures
            original_figure = plt.Figure

            def figure_with_watermark(*args, **kwargs):
                fig = original_figure(*args, **kwargs)
                self._add_watermark_to_figure(fig, config)
                return fig

            plt.Figure = figure_with_watermark
        except Exception:
            pass

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
