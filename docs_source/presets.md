# Configuring Custom Presets

Sane-Figs allows you to create custom presets using YAML files. This gives you full control over figure styling without writing Python code.

## Built-in Presets

Sane-Figs comes with two built-in presets:

- **Article Mode**: Optimized for print publication (smaller fonts, higher DPI)
- **Presentation Mode**: Optimized for slides (larger fonts, lower DPI)

```python
import sane_figs

# Use built-in presets
sane_figs.setup(mode='article')
sane_figs.setup(mode='presentation')
```

## Creating Custom Presets

Create a YAML file to define your custom preset. You can either specify all fields explicitly, or use the `base` field to inherit from an existing preset and only override specific values.

### Using Inheritance (Recommended)

The `base` field allows you to inherit all settings from an existing preset (like `article` or `presentation`) and only override the fields you want to change:

```yaml
name: "my-journal-preset"
base: "article"  # Inherit all settings from article preset

# Only override specific fields
figure:
  size: [7.0, 5.0]  # Larger figure size

typography:
  font_family: "serif"  # Use serif font
  font_sizes:
    title: 16.0  # Larger title

# All other settings (dpi, line_width, etc.) are inherited from "article"
```

Available base presets include: `article`, `presentation`, `ulaval`, `modeleau`, `marimo`, `latex`, or any previously registered custom preset.

### Full Custom Preset (Without Inheritance)

If you don't specify a `base`, you must provide all required fields:

```yaml
name: "my-custom-preset"
# No 'base' specified - must define all required fields

# Figure settings (required)
figure:
  size: [8.0, 6.0]  # [width, height] in inches
  dpi: 300

# Typography settings
typography:
  font_family: "sans-serif"
  font_sizes:
    title: 16.0
    label: 14.0
    legend: 12.0
    tick: 12.0
    annotation: 12.0

# Line and marker settings
elements:
  line_width: 2.0
  marker_size: 8.0

# Colorway reference
colorway:
  name: "nature"

# Watermark settings (optional)
watermark:
  type: "text"
  text: "© 2025 My Lab"
  position: "bottom-right"
  opacity: 0.3
```

### Font Size Merging

When using inheritance, `font_sizes` are merged with the base preset. You only need to specify the sizes you want to override:

```yaml
name: "large-title-preset"
base: "article"

typography:
  font_sizes:
    title: 20.0  # Only override title, keep other sizes from article
```

## Using Custom Presets

### Load and Use a Preset

```python
import sane_figs

# Load a preset from a YAML file
preset = sane_figs.load_preset('my_preset.yaml')
sane_figs.setup(preset=preset)
```

### Register Multiple Presets

```python
import sane_figs

# Load all presets from a file
presets = sane_figs.load_presets('presets.yaml')
for preset in presets:
    sane_figs.register_preset(preset)

# Use a registered preset by name
sane_figs.setup(mode='my-custom-preset')
```

## Preset Properties

### Figure Settings

| Property | Type | Article Default | Presentation Default | Description |
|----------|------|-----------------|---------------------|-------------|
| `size` | `[width, height]` | `[3.5, 2.625]` | `[13.33, 7.5]` | Figure size in inches |
| `dpi` | `int` | `300` | `150` | Dots per inch |

### Typography Settings

| Property | Type | Article Default | Presentation Default | Description |
|----------|------|-----------------|---------------------|-------------|
| `font_family` | `str` | `"sans-serif"` | `"sans-serif"` | Font family |
| `font_sizes.title` | `float` | `9.0` | `28.0` | Title font size |
| `font_sizes.label` | `float` | `8.0` | `24.0` | Axis label font size |
| `font_sizes.legend` | `float` | `7.0` | `20.0` | Legend font size |
| `font_sizes.tick` | `float` | `7.0` | `20.0` | Tick label font size |
| `font_sizes.annotation` | `float` | `7.0` | `20.0` | Annotation font size |

### Element Settings

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `line_width` | `float` | `1.5` | Line width for plots |
| `marker_size` | `float` | `6.0` | Marker size for scatter plots |

## Multiple Presets in One File

You can define multiple presets in a single YAML file:

```yaml
presets:
  - name: "small-print"
    base: "article"
    figure:
      size: [4.0, 3.0]
    typography:
      font_sizes:
        title: 12.0
        label: 10.0
        legend: 8.0
        tick: 8.0

  - name: "large-poster"
    base: "presentation"
    figure:
      size: [16.0, 12.0]
    typography:
      font_sizes:
        title: 36.0
        label: 28.0
        legend: 24.0
        tick: 24.0
```

Each preset can use a different `base` to inherit from, making it easy to create variations optimized for different use cases.

## Example: Custom Preset for Journal Submission

```yaml
name: "nature-journal"
base: "article"  # Start with article preset

figure:
  size: [7.0, 5.0]  # Nature's recommended single column size

typography:
  font_family: "Arial"
  font_sizes:
    title: 14.0
    label: 12.0

colorway:
  name: "colorblind-safe"
```

This preset inherits the DPI, line width, and other settings from the `article` preset while customizing the figure size, font family, and font sizes for Nature's requirements.

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Load and use the custom preset
preset = sane_figs.load_preset('nature_journal.yaml')
sane_figs.setup(preset=preset)

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.savefig('figure.png')
```

![Nature Journal Preset Example](assets/images/presets_example.png)

