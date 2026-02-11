"""
Article mode example for sane-figs.

This example demonstrates the article mode preset, which is optimized
for print publication.
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

# Apply article mode
sane_figs.setup(mode='article')

# Create a figure with article mode styling
plt.figure(figsize=(6.4, 4.8))
plt.plot(x, y1, label='sin(x)', linewidth=1.5)
plt.plot(x, y2, label='cos(x)', linewidth=1.5)
plt.plot(x, y3, label='sin(x + π/4)', linewidth=1.5)
plt.title('Trigonometric Functions', fontsize=14, fontweight='bold')
plt.xlabel('x (radians)', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('article_mode.png', dpi=300, bbox_inches='tight')
plt.close()

print("Figure saved as 'article_mode.png'")
print("\nArticle mode settings:")
print("  - Figure size: (6.4, 4.8) inches")
print("  - DPI: 300 (high resolution for print)")
print("  - Title font size: 14pt")
print("  - Axis label font size: 12pt")
print("  - Legend font size: 10pt")
print("  - Tick label font size: 10pt")
print("  - Line width: 1.5")
print("  - Marker size: 6.0")
print("  - Colorway: default (publication-ready palette)")
print("\nThese settings are optimized for print publication in journals.")
