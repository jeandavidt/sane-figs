"""
Cross-library legend positioning demo for sane-figs.

Generates the same sin/cos figure with all four supported libraries
(Matplotlib, Seaborn, Plotly, Altair) using the article preset with
legend positioned at inside_upper_right.

Run with:
    python examples/legend_positioning_demo.py

Matplotlib and Seaborn figures are saved as PNG.
Plotly and Altair figures are saved as HTML.
"""

import numpy as np

import sane_figs
from sane_figs.styling.layout import LegendConfig

# Data shared across all figures
x = np.linspace(0, 2 * np.pi, 200)
y_sin = np.sin(x)
y_cos = np.cos(x)


def demo_matplotlib():
    import matplotlib.pyplot as plt

    sane_figs.reset()
    sane_figs.setup_matplotlib(
        mode="article",
        legend_config=LegendConfig(position="inside_upper_right"),
    )

    fig, ax = plt.subplots()
    ax.plot(x, y_sin, label="sin(x)")
    ax.plot(x, y_cos, label="cos(x)")
    ax.set_title("Matplotlib — inside_upper_right legend")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()

    fig.savefig("legend_demo_matplotlib.png", bbox_inches="tight")
    plt.close(fig)
    print("Saved: legend_demo_matplotlib.png")


def demo_seaborn():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    sane_figs.reset()
    sane_figs.setup_seaborn(
        mode="article",
        legend_config=LegendConfig(position="inside_upper_right"),
    )

    df = pd.DataFrame({"x": x, "sin(x)": y_sin, "cos(x)": y_cos})
    df_long = df.melt(id_vars="x", var_name="function", value_name="y")

    fig, ax = plt.subplots()
    sns.lineplot(data=df_long, x="x", y="y", hue="function", ax=ax)
    ax.set_title("Seaborn — inside_upper_right legend")

    fig.savefig("legend_demo_seaborn.png", bbox_inches="tight")
    plt.close(fig)
    print("Saved: legend_demo_seaborn.png")


def demo_plotly():
    import plotly.graph_objects as go

    sane_figs.reset()
    sane_figs.setup_plotly(
        mode="article",
        legend_config=LegendConfig(position="inside_upper_right"),
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_sin, mode="lines", name="sin(x)"))
    fig.add_trace(go.Scatter(x=x, y=y_cos, mode="lines", name="cos(x)"))
    fig.update_layout(
        title="Plotly — inside_upper_right legend",
        xaxis_title="x",
        yaxis_title="y",
    )

    fig.write_html("legend_demo_plotly.html")
    print("Saved: legend_demo_plotly.html")


def demo_altair():
    import altair as alt
    import pandas as pd

    sane_figs.reset()
    sane_figs.setup_altair(
        mode="article",
        legend_config=LegendConfig(position="inside_upper_right"),
    )

    df = pd.DataFrame({"x": x, "sin(x)": y_sin, "cos(x)": y_cos})
    df_long = df.melt(id_vars="x", var_name="function", value_name="y")

    chart = (
        alt.Chart(df_long)
        .mark_line()
        .encode(
            x=alt.X("x:Q", title="x"),
            y=alt.Y("y:Q", title="y"),
            color=alt.Color("function:N"),
        )
        .properties(title="Altair — inside_upper_right legend")
    )

    chart.save("legend_demo_altair.html")
    print("Saved: legend_demo_altair.html")


if __name__ == "__main__":
    print("Generating cross-library legend positioning demo...\n")
    demo_matplotlib()
    demo_seaborn()
    demo_plotly()
    demo_altair()
    print(
        "\nAll figures generated. Verify that the legend appears in the"
        " top-right corner inside the plot area for all four figures."
    )
