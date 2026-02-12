"""
Test image watermark functionality across all 4 supported plotting libraries.

This script creates figures with image watermarks using test_logo.png.
"""

import os
from pathlib import Path

# Create output directory
output_dir = Path("watermark_test_output")
output_dir.mkdir(exist_ok=True)

# Test data
import numpy as np
import pandas as pd

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
df = pd.DataFrame({'x': x, 'sin(x)': y1, 'cos(x)': y2})

# Import sane_figs
import sane_figs

# Get absolute path to the logo
logo_path = Path("test_logo.png").absolute()

print("=" * 60)
print("Testing Image Watermark Feature Across All Libraries")
print(f"Using logo: {logo_path}")
print("=" * 60)

# Test 1: Matplotlib with image watermark
print("\n1. Testing Matplotlib image watermark...")
try:
    import matplotlib.pyplot as plt
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with image watermark
    sane_figs.setup(
        mode='article',
        libraries=['matplotlib'],
        watermark=sane_figs.create_image_watermark(
            image_path=str(logo_path),
            position='bottom-right',
            opacity=0.5,
            scale=0.15,
        )
    )
    
    # Create figure
    plt.figure(figsize=(8, 5))
    plt.plot(x, y1, label='sin(x)', linewidth=1.5)
    plt.plot(x, y2, label='cos(x)', linewidth=1.5)
    plt.title('Matplotlib Image Watermark Test')
    plt.xlabel('x (radians)')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure (watermark should be added automatically)
    output_path = output_dir / "image_watermark_matplotlib.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Matplotlib figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Matplotlib test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Seaborn with image watermark
print("\n2. Testing Seaborn image watermark...")
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with image watermark
    sane_figs.setup(
        mode='article',
        libraries=['seaborn'],
        watermark=sane_figs.create_image_watermark(
            image_path=str(logo_path),
            position='top-left',
            opacity=0.4,
            scale=0.12,
        )
    )
    
    # Create figure using seaborn
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='x', y='sin(x)', label='sin(x)')
    sns.lineplot(data=df, x='x', y='cos(x)', label='cos(x)')
    plt.title('Seaborn Image Watermark Test')
    plt.xlabel('x (radians)')
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    
    # Save figure (watermark should be added automatically)
    output_path = output_dir / "image_watermark_seaborn.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Seaborn figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Seaborn test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Plotly with image watermark
print("\n3. Testing Plotly image watermark...")
try:
    import plotly.graph_objects as go
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with image watermark
    sane_figs.setup(
        mode='article',
        libraries=['plotly'],
        watermark=sane_figs.create_image_watermark(
            image_path=str(logo_path),
            position='bottom-right',
            opacity=0.5,
            scale=0.15,
        )
    )
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='sin(x)'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='cos(x)'))
    fig.update_layout(
        title='Plotly Image Watermark Test',
        xaxis_title='x (radians)',
        yaxis_title='y',
    )
    
    # Save figure
    output_path = output_dir / "image_watermark_plotly.html"
    fig.write_html(str(output_path))
    
    print(f"   ✓ Plotly figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Plotly test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Altair with image watermark
print("\n4. Testing Altair image watermark...")
try:
    import altair as alt
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with image watermark
    sane_figs.setup(
        mode='article',
        libraries=['altair'],
        watermark=sane_figs.create_image_watermark(
            image_path=str(logo_path),
            position='bottom-right',
            opacity=0.5,
            scale=0.15,
        )
    )
    
    # Create base chart
    base = alt.Chart(df).encode(x='x:Q')
    
    chart = (
        base.mark_line(color='blue')
        .encode(y='sin(x):Q')
        .properties(title='Altair Image Watermark Test', width=600, height=400)
    )
    
    # Save figure (watermark should be added automatically via patched save method)
    output_path = output_dir / "image_watermark_altair.html"
    chart.save(str(output_path))
    
    print(f"   ✓ Altair figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Altair test failed: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
sane_figs.reset()

print("\n" + "=" * 60)
print("Image watermark testing complete!")
print(f"Output files saved to: {output_dir.absolute()}")
print("=" * 60)
