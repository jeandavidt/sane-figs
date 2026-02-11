# Sane-Figs

Publication-ready figures for Matplotlib, Seaborn, Plotly, and Altair.

## Overview

Sane-Figs is a Python package that automatically applies publication-ready styling to figures generated with popular Python visualization libraries. It solves the common problem of figures having text that is too small for articles and presentations.

## Features

- **Automatic Styling**: Apply publication-ready defaults with a single function call
- **Multiple Libraries**: Support for Matplotlib, Seaborn, Plotly, and Altair
- **Version-Aware**: Automatically detects library versions and adapts to API changes
- **Two Usage Modes**: Global setup or context manager for scoped styling
- **Presets**: Built-in presets for articles and presentations
- **Colorways**: Publication-ready color palettes (default, nature, vibrant, pastel, colorblind-safe)
- **Watermarks**: Text and image watermark support

## Installation

```bash
pip install sane-figs
```

For full library support:

```bash
pip install sane-figs[all]
```

Or install with specific libraries:

```bash
pip install sane-figs[matplotlib,seaborn]
```

## Quick Start

### Global Setup

```python
import sane_figs
import matplotlib.pyplot as plt

# Apply publication defaults globally
sane_figs.setup(mode='article')

# Your existing code works as-is
plt.plot([1, 2, 3], [1, 4, 9])
plt.title('My Figure')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.savefig('figure.png', dpi=300)
```

### Context Manager

```python
import sane_figs
import matplotlib.pyplot as plt

# Scoped styling
with sane_figs.publication_style(mode='article'):
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.title('My Figure')
    plt.savefig('figure.png')

# Styling resets after context
plt.plot([1, 2, 3], [1, 4, 9])  # Back to default styling
```

### With Colorways

```python
import sane_figs
import matplotlib.pyplot as plt

# Apply colorway
sane_figs.setup(mode='article', colorway='nature')

# List available colorways
print(sane_figs.list_colorways())
# ['default', 'nature', 'vibrant', 'pastel', 'colorblind-safe']
```

### With Watermarks

```python
import sane_figs
import matplotlib.pyplot as plt

# Text watermark
sane_figs.setup(mode='article', watermark='© 2025 My Lab')

# Image watermark
sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_image_watermark('logo.png', opacity=0.2)
)
```

## Presets

### Article Mode

Optimized for print publication:
- Figure size: (6.4, 4.8) inches
- DPI: 300
- Title: 14pt
- Axis labels: 12pt
- Legend: 10pt
- Tick labels: 10pt

### Presentation Mode

Optimized for slides:
- Figure size: (10, 7.5) inches
- DPI: 150
- Title: 24pt
- Axis labels: 20pt
- Legend: 16pt
- Tick labels: 16pt

## Colorways

- **default**: Publication-ready palette optimized for print
- **nature**: Earth tones inspired by nature
- **vibrant**: High contrast colors for presentations
- **pastel**: Soft, professional colors
- **colorblind-safe**: Designed for colorblind accessibility

## API Reference

### Main Functions

- `setup(mode='article', libraries=None, colorway=None, watermark=None)` - Apply publication defaults globally
- `publication_style(mode='article', libraries=None, colorway=None, watermark=None)` - Context manager for scoped styling
- `list_colorways()` - List available colorways
- `create_text_watermark(text, **kwargs)` - Create a text watermark configuration
- `create_image_watermark(image_path, **kwargs)` - Create an image watermark configuration

### Per-Library Functions

- `setup_matplotlib(mode='article', colorway=None, watermark=None)`
- `setup_seaborn(mode='article', colorway=None, watermark=None)`
- `setup_plotly(mode='article', colorway=None, watermark=None)`
- `setup_altair(mode='article', colorway=None, watermark=None)`

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
