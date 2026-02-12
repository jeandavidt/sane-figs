"""
Test watermark functionality across all 4 supported plotting libraries.

This script creates watermarked figures using Matplotlib, Seaborn, Plotly, and Altair
to verify the watermark feature works correctly.
"""

import os
import sys
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

print("=" * 60)
print("Testing Watermark Feature Across All Libraries")
print("=" * 60)

# Test 1: Matplotlib
print("\n1. Testing Matplotlib watermark...")
try:
    import matplotlib.pyplot as plt
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with watermark
    sane_figs.setup(
        mode='article',
        libraries=['matplotlib'],
        watermark=sane_figs.create_text_watermark(
            text='© 2025 My Lab',
            position='bottom-right',
            opacity=0.5,
            font_size=14,
        )
    )
    
    # Create figure
    plt.figure(figsize=(8, 5))
    plt.plot(x, y1, label='sin(x)', linewidth=1.5)
    plt.plot(x, y2, label='cos(x)', linewidth=1.5)
    plt.title('Matplotlib Watermark Test')
    plt.xlabel('x (radians)')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure (watermark should be added automatically)
    output_path = output_dir / "watermark_matplotlib.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Matplotlib figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Matplotlib test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Seaborn
print("\n2. Testing Seaborn watermark...")
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with watermark
    sane_figs.setup(
        mode='article',
        libraries=['seaborn'],
        watermark=sane_figs.create_text_watermark(
            text='DRAFT',
            position='center',
            opacity=0.3,
            font_size=40,
            font_weight='bold',
            font_color='gray',
        )
    )
    
    # Create figure using seaborn
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='x', y='sin(x)', label='sin(x)')
    sns.lineplot(data=df, x='x', y='cos(x)', label='cos(x)')
    plt.title('Seaborn Watermark Test')
    plt.xlabel('x (radians)')
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    
    # Save figure (watermark should be added automatically)
    output_path = output_dir / "watermark_seaborn.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Seaborn figure saved to {output_path}")
except Exception as e:
    print(f"   ✗ Seaborn test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Plotly
print("\n3. Testing Plotly watermark...")
try:
    import plotly.graph_objects as go
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with watermark
    sane_figs.setup(
        mode='article',
        libraries=['plotly'],
        watermark=sane_figs.create_text_watermark(
            text='© My Research Group',
            position='top-left',
            opacity=0.4,
            font_size=12,
        )
    )
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='sin(x)'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='cos(x)'))
    fig.update_layout(
        title='Plotly Watermark Test',
        xaxis_title='x (radians)',
        yaxis_title='y',
    )
    
    # Save figure
    output_path = output_dir / "watermark_plotly.html"
    fig.write_html(str(output_path))
    
    # Also save as image if kaleido is available
    try:
        output_path_png = output_dir / "watermark_plotly.png"
        fig.write_image(str(output_path_png), scale=1)
        print(f"   ✓ Plotly figure saved to {output_path} and {output_path_png}")
    except Exception:
        print(f"   ✓ Plotly figure saved to {output_path} (PNG requires kaleido)")
except Exception as e:
    print(f"   ✗ Plotly test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Altair
print("\n4. Testing Altair watermark...")
try:
    import altair as alt
    
    # Reset any previous state
    sane_figs.reset()
    
    # Setup with watermark
    sane_figs.setup(
        mode='article',
        libraries=['altair'],
        watermark=sane_figs.create_text_watermark(
            text='CONFIDENTIAL',
            position='bottom-right',
            opacity=0.5,
            font_size=14,
        )
    )
    
    # Create base chart
    base = alt.Chart(df).encode(x='x:Q')
    
    chart = (
        base.mark_line(color='blue')
        .encode(y='sin(x):Q')
        .properties(title='Altair Watermark Test', width=600, height=400)
    )
    
    # Save figure (watermark should be added automatically via patched save method)
    output_path = output_dir / "watermark_altair.json"
    chart.save(str(output_path))
    
    # Also save as HTML
    output_path_html = output_dir / "watermark_altair.html"
    chart.save(str(output_path_html))
    
    print(f"   ✓ Altair figure saved to {output_path} and {output_path_html}")
except Exception as e:
    print(f"   ✗ Altair test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Different positions with Matplotlib
print("\n5. Testing different watermark positions...")
positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']

for pos in positions:
    try:
        import matplotlib.pyplot as plt
        
        # Reset any previous state
        sane_figs.reset()
        
        # Setup with watermark at different position
        sane_figs.setup(
            mode='article',
            libraries=['matplotlib'],
            watermark=sane_figs.create_text_watermark(
                text=f'Position: {pos}',
                position=pos,
                opacity=0.5,
                font_size=12,
            )
        )
        
        # Create figure
        plt.figure(figsize=(6, 4))
        plt.plot(x, y1, label='sin(x)')
        plt.title(f'Watermark Position: {pos}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        output_path = output_dir / f"watermark_pos_{pos.replace('-', '_')}.png"
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"   ✓ Position '{pos}' saved to {output_path}")
    except Exception as e:
        print(f"   ✗ Position '{pos}' test failed: {e}")

# Cleanup
sane_figs.reset()

print("\n" + "=" * 60)
print("Watermark testing complete!")
print(f"Output files saved to: {output_dir.absolute()}")
print("=" * 60)
