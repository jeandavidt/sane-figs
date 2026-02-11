import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import sane_figs
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import altair as alt
    import pandas as pd
    import numpy as np

    return alt, mo, np, pd, plt, px, sane_figs, sns


@app.cell
def _(mo):
    mo.md(r"""
    # Sane-Figs Interactive Demo

    Experiment with different libraries, styles, and colorways to see how **sane-figs** automatically styles your figures.
    """)
    return


@app.cell
def _(mo, sane_figs):
    # Controls
    library_selector = mo.ui.dropdown(
        options=["Matplotlib", "Seaborn", "Plotly", "Altair"],
        value="Matplotlib",
        label="Library"
    )

    style_selector = mo.ui.dropdown(
        options=["article", "presentation"],
        value="article",
        label="Style"
    )

    # Use list_colorways to populate themes, including ulaval, modeleau etc.
    theme_selector = mo.ui.dropdown(
        options=sane_figs.list_colorways(),
        value="default",
        label="Theme"
    )

    mo.hstack([library_selector, style_selector, theme_selector], justify="center")
    return library_selector, style_selector, theme_selector


@app.cell
def _(library_selector, style_selector, theme_selector):
    # Get values
    selected_lib = library_selector.value
    selected_style = style_selector.value
    selected_theme = theme_selector.value
    return selected_lib, selected_style, selected_theme


@app.cell
def _(
    alt,
    mo,
    np,
    pd,
    plt,
    px,
    sane_figs,
    selected_lib,
    selected_style,
    selected_theme,
    sns,
):
    # Generate Data
    def get_data():
        x = np.linspace(0, 10, 100)
        return pd.DataFrame({
            'x': x,
            'y1': np.sin(x),
            'y2': np.cos(x),
            'y3': np.sin(x) * 0.5 + np.cos(x) * 0.5,
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })

    df = get_data()

    # Reset and Apply Style
    # We reset first to ensure clean state when switching modes/colorways
    sane_figs.reset()
    # Apply style (size/font-size) and theme (colors)
    sane_figs.setup(mode=selected_style, colorway=selected_theme)

    # Plotting Logic
    final_plot = None

    try:
        if selected_lib == "Matplotlib":
            fig, ax = plt.subplots()
            ax.plot(df['x'], df['y1'], label='Sin(x)')
            ax.plot(df['x'], df['y2'], label='Cos(x)')
            ax.plot(df['x'], df['y3'], label='Combined')
            ax.set_title(f"{selected_lib} - {selected_style} - {selected_theme}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            final_plot = fig

        elif selected_lib == "Seaborn":
            fig, ax = plt.subplots()
            # For seaborn, we'll use a slightly different data shape for some var
            sns.lineplot(data=df, x='x', y='y1', label='Sin(x)', ax=ax)
            sns.lineplot(data=df, x='x', y='y2', label='Cos(x)', ax=ax)
            ax.set_title(f"{selected_lib} - {selected_style} - {selected_theme}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            final_plot = fig

        elif selected_lib == "Plotly":
            # Melt for plotly express
            df_melt = df.melt(id_vars=['x', 'category'], value_vars=['y1', 'y2', 'y3'], var_name='signal', value_name='value')
            fig = px.line(df_melt, x='x', y='value', color='signal', title=f"{selected_lib} - {selected_style} - {selected_theme}")
            final_plot = fig

        elif selected_lib == "Altair":
             # Melt for altair
            df_melt = df.melt(id_vars=['x', 'category'], value_vars=['y1', 'y2', 'y3'], var_name='signal', value_name='value')
            fig = alt.Chart(df_melt).mark_line().encode(
                x='x',
                y='value',
                color='signal'
            ).properties(title=f"{selected_lib} - {selected_style} - {selected_theme}")
            final_plot = fig

    except Exception as e:
        final_plot = mo.md(f"**Error generating plot:** {str(e)}")

    # Display
    # Center the output and prevent it from stretching to full width
    # We use a div with fit-content width to respect the figure's natural size
    mo.vstack([
        mo.Html(
            mo.hstack([final_plot], justify="center").text,
            style={"width": "100%", "display": "flex", "justify-content": "center"}
        )
    ])
    return


if __name__ == "__main__":
    app.run()
