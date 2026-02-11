"""
Presentation mode example for sane-figs.

This example demonstrates the presentation mode preset, which is optimized
for slides and presentations.
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

# Apply presentation mode
sane_figs.setup(mode='presentation')

# Create a figure with presentation mode styling
plt.figure(figsize=(10, 7.5))
plt.plot(x, y1, label='sin(x)', linewidth=3.0)
plt.plot(x, y2, label='cos(x)', linewidth=3.0)
plt.plot(x, y3, label='sin(x + π/4)', linewidth=3.0)
plt.title('Trigonometric Functions', fontsize=24, fontweight='bold')
plt.xlabel('x (radians)', fontsize=20)
plt.ylabel('y', fontsize=20)
plt.legend(fontsize=16)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('presentation_mode.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figure saved as 'presentation_mode.png'")
print("\nPresentation mode settings:")
print("  - Figure size: (10, 7.5) inches")
print("  - DPI: 150 (sufficient for projection)")
print("  - Title font size: 24pt")
print("  - Axis label font size: 20pt")
print("  - Legend font size: 16pt")
print("  - Tick label font size: 16pt")
print("  - Line width: 3.0")
print("  - Marker size: 10.0")
print("  - Colorway: vibrant (high contrast for projection)")
print("\nThese settings are optimized for slides and presentations.")
