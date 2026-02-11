"""
Basic usage example for sane-figs.

This example demonstrates how to use sane-figs to apply publication-ready
styling to Matplotlib figures.
"""

import matplotlib.pyplot as plt
import numpy as np

# Import sane-figs
import sane_figs

# Apply publication defaults globally
sane_figs.setup(mode='article')

# Your existing code works as-is
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure()
plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')
plt.title('Trigonometric Functions')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.savefig('basic_example.png', dpi=300)
plt.close()

print("Figure saved as 'basic_example.png'")
print("The figure has publication-ready styling with:")
print("  - Appropriate font sizes (title: 14pt, labels: 12pt, legend: 10pt)")
print("  - High resolution (300 DPI)")
print("  - Publication-ready color palette")
print("  - Clean grid and spines")
