"""
Context manager example for sane-figs.

This example demonstrates how to use the context manager to apply
publication-ready styling to a specific block of code.
"""

import matplotlib.pyplot as plt
import numpy as np

# Import sane-figs
import sane_figs

# Create some data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create a figure with default styling
plt.figure()
plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')
plt.title('Default Styling')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('default_styling.png')
plt.close()

print("Figure saved as 'default_styling.png' (with default matplotlib styling)")

# Create a figure with publication styling using context manager
with sane_figs.publication_style(mode='article'):
    plt.figure()
    plt.plot(x, y1, label='sin(x)')
    plt.plot(x, y2, label='cos(x)')
    plt.title('Publication Styling')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('publication_styling.png')
    plt.close()

print("Figure saved as 'publication_styling.png' (with publication-ready styling)")

# Create another figure - styling is reset to default
plt.figure()
plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')
plt.title('Back to Default Styling')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('back_to_default.png')
plt.close()

print("Figure saved as 'back_to_default.png' (back to default matplotlib styling)")
print("\nThe context manager applies styling only within the 'with' block.")
print("After the block exits, styling is reset to the original state.")
