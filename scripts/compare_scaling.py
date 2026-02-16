"""
Diagnostic script: generate the same scatter plot with all 4 libraries,
save to PNG, and print the expected vs actual pixel dimensions of key elements.

Run from repo root:
    python scripts/compare_scaling.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import sane_figs

# ── shared data ────────────────────────────────────────────────────────────────
np.random.seed(42)
x = np.linspace(0, 10, 20)
y1 = np.sin(x) + np.random.normal(0, 0.1, 20)
y2 = np.cos(x) + np.random.normal(0, 0.1, 20)

OUT = "scripts/compare_output"
os.makedirs(OUT, exist_ok=True)

preset = sane_figs.get_preset("article")
print(f"Preset: {preset.name}")
print(f"  figure_size : {preset.figure_size} in")
print(f"  dpi (print) : {preset.dpi}")
print(f"  screen_dpi  : {preset.screen_dpi!r}  → get_display_dpi()={preset.get_display_dpi()}")
print(f"  font_size   : {preset.font_size}")
print(f"  line_width  : {preset.line_width}")
print(f"  marker_size : {preset.marker_size}")
from sane_figs.utils.dpi_utils import get_screen_scale, get_export_scale_factor, get_screen_dimensions
scale = get_screen_scale(preset)
export_sf = get_export_scale_factor(preset)
w_px, h_px = get_screen_dimensions(preset)
print(f"\nDerived values:")
print(f"  screen_scale        = {scale:.4f}  (screen_dpi / 72)")
print(f"  export_scale_factor = {export_sf:.4f}  (print_dpi / screen_dpi)")
print(f"  screen_dimensions   = {w_px} x {h_px} px")

# ── expected pixel sizes at export ────────────────────────────────────────────
label_pt   = preset.font_size.get("label", 12)
title_pt   = preset.font_size.get("title", 14)
tick_pt    = preset.font_size.get("tick", 10)
mpl_label_px = label_pt * preset.dpi / 72
mpl_marker_px = preset.marker_size * preset.dpi / 72
print(f"\nExpected export pixel sizes (Matplotlib reference):")
print(f"  label font  : {label_pt}pt × {preset.dpi}dpi/72 = {mpl_label_px:.1f} px")
print(f"  marker diam : {preset.marker_size}pt × {preset.dpi}dpi/72 = {mpl_marker_px:.1f} px")


# ── 1. Matplotlib ─────────────────────────────────────────────────────────────
print("\n── Matplotlib ──")
sane_figs.reset()
sane_figs.setup(mode="article", libraries=["matplotlib"])

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(x, y1, label="sin(x)")
ax.scatter(x, y2, label="cos(x)")
ax.set_title("Matplotlib")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.legend()
mpl_path = f"{OUT}/matplotlib.png"
fig.savefig(mpl_path)
plt.close()
from PIL import Image
img = Image.open(mpl_path)
print(f"  saved {img.size[0]}×{img.size[1]} px → {mpl_path}")

# ── 2. Seaborn ────────────────────────────────────────────────────────────────
print("\n── Seaborn ──")
sane_figs.reset()
sane_figs.setup(mode="article", libraries=["seaborn"])

import seaborn as sns
import pandas as pd
df = pd.DataFrame({"x": np.tile(x, 2),
                   "y": np.concatenate([y1, y2]),
                   "group": ["sin"]*20 + ["cos"]*20})
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="x", y="y", hue="group", ax=ax)
ax.set_title("Seaborn")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
sns_path = f"{OUT}/seaborn.png"
fig.savefig(sns_path)
plt.close()
img = Image.open(sns_path)
print(f"  saved {img.size[0]}×{img.size[1]} px → {sns_path}")

# ── 3. Plotly ─────────────────────────────────────────────────────────────────
print("\n── Plotly ──")
sane_figs.reset()
sane_figs.setup(mode="article", libraries=["plotly"])

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1, mode="markers", name="sin(x)"))
fig.add_trace(go.Scatter(x=x, y=y2, mode="markers", name="cos(x)"))
fig.update_layout(title="Plotly", xaxis_title="X label", yaxis_title="Y label")
plotly_path = f"{OUT}/plotly.png"
fig.write_image(plotly_path)
img = Image.open(plotly_path)
print(f"  saved {img.size[0]}×{img.size[1]} px → {plotly_path}")

# ── 4. Altair ─────────────────────────────────────────────────────────────────
print("\n── Altair ──")
sane_figs.reset()
sane_figs.setup(mode="article", libraries=["altair"])

import altair as alt
df_alt = pd.DataFrame({"x": np.tile(x, 2),
                        "y": np.concatenate([y1, y2]),
                        "group": ["sin(x)"]*20 + ["cos(x)"]*20})
chart = (
    alt.Chart(df_alt)
    .mark_point()
    .encode(x="x:Q", y="y:Q", color="group:N")
    .properties(title="Altair")
)
altair_path = f"{OUT}/altair.png"
chart.save(altair_path)
img = Image.open(altair_path)
print(f"  saved {img.size[0]}×{img.size[1]} px → {altair_path}")

print("\n✓ All images saved. Open scripts/compare_output/ to inspect them.")
