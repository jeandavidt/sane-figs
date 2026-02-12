# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "anthropic==0.79.0",
#     "marimo>=0.19.10",
#     "numpy==2.4.2",
#     "pandas==3.0.0",
#     "plotly==6.5.2",
#     "pydantic-ai-slim==1.58.0",
#     "sane-figs==0.1.0",
# ]
# ///

import marimo

__generated_with = "0.19.10"
app = marimo.App(width="medium")


@app.cell
async def install_packages():
    """Install WASM-safe packages only - NO matplotlib or seaborn."""
    import sys
    if "pyodide" in sys.modules:
        import micropip
        print("📦 Installing WASM-compatible dependencies...")
        # CRITICAL: Only install Plotly and Altair - NO matplotlib/seaborn
        await micropip.install("plotly")
        await micropip.install("altair")
        await micropip.install("sane-figs")
        print("✅ All packages installed successfully!")
    return


@app.cell
def import_libs():
    """Import all required libraries."""
    import marimo as mo
    import plotly.express as px
    import plotly.graph_objects as go
    import altair as alt
    import sane_figs
    import pandas as pd
    import numpy as np

    return alt, mo, np, pd, px, sane_figs


@app.cell
def header(mo):
    """Display educational header."""
    mo.md(r"""
    # Sane-Figs: Interactive Size Comparison Demo

    Explore publication-ready figure styling and see **exactly** how your
    figures compare to standard formats like US Letter paper and PowerPoint slides.

    ## Why Size Matters

    - **Article mode**: 3.5" × 2.625" fits perfectly in single-column journals
    - **Presentation mode**: 13.33" × 7.5" fills a 16:9 widescreen slide

    Adjust the settings below and watch the comparison update in real-time.
    """)
    return


@app.cell
def create_controls(mo, sane_figs):
    """Create interactive controls."""

    # Library selector (WASM-safe libraries only)
    library_selector = mo.ui.dropdown(
        options=["Plotly", "Altair"],
        value="Plotly",
        label="Library"
    )

    # Mode selector
    mode_selector = mo.ui.dropdown(
        options=["article", "presentation"],
        value="article",
        label="Mode"
    )

    # Colorway selector (dynamically populated)
    colorway_selector = mo.ui.dropdown(
        options=sane_figs.list_colorways(),
        value="default",
        label="Colorway"
    )

    # Size comparison toggle
    comparison_checkbox = mo.ui.checkbox(
        value=True,
        label="Show size comparison"
    )

    # Display controls
    mo.hstack([library_selector, mode_selector, colorway_selector, comparison_checkbox], justify="center")
    return (
        colorway_selector,
        comparison_checkbox,
        library_selector,
        mode_selector,
    )


@app.cell
def extract_values(
    colorway_selector,
    comparison_checkbox,
    library_selector,
    mode_selector,
):
    """Extract selected values from controls."""
    selected_library = library_selector.value
    selected_mode = mode_selector.value
    selected_colorway = colorway_selector.value
    show_size_comparison = comparison_checkbox.value
    return (
        selected_colorway,
        selected_library,
        selected_mode,
        show_size_comparison,
    )


@app.cell
def generate_plot(
    alt,
    np,
    pd,
    px,
    sane_figs,
    selected_colorway,
    selected_library,
    selected_mode,
):
    """Apply styling and generate the demo plot."""

    # Reset and apply sane-figs styling
    sane_figs.reset()
    sane_figs.setup(mode=selected_mode, colorway=selected_colorway)

    # Get preset info for later use
    current_preset = sane_figs.get_preset(selected_mode)

    # Generate demo data
    t = np.linspace(0, 10, 200)
    demo_data = pd.DataFrame({
        'Time (s)': t,
        'Signal A': np.sin(t),
        'Signal B': np.cos(t),
        'Signal C': np.sin(2*t) * 0.5 + 0.5,
        'Signal D': np.cos(0.5*t) * 0.8
    })

    # Create plot based on selected library
    demo_plot = None
    plot_error = None

    try:
        if selected_library == "Plotly":
            # Melt data for Plotly Express
            melted = demo_data.melt(
                id_vars=['Time (s)'],
                var_name='Signal',
                value_name='Amplitude'
            )
            demo_plot = px.line(
                melted,
                x='Time (s)',
                y='Amplitude',
                color='Signal',
                title=f'Demo Plot: {selected_mode} mode, {selected_colorway} colorway',
                labels={'Amplitude': 'Amplitude (a.u.)'}
            )

        elif selected_library == "Altair":
            # Melt data for Altair
            melted = demo_data.melt(
                id_vars=['Time (s)'],
                var_name='Signal',
                value_name='Amplitude'
            )
            demo_plot = (
                alt.Chart(melted)
                .mark_line()
                .encode(
                    x=alt.X('Time (s):Q', title='Time (s)'),
                    y=alt.Y('Amplitude:Q', title='Amplitude (a.u.)'),
                    color='Signal:N'
                )
                .properties(
                    title=f'Demo Plot: {selected_mode} mode, {selected_colorway} colorway'
                )
            )

    except Exception as e:
        plot_error = str(e)
    return current_preset, demo_plot, plot_error


@app.cell
def create_size_comparison(current_preset, mo):
    """Create visual size comparison with standard formats."""

    # Standard format dimensions (inches)
    US_LETTER = (8.5, 11.0)
    POWERPOINT = (13.33, 7.5)
    # 4-up printout: US Letter landscape divided into 2×2 grid
    FOUR_UP = (5.5, 4.25)  # Each quadrant when printing 4 slides per page

    # Reference DPI for web display (standard 96 DPI)
    WEB_DPI = 96

    # Current figure dimensions
    fig_width, fig_height = current_preset.figure_size
    fig_dpi = current_preset.dpi

    # Convert inches to pixels for display
    def to_px(inches):
        return int(inches * WEB_DPI)

    # Calculate dimensions
    letter_w, letter_h = to_px(US_LETTER[0]), to_px(US_LETTER[1])
    ppt_w, ppt_h = to_px(POWERPOINT[0]), to_px(POWERPOINT[1])
    four_up_w, four_up_h = to_px(FOUR_UP[0]), to_px(FOUR_UP[1])
    fig_w, fig_h = to_px(fig_width), to_px(fig_height)

    # Create container with overlaid outlines
    # Strategy: Use max dimensions and position everything absolutely
    container_w = max(letter_w, ppt_w, fig_w, four_up_w) + 100
    container_h = max(letter_h, ppt_h, fig_h, four_up_h) + 150

    comparison_view = mo.Html(f"""
    <div style="position: relative;
                width: {container_w}px;
                height: {container_h}px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 20px;
                overflow: auto;">

        <!-- Legend -->
        <div style="margin-bottom: 20px; padding: 10px; background: white; border-radius: 4px;">
            <strong>Size Comparison Reference:</strong><br/>
            <span style="color: #6c757d;">━━</span> US Letter Paper (8.5" × 11")<br/>
            <span style="color: #0066cc;">━━</span> PowerPoint Slide (13.33" × 7.5")<br/>
            <span style="color: #28a745;">━━</span> 4-Up Printout Area (5.5" × 4.25")<br/>
            <span style="color: #dc3545;">━━</span> Your Figure ({fig_width}" × {fig_height}" @ {fig_dpi} DPI)
        </div>

        <!-- US Letter outline -->
        <div style="position: absolute;
                    top: 80px; left: 40px;
                    width: {letter_w}px;
                    height: {letter_h}px;
                    border: 2px dashed #6c757d;
                    background: rgba(108, 117, 125, 0.03);">
            <span style="position: absolute; top: -20px; left: 0;
                         color: #6c757d; font-size: 11px; font-weight: 600;">
                US Letter
            </span>
        </div>

        <!-- PowerPoint outline -->
        <div style="position: absolute;
                    top: 120px; left: 80px;
                    width: {ppt_w}px;
                    height: {ppt_h}px;
                    border: 2px dashed #0066cc;
                    background: rgba(0, 102, 204, 0.03);">
            <span style="position: absolute; top: -20px; left: 0;
                         color: #0066cc; font-size: 11px; font-weight: 600;">
                PowerPoint Slide
            </span>
        </div>

        <!-- 4-Up Printout outline -->
        <div style="position: absolute;
                    top: 140px; left: 100px;
                    width: {four_up_w}px;
                    height: {four_up_h}px;
                    border: 2px dashed #28a745;
                    background: rgba(40, 167, 69, 0.05);">
            <span style="position: absolute; top: -20px; left: 0;
                         color: #28a745; font-size: 11px; font-weight: 600;">
                4-Up Printout Area
            </span>
        </div>

        <!-- Figure highlight box -->
        <div style="position: absolute;
                    top: 160px; left: 120px;
                    width: {fig_w}px;
                    height: {fig_h}px;
                    border: 3px solid #dc3545;
                    background: white;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    border-radius: 2px;">
            <span style="position: absolute; top: -25px; left: 0;
                         color: #dc3545; font-size: 12px; font-weight: bold;">
                Your Figure
            </span>
        </div>

        <div style="margin-top: 20px; padding: 10px; background: #fff3cd;
                    border: 1px solid #ffc107; border-radius: 4px; font-size: 11px;">
            <strong>Note:</strong> Size comparison is approximate based on standard 96 DPI display.
            Actual physical size will vary by screen resolution.
            4-Up shows the area each slide occupies when printing 4 slides per page on US Letter (landscape, 2×2 grid).
        </div>
    </div>
    """)
    return comparison_view, fig_height, fig_width


@app.cell
def display_output(
    comparison_view,
    demo_plot,
    fig_height,
    fig_width,
    mo,
    plot_error,
    selected_mode,
    show_size_comparison,
):
    """Display the plot with optional size comparison."""
    _out=None
    # Handle errors
    if plot_error:
        _out=mo.md(f"""
        ### ⚠️ Error Generating Plot

        **Error message:** `{plot_error}`

        Please try a different combination of settings.
        """)
    else:
        # Display info banner
        info = mo.md(f"""
        ### Generated Figure
    
        **Mode:** {selected_mode} | **Dimensions:** {fig_width}" × {fig_height}"
        """)
    
        # Show output based on comparison toggle
        if show_size_comparison:
            _out=mo.vstack([
                info,
                comparison_view,
                mo.md("---"),
                mo.md("### The Plot:"),
                demo_plot
            ])
        else:
            _out=mo.vstack([
                info,
                demo_plot
            ])
    _out
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
