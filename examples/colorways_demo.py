"""
Colorways demo for sane-figs.

This example demonstrates the different colorways available in sane-figs.
"""

import matplotlib.pyplot as plt
import numpy as np

# Import sane-figs
import sane_figs

# Create some data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x + np.pi/4)
y4 = np.cos(x + np.pi/4)
y5 = np.sin(x + np.pi/2)

# List available colorways
print("Available colorways:")
for colorway_name in sane_figs.list_colorways():
    colorway = sane_figs.get_colorway(colorway_name)
    print(f"  - {colorway_name}: {colorway.description}")

# Create figures with different colorways
colorways = ['default', 'nature', 'vibrant', 'pastel', 'colorblind-safe']

for colorway_name in colorways:
    # Apply article mode with the colorway
    sane_figs.setup(mode='article', colorway=colorway_name)

    # Create a figure
    plt.figure(figsize=(6.4, 4.8))
    plt.plot(x, y1, label='sin(x)', linewidth=1.5)
    plt.plot(x, y2, label='cos(x)', linewidth=1.5)
    plt.plot(x, y3, label='sin(x + π/4)', linewidth=1.5)
    plt.plot(x, y4, label='cos(x + π/4)', linewidth=1.5)
    plt.plot(x, y5, label='sin(x + π/2)', linewidth=1.5)
    plt.title(f'Trigonometric Functions - {colorway_name.capitalize()} Colorway',
              fontsize=14, fontweight='bold')
    plt.xlabel('x (radians)', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'colorway_{colorway_name}.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure saved as 'colorway_{colorway_name}.png'")

print("\nColorway descriptions:")
print("  - default: Publication-ready palette optimized for print")
print("  - nature: Earth tones inspired by nature")
print("  - vibrant: High contrast colors optimized for presentations")
print("  - pastel: Soft, professional colors")
print("  - colorblind-safe: Designed for colorblind accessibility")
