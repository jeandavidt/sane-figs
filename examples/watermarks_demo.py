"""
Watermarks demo for sane-figs.

This example demonstrates how to add watermarks to figures.
"""

import matplotlib.pyplot as plt
import numpy as np

# Import sane-figs
import sane_figs

# Create some data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Text watermark example
print("Creating figure with text watermark...")
sane_figs.setup(mode='article', watermark='© 2025 My Lab')

plt.figure(figsize=(6.4, 4.8))
plt.plot(x, y1, label='sin(x)', linewidth=1.5)
plt.plot(x, y2, label='cos(x)', linewidth=1.5)
plt.title('Trigonometric Functions', fontsize=14, fontweight='bold')
plt.xlabel('x (radians)', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('watermark_text.png', dpi=300, bbox_inches='tight')
plt.close()

print("Figure saved as 'watermark_text.png'")

# Custom text watermark example
print("\nCreating figure with custom text watermark...")
watermark_config = sane_figs.create_text_watermark(
    text='Draft - Do Not Distribute',
    position='center',
    opacity=0.5,
    font_size=20,
    font_weight='bold',
    font_color='#FF0000'
)

sane_figs.setup(mode='article', watermark=watermark_config)

plt.figure(figsize=(6.4, 4.8))
plt.plot(x, y1, label='sin(x)', linewidth=1.5)
plt.plot(x, y2, label='cos(x)', linewidth=1.5)
plt.title('Trigonometric Functions', fontsize=14, fontweight='bold')
plt.xlabel('x (radians)', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('watermark_custom_text.png', dpi=300, bbox_inches='tight')
plt.close()

print("Figure saved as 'watermark_custom_text.png'")

# Image watermark example (if you have an image file)
# Uncomment the following lines to test image watermark
# print("\nCreating figure with image watermark...")
# watermark_config = sane_figs.create_image_watermark(
#     'logo.png',
#     position='bottom-right',
#     opacity=0.2,
#     scale=0.1
# )
#
# sane_figs.setup(mode='article', watermark=watermark_config)
#
# plt.figure(figsize=(6.4, 4.8))
# plt.plot(x, y1, label='sin(x)', linewidth=1.5)
# plt.plot(x, y2, label='cos(x)', linewidth=1.5)
# plt.title('Trigonometric Functions', fontsize=14, fontweight='bold')
# plt.xlabel('x (radians)', fontsize=12)
# plt.ylabel('y', fontsize=12)
# plt.legend(fontsize=10)
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig('watermark_image.png', dpi=300, bbox_inches='tight')
# plt.close()
#
# print("Figure saved as 'watermark_image.png'")

print("\nWatermark features:")
print("  - Text watermarks: Add text overlays (copyright, draft status, etc.)")
print("  - Image watermarks: Add logo or brand images")
print("  - Positioning: 5 standard positions (top-left, top-right, bottom-left, bottom-right, center)")
print("  - Opacity control: Adjustable transparency (0.0 to 1.0)")
print("  - Scaling: Size control relative to figure size")
print("  - Custom styling: Font size, font family, font weight, font color")
