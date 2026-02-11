"""
YAML preset usage example for sane-figs.

This example demonstrates how to use YAML-based presets with sane-figs.
"""

import matplotlib.pyplot as plt
import numpy as np

# Import sane-figs
import sane_figs

# Create some data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x + np.pi / 4)

# Example 1: Load a single preset from a YAML file
print("Example 1: Load a single preset from a YAML file")
print("-" * 50)
preset = sane_figs.load_preset_from_file("examples/presets/my_custom_preset.yaml")
print(f"Loaded preset: {preset.name}")
print(f"Mode: {preset.mode}")
print(f"Figure size: {preset.figure_size}")
print(f"DPI: {preset.dpi}")
print()

# Apply the loaded preset
sane_figs.setup(mode=preset.name)

plt.figure()
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.title("Custom Preset Example")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("yaml_preset_example_1.png", dpi=300, bbox_inches="tight")
plt.close()
print("Figure saved as 'yaml_preset_example_1.png'")
print()

# Example 2: Load multiple presets from a YAML file
print("Example 2: Load multiple presets from a YAML file")
print("-" * 50)
presets = sane_figs.load_presets_from_file("examples/presets/multi_presets.yaml")
print(f"Loaded {len(presets)} presets:")
for p in presets:
    print(f"  - {p.name}")
print()

# Use one of the loaded presets
sane_figs.setup(mode="nature-journal")

plt.figure()
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.plot(x, y3, label="sin(x + π/4)")
plt.title("Nature Journal Preset")
plt.xlabel("x (radians)")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("yaml_preset_example_2.png", dpi=300, bbox_inches="tight")
plt.close()
print("Figure saved as 'yaml_preset_example_2.png'")
print()

# Example 3: List all available presets
print("Example 3: List all available presets")
print("-" * 50)
all_presets = sane_figs.list_presets()
print(f"Available presets: {all_presets}")
print()

# Example 4: Get a preset by name
print("Example 4: Get a preset by name")
print("-" * 50)
preset = sane_figs.get_preset("article")
print(f"Preset name: {preset.name}")
print(f"Mode: {preset.mode}")
print(f"Figure size: {preset.figure_size}")
print(f"DPI: {preset.dpi}")
print(f"Font sizes: {preset.font_size}")
print()

# Example 5: Create and register a custom preset programmatically
print("Example 5: Create and register a custom preset programmatically")
print("-" * 50)
custom_preset = sane_figs.Preset(
    name="my-programmatic-preset",
    mode="custom",
    figure_size=(9.0, 6.0),
    dpi=300,
    font_family="sans-serif",
    font_size={
        "title": 18.0,
        "label": 16.0,
        "legend": 14.0,
        "tick": 14.0,
        "annotation": 14.0,
    },
    line_width=2.5,
    marker_size=10.0,
    colorway=sane_figs.get_colorway("vibrant"),
)
sane_figs.register_preset(custom_preset)
print(f"Registered custom preset: {custom_preset.name}")
print()

# Apply the custom preset
sane_figs.setup(mode="my-programmatic-preset")

plt.figure()
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.title("Programmatic Custom Preset")
plt.xlabel("x (radians)")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("yaml_preset_example_3.png", dpi=300, bbox_inches="tight")
plt.close()
print("Figure saved as 'yaml_preset_example_3.png'")
print()

# Example 6: Use context manager with a loaded preset
print("Example 6: Use context manager with a loaded preset")
print("-" * 50)
with sane_figs.publication_style(mode="science-journal"):
    plt.figure()
    plt.plot(x, y1, label="sin(x)")
    plt.plot(x, y2, label="cos(x)")
    plt.title("Context Manager with Science Journal Preset")
    plt.xlabel("x (radians)")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.savefig("yaml_preset_example_4.png", dpi=300, bbox_inches="tight")
    plt.close()
print("Figure saved as 'yaml_preset_example_4.png'")
print()

# Example 7: Load colorways from YAML
print("Example 7: Load colorways from YAML")
print("-" * 50)
from sane_figs.core.yaml_parser import load_colorways_from_yaml

colorways = load_colorways_from_yaml("examples/presets/custom_colorways.yaml")
print(f"Loaded {len(colorways)} colorways:")
for c in colorways:
    print(f"  - {c.name}: {c.description}")
    # Register the colorways
    sane_figs.register_colorway(c)
print()

# Use a custom colorway
sane_figs.setup(mode="article", colorway="my-lab-colors")

plt.figure()
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.title("Custom Colorway Example")
plt.xlabel("x (radians)")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("yaml_preset_example_5.png", dpi=300, bbox_inches="tight")
plt.close()
print("Figure saved as 'yaml_preset_example_5.png'")
print()

print("All examples completed successfully!")
print()
print("Summary:")
print("  - YAML files allow you to define custom presets")
print("  - Presets can be loaded from files and registered")
print("  - You can use presets by name with setup() and publication_style()")
print("  - Colorways can also be defined in YAML files")
print("  - The system is library-agnostic and human-readable")
