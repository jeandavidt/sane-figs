"""
Generate all documentation figures.
Run with: uv run docs_scripts/generate_figures.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import sane_figs
from pathlib import Path

# Create output directory
output_dir = Path(__file__).parent.parent / "docs" / "images"
output_dir.mkdir(parents=True, exist_ok=True)

# Common data
x = np.linspace(0, 10, 100)
y = np.sin(x)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x + np.pi / 4)

print("=" * 60)
print("Starting documentation figure generation...")
print("=" * 60)


def save_mpl(name):
    """Save current matplotlib figure consistently."""
    plt.tight_layout()
    plt.savefig(output_dir / name, bbox_inches="tight")
    plt.close()
    print(f"Generated: {name}")


# =============================================================================
# Index / Basic Usage
# =============================================================================
print("\n[1/7] Generating Index / Basic Usage figures...")
sane_figs.setup(mode="article")
plt.figure()
plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("basic_usage.png")

# =============================================================================
# Presets page
# =============================================================================
print("\n[2/7] Generating Presets page figures...")

# Article vs Presentation comparison
# Use a shared figsize so only the font/line styling differs
demo_figsize = (8, 5)

sane_figs.setup(mode="article")
plt.figure(figsize=demo_figsize)
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.legend()
plt.title("Trigonometric Functions")
plt.xlabel("x")
plt.ylabel("y")
save_mpl("article_mode.png")

sane_figs.setup(mode="presentation")
plt.figure(figsize=demo_figsize)
plt.plot(x, y, label="sin(x)")
plt.title("Sine Wave (Presentation Mode)")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("presentation_mode.png")

# Preset example
sane_figs.setup(mode="article")
plt.figure()
plt.plot(x, y1)
plt.plot(x, y2)
plt.title("Nature Journal Preset Example")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
save_mpl("presets_example.png")

# =============================================================================
# Colorways page - Color blocks (need custom sizing for swatch layout)
# =============================================================================
print("\n[3/7] Generating Colorways page figures...")
for colorway_name in ["default", "nature", "vibrant", "pastel", "colorblind-safe"]:
    sane_figs.setup(mode="article", colorway=colorway_name)
    colorway = sane_figs.get_colorway(colorway_name)
    colors = colorway.categorical[:10]

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis("off")

    for i, color in enumerate(colors):
        rect = patches.Rectangle(
            (i, 0), 1, 1, linewidth=0, edgecolor=None, facecolor=color
        )
        ax.add_patch(rect)
        ax.text(
            i + 0.5,
            0.5,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="white" if i % 2 == 0 else "black",
        )

    plt.title(
        f"{colorway_name.capitalize()} Colorway",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    plt.tight_layout()
    plt.savefig(
        output_dir / f"colorway_{colorway_name}.png", bbox_inches="tight"
    )
    plt.close()
    print(f"Generated: colorway_{colorway_name}.png (color blocks)")

# Colorway example (Nature line plot)
sane_figs.setup(mode="article", colorway="nature")
plt.figure()
plt.plot(x, y1, label="Series 1")
plt.plot(x, y2, label="Series 2")
plt.plot(x, y3, label="Series 3")
plt.legend()
plt.title("Nature Colorway Example")
save_mpl("colorway_example.png")

# Accessible figure
sane_figs.setup(mode="article", colorway="colorblind-safe")
plt.figure()
plt.plot(x, y1, label="sin(x)", linestyle="-")
plt.plot(x, y2, label="cos(x)", linestyle="--")
plt.legend()
plt.title("Accessible Figure")
save_mpl("accessible_figure.png")

# =============================================================================
# Watermarks page
# =============================================================================
print("\n[4/7] Generating Watermarks page figures...")
sane_figs.setup(mode="article", watermark="\u00a9 2025 My Lab")
plt.figure()
plt.plot(x, y)
plt.title("Figure with Text Watermark")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("watermark_text.png")

sane_figs.setup(
    mode="article",
    watermark=sane_figs.create_text_watermark(
        "LOGO", position="top-right", opacity=0.2
    ),
)
plt.figure()
plt.plot(x, y)
plt.title("Figure with Image Watermark")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("watermark_image.png")

# Watermark positions
for pos in ["top-left", "top-right", "bottom-left", "bottom-right"]:
    sane_figs.setup(
        mode="article",
        watermark=sane_figs.create_text_watermark(
            "DRAFT", position=pos, opacity=0.3
        ),
    )
    plt.figure()
    plt.plot(x, y)
    plt.title(f"Watermark: {pos}")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    save_mpl(f"watermark_{pos}.png")

# Effective watermark
sane_figs.setup(
    mode="article",
    watermark=sane_figs.create_text_watermark(
        "\u00a9 2025 My Lab", position="bottom-right", opacity=0.15
    ),
)
plt.figure()
plt.plot(x, y)
plt.title("Effective Watermark")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("watermark_effective.png")

# =============================================================================
# Matplotlib page
# =============================================================================
print("\n[5/7] Generating Matplotlib page figures...")

# Basic
sane_figs.setup(mode="article")
plt.figure()
plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)")
save_mpl("matplotlib_basic.png")

# Simple line
sane_figs.setup(mode="article")
plt.figure()
plt.plot(x, y)
plt.title("Simple Line Plot")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True, alpha=0.3)
save_mpl("matplotlib_line.png")

# Multiple lines
sane_figs.setup(mode="article")
plt.figure()
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.plot(x, y3, label="sin(x + \u03c0/4)")
plt.legend()
plt.title("Multiple Lines")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
save_mpl("matplotlib_multiple_lines.png")

# Scatter
sane_figs.setup(mode="article")
np.random.seed(42)
sx = np.random.randn(100)
sy = np.random.randn(100)
sc = np.random.rand(100)
plt.figure()
plt.scatter(sx, sy, c=sc, s=50, alpha=0.7, edgecolors="black", linewidth=0.5)
plt.title("Scatter Plot")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="Value")
plt.grid(True, alpha=0.3)
save_mpl("matplotlib_scatter.png")

# Bar chart
sane_figs.setup(mode="article")
categories = ["A", "B", "C", "D", "E"]
values = [23, 45, 56, 78, 32]
plt.figure()
plt.bar(categories, values, edgecolor="black", linewidth=0.5)
plt.title("Bar Chart")
plt.xlabel("Category")
plt.ylabel("Value")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("matplotlib_bar.png")

# Histogram
sane_figs.setup(mode="article")
np.random.seed(42)
hist_data = np.random.randn(1000)
plt.figure()
plt.hist(hist_data, bins=30, edgecolor="black", linewidth=0.5, alpha=0.7)
plt.title("Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("matplotlib_histogram.png")

# Subplots - needs explicit figsize for side-by-side panels
sane_figs.setup(mode="article")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2.625))
ax1.plot(x, y1)
ax1.set_title("Sine Wave")
ax1.set_xlabel("x")
ax1.set_ylabel("sin(x)")
ax1.grid(True, alpha=0.3)
ax2.plot(x, y2)
ax2.set_title("Cosine Wave")
ax2.set_xlabel("x")
ax2.set_ylabel("cos(x)")
ax2.grid(True, alpha=0.3)
save_mpl("matplotlib_subplots.png")

# Colorway
sane_figs.setup(mode="article", colorway="nature")
plt.figure()
plt.plot(x, y1, label="Series 1")
plt.plot(x, y2, label="Series 2")
plt.plot(x, y3, label="Series 3")
plt.legend()
plt.title("Nature Colorway")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
save_mpl("matplotlib_colorway.png")

# Watermark
sane_figs.setup(mode="article", watermark="\u00a9 2025 My Lab")
plt.figure()
plt.plot(x, y)
plt.title("Figure with Watermark")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True, alpha=0.3)
save_mpl("matplotlib_watermark.png")

# =============================================================================
# Seaborn page
# =============================================================================
print("\n[6/7] Generating Seaborn page figures...")

# Basic
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.histplot(np.random.randn(100))
plt.title("Histogram with Seaborn")
save_mpl("seaborn_basic.png")

# Histogram with KDE
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.histplot(np.random.randn(1000), bins=30, kde=True, edgecolor="black", linewidth=0.5)
plt.title("Histogram with KDE")
plt.xlabel("Value")
plt.ylabel("Count")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_histogram.png")

# Box plot
sane_figs.setup(mode="article")
np.random.seed(42)
box_data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
plt.figure()
sns.boxplot(data=box_data)
plt.title("Box Plot")
plt.xlabel("Group")
plt.ylabel("Value")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_boxplot.png")

# Violin plot
sane_figs.setup(mode="article")
np.random.seed(42)
violin_data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
plt.figure()
sns.violinplot(data=violin_data)
plt.title("Violin Plot")
plt.xlabel("Group")
plt.ylabel("Value")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_violin.png")

# Bar plot
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.barplot(
    x=["A", "B", "C", "D", "E"],
    y=np.random.randint(10, 100, 5),
    edgecolor="black",
    linewidth=0.5,
)
plt.title("Bar Plot")
plt.xlabel("Category")
plt.ylabel("Value")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_barplot.png")

# Count plot
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.countplot(
    x=np.random.choice(["A", "B", "C", "D", "E"], 100),
    edgecolor="black",
    linewidth=0.5,
)
plt.title("Count Plot")
plt.xlabel("Category")
plt.ylabel("Count")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_countplot.png")

# Scatter plot
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.scatterplot(
    x=np.random.randn(100),
    y=np.random.randn(100),
    s=50,
    alpha=0.7,
    edgecolor="black",
    linewidth=0.5,
)
plt.title("Scatter Plot")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
save_mpl("seaborn_scatter.png")

# Line plot
sane_figs.setup(mode="article")
plt.figure()
sns.lineplot(x=x, y=y)
plt.title("Line Plot")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True, alpha=0.3)
save_mpl("seaborn_lineplot.png")

# Heatmap
sane_figs.setup(mode="article")
np.random.seed(42)
plt.figure()
sns.heatmap(
    np.random.randn(10, 10),
    cmap="coolwarm",
    center=0,
    annot=False,
    cbar_kws={"label": "Value"},
)
plt.title("Heatmap")
save_mpl("seaborn_heatmap.png")

# Regression plot
sane_figs.setup(mode="article")
np.random.seed(42)
reg_x = np.random.randn(100)
reg_y = 2 * reg_x + np.random.randn(100)
plt.figure()
sns.regplot(x=reg_x, y=reg_y, scatter_kws={"s": 50, "alpha": 0.7})
plt.title("Linear Regression")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
save_mpl("seaborn_regplot.png")

# Colorway
sane_figs.setup(mode="article", colorway="nature")
np.random.seed(42)
plt.figure()
sns.barplot(
    x=["A", "B", "C", "D", "E"],
    y=np.random.randint(10, 100, 5),
    edgecolor="black",
    linewidth=0.5,
)
plt.title("Nature Colorway")
plt.xlabel("Category")
plt.ylabel("Value")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_colorway.png")

# Watermark
sane_figs.setup(mode="article", watermark="\u00a9 2025 My Lab")
np.random.seed(42)
plt.figure()
sns.histplot(np.random.randn(1000), bins=30, kde=True, edgecolor="black", linewidth=0.5)
plt.title("Figure with Watermark")
plt.xlabel("Value")
plt.ylabel("Count")
plt.grid(True, alpha=0.3, axis="y")
save_mpl("seaborn_watermark.png")

# =============================================================================
# Plotly page
# =============================================================================
print("\n[7/7] Generating Plotly page figures...")


def save_plotly(fig, name):
    """Save plotly figure consistently."""
    # Don't use scale parameter - it causes fonts to appear too small
    # The template already sets the correct figure size and font sizes
    fig.write_image(str(output_dir / name))
    print(f"Generated: {name}")


# Basic
sane_figs.setup(mode="article")
fig = px.line(x=x, y=y, title="Sine Wave")
fig.update_layout(xaxis_title="x", yaxis_title="sin(x)")
save_plotly(fig, "plotly_basic.png")

# Simple line
sane_figs.setup(mode="article")
fig = px.line(
    x=x, y=y, title="Simple Line Plot", labels={"x": "x", "y": "sin(x)"}
)
fig.update_layout(showlegend=True)
save_plotly(fig, "plotly_line.png")

# Multiple lines
sane_figs.setup(mode="article")
df = pd.DataFrame(
    {
        "x": x,
        "sin(x)": np.sin(x),
        "cos(x)": np.cos(x),
        "sin(x + \u03c0/4)": np.sin(x + np.pi / 4),
    }
)
df_long = df.melt("x", var_name="Function", value_name="y")
fig = px.line(df_long, x="x", y="y", color="Function", title="Multiple Lines")
fig.update_layout(showlegend=True)
save_plotly(fig, "plotly_multiple_lines.png")

# Scatter
sane_figs.setup(mode="article")
np.random.seed(42)
fig = px.scatter(
    x=np.random.randn(100),
    y=np.random.randn(100),
    color=np.random.rand(100),
    title="Scatter Plot",
    labels={"x": "x", "y": "y", "color": "Value"},
    color_continuous_scale="Viridis",
)
fig.update_traces(marker=dict(opacity=0.7))
save_plotly(fig, "plotly_scatter.png")

# Bar chart
sane_figs.setup(mode="article")
fig = px.bar(
    x=["A", "B", "C", "D", "E"],
    y=[23, 45, 56, 78, 32],
    title="Bar Chart",
    labels={"x": "Category", "y": "Value"},
)
fig.update_layout(showlegend=False)
save_plotly(fig, "plotly_bar.png")

# Histogram
sane_figs.setup(mode="article")
np.random.seed(42)
fig = px.histogram(
    np.random.randn(1000),
    nbins=30,
    title="Histogram",
    labels={"value": "Value", "count": "Frequency"},
)
fig.update_layout(showlegend=False)
save_plotly(fig, "plotly_histogram.png")

# Box plot
sane_figs.setup(mode="article")
np.random.seed(42)
box_data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
df_box = pd.DataFrame(
    {
        "Group": ["A"] * 100 + ["B"] * 100 + ["C"] * 100,
        "Value": np.concatenate(box_data),
    }
)
fig = px.box(df_box, x="Group", y="Value", title="Box Plot")
fig.update_layout(showlegend=False)
save_plotly(fig, "plotly_box.png")

# Violin plot
sane_figs.setup(mode="article")
fig = px.violin(df_box, x="Group", y="Value", title="Violin Plot")
fig.update_layout(showlegend=False)
save_plotly(fig, "plotly_violin.png")

# Subplots - needs explicit sizing for multi-panel layout
sane_figs.setup(mode="article")
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("Sine Wave", "Cosine Wave")
)
fig.add_trace(
    go.Scatter(x=x, y=y1, mode="lines", name="sin(x)"), row=1, col=1
)
fig.add_trace(
    go.Scatter(x=x, y=y2, mode="lines", name="cos(x)"), row=1, col=2
)
fig.update_xaxes(title_text="x")
fig.update_yaxes(title_text="sin(x)", row=1, col=1)
fig.update_yaxes(title_text="cos(x)", row=1, col=2)
fig.update_layout(showlegend=True, width=1200, height=500)
save_plotly(fig, "plotly_subplots.png")

# Colorway
sane_figs.setup(mode="article", colorway="nature")
df_cw = pd.DataFrame(
    {
        "x": x,
        "Series 1": np.sin(x),
        "Series 2": np.cos(x),
        "Series 3": np.sin(x + np.pi / 4),
    }
)
df_long = df_cw.melt("x", var_name="Series", value_name="y")
fig = px.line(df_long, x="x", y="y", color="Series", title="Nature Colorway")
fig.update_layout(showlegend=True)
save_plotly(fig, "plotly_colorway.png")

# Watermark
sane_figs.setup(mode="article", watermark="\u00a9 2025 My Lab")
fig = px.line(
    x=x,
    y=y,
    title="Figure with Watermark",
    labels={"x": "x", "y": "sin(x)"},
)
fig.update_layout(showlegend=True)
save_plotly(fig, "plotly_watermark.png")

# =============================================================================
# Altair page
# =============================================================================
print("\n[8/8] Generating Altair page figures...")


def save_altair(chart, name):
    """Save altair chart consistently."""
    # Save without scale factor - the theme should handle font sizing
    chart.save(str(output_dir / name))
    print(f"Generated: {name}")


# Basic
sane_figs.setup(mode="article")
df_line = pd.DataFrame({"x": x, "y": y})
chart = (
    alt.Chart(df_line)
    .mark_line()
    .encode(x="x", y="y")
    .properties(title="Sine Wave")
)
save_altair(chart, "altair_basic.png")

# Simple line
sane_figs.setup(mode="article")
chart = (
    alt.Chart(df_line)
    .mark_line()
    .encode(x=alt.X("x", title="x"), y=alt.Y("y", title="sin(x)"))
    .properties(title="Simple Line Plot")
)
save_altair(chart, "altair_line.png")

# Multiple lines
sane_figs.setup(mode="article")
df_multi = pd.DataFrame(
    {
        "x": x,
        "sin(x)": np.sin(x),
        "cos(x)": np.cos(x),
        "sin(x + \u03c0/4)": np.sin(x + np.pi / 4),
    }
)
df_long = df_multi.melt("x", var_name="Function", value_name="y")
chart = (
    alt.Chart(df_long)
    .mark_line()
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("y", title="y"),
        color=alt.Color("Function", legend=alt.Legend(title="Function")),
    )
    .properties(title="Multiple Lines")
)
save_altair(chart, "altair_multiple_lines.png")

# Scatter
sane_figs.setup(mode="article")
np.random.seed(42)
df_scatter = pd.DataFrame(
    {
        "x": np.random.randn(100),
        "y": np.random.randn(100),
        "color": np.random.rand(100),
    }
)
chart = (
    alt.Chart(df_scatter)
    .mark_circle(opacity=0.7)
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("y", title="y"),
        color=alt.Color(
            "color",
            legend=alt.Legend(title="Value"),
            scale=alt.Scale(scheme="viridis"),
        ),
    )
    .properties(title="Scatter Plot")
)
save_altair(chart, "altair_scatter.png")

# Bar chart
sane_figs.setup(mode="article")
df_bar = pd.DataFrame(
    {"Category": ["A", "B", "C", "D", "E"], "Value": [23, 45, 56, 78, 32]}
)
chart = (
    alt.Chart(df_bar)
    .mark_bar()
    .encode(
        x=alt.X("Category", title="Category"),
        y=alt.Y("Value", title="Value"),
    )
    .properties(title="Bar Chart")
)
save_altair(chart, "altair_bar.png")

# Histogram
sane_figs.setup(mode="article")
np.random.seed(42)
df_hist = pd.DataFrame({"Value": np.random.randn(1000)})
chart = (
    alt.Chart(df_hist)
    .mark_bar(opacity=0.7)
    .encode(
        x=alt.X("Value", bin=alt.Bin(maxbins=30), title="Value"),
        y=alt.Y("count()", title="Frequency"),
    )
    .properties(title="Histogram")
)
save_altair(chart, "altair_histogram.png")

# Box plot
sane_figs.setup(mode="article")
np.random.seed(42)
box_data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
df_alt_box = pd.DataFrame(
    {
        "Group": ["A"] * 100 + ["B"] * 100 + ["C"] * 100,
        "Value": np.concatenate(box_data),
    }
)
chart = (
    alt.Chart(df_alt_box)
    .mark_boxplot()
    .encode(
        x=alt.X("Group", title="Group"),
        y=alt.Y("Value", title="Value"),
    )
    .properties(title="Box Plot")
)
save_altair(chart, "altair_box.png")

# Area chart
sane_figs.setup(mode="article")
df_area = pd.DataFrame(
    {"x": x, "sin(x)": np.sin(x), "cos(x)": np.cos(x)}
)
df_long = df_area.melt("x", var_name="Function", value_name="y")
chart = (
    alt.Chart(df_long)
    .mark_area(opacity=0.5)
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("y", title="y"),
        color=alt.Color("Function", legend=alt.Legend(title="Function")),
    )
    .properties(title="Area Chart")
)
save_altair(chart, "altair_area.png")

# Subplots (faceting) - needs explicit width for faceted panels
sane_figs.setup(mode="article")
df_facet = pd.DataFrame(
    {"x": x, "sin(x)": np.sin(x), "cos(x)": np.cos(x)}
)
df_long = df_facet.melt("x", var_name="Function", value_name="y")
chart = (
    alt.Chart(df_long)
    .mark_line()
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("y", title="y"),
        color=alt.Color("Function", legend=alt.Legend(title="Function")),
    )
    .properties(width=300, height=300)
    .facet(column=alt.Column("Function", title=None))
    .properties(title="Subplots")
)
save_altair(chart, "altair_subplots.png")

# Colorway
sane_figs.setup(mode="article", colorway="nature")
df_cw = pd.DataFrame(
    {
        "x": x,
        "Series 1": np.sin(x),
        "Series 2": np.cos(x),
        "Series 3": np.sin(x + np.pi / 4),
    }
)
df_long = df_cw.melt("x", var_name="Series", value_name="y")
chart = (
    alt.Chart(df_long)
    .mark_line()
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("y", title="y"),
        color=alt.Color("Series", legend=alt.Legend(title="Series")),
    )
    .properties(title="Nature Colorway")
)
save_altair(chart, "altair_colorway.png")

# Watermark
sane_figs.setup(mode="article", watermark="\u00a9 2025 My Lab")
df_wm = pd.DataFrame({"x": x, "y": y})
chart = (
    alt.Chart(df_wm)
    .mark_line()
    .encode(x=alt.X("x", title="x"), y=alt.Y("y", title="sin(x)"))
    .properties(title="Figure with Watermark")
)
save_altair(chart, "altair_watermark.png")

print("\n" + "=" * 60)
print("All figures generated successfully!")
print("=" * 60)
