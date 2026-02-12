# Colorways

Sane-Figs provides publication-ready color palettes (colorways) that are optimized for different use cases.

## Built-in Colorways

### Default

The default colorway is optimized for print publication with high contrast and readability.

![Default Colorway](assets/images/colorway_default.png)

```python
import sane_figs
sane_figs.setup(mode='article', colorway='default')
```

### Nature

Earth tones inspired by nature, perfect for environmental and biological publications.

![Nature Colorway](assets/images/colorway_nature.png)

```python
import sane_figs
sane_figs.setup(mode='article', colorway='nature')
```

### Vibrant

High contrast colors optimized for presentations and slides.

![Vibrant Colorway](assets/images/colorway_vibrant.png)

```python
import sane_figs
sane_figs.setup(mode='article', colorway='vibrant')
```

### Pastel

Soft, professional colors suitable for business and corporate publications.

![Pastel Colorway](assets/images/colorway_pastel.png)

```python
import sane_figs
sane_figs.setup(mode='article', colorway='pastel')
```

### Colorblind-Safe

Designed for colorblind accessibility, ensuring your figures are readable by everyone.

![Colorblind-Safe Colorway](assets/images/colorway_colorblind-safe.png)

```python
import sane_figs
sane_figs.setup(mode='article', colorway='colorblind-safe')
```

## Listing Available Colorways

```python
import sane_figs

# List all available colorways
for colorway_name in sane_figs.list_colorways():
    colorway = sane_figs.get_colorway(colorway_name)
    print(f"{colorway_name}: {colorway.description}")
```

Output:
```
default: Publication-ready palette optimized for print
nature: Earth tones inspired by nature
vibrant: High contrast colors optimized for presentations
pastel: Soft, professional colors
colorblind-safe: Designed for colorblind accessibility
```

## Using Colorways

### Basic Usage

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article', colorway='nature')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x + np.pi/4)

plt.plot(x, y1, label='Series 1')
plt.plot(x, y2, label='Series 2')
plt.plot(x, y3, label='Series 3')
plt.legend()
plt.title('Nature Colorway Example')
plt.savefig('figure.png')
```

![Nature Colorway Example](assets/images/colorway_example.png)

### Multiple Plots with Different Colorways

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

for colorway in ['default', 'nature', 'vibrant']:
    sane_figs.setup(mode='article', colorway=colorway)
    plt.figure()
    plt.plot(x, y1, label='sin(x)')
    plt.plot(x, y2, label='cos(x)')
    plt.legend()
    plt.title(f'{colorway.capitalize()} Colorway')
    plt.savefig(f'colorway_{colorway}.png')
    plt.close()
```

## Colorway Properties

Each colorway contains four types of color palettes:

- **Categorical**: For discrete categories (e.g., different groups)
- **Sequential**: For ordered data (e.g., temperature gradients)
- **Diverging**: For data with a meaningful midpoint (e.g., positive/negative values)
- **Qualitative**: For nominal data without inherent order

## Choosing the Right Colorway

| Colorway | Best For | Accessibility |
|----------|----------|---------------|
| `default` | Print publications | Good |
| `nature` | Environmental/biological topics | Good |
| `vibrant` | Presentations/slides | Fair |
| `pastel` | Business/corporate | Good |
| `colorblind-safe` | General audience | Excellent |

## Custom Colorways

You can define custom colorways in YAML files:

```yaml
colorways:
  - name: "my-lab-colors"
    description: "My lab's official color palette"
    colors:
      categorical: ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
      sequential: ["#FFFFE0", "#FFFF00", "#FFD700", "#FFA500", "#FF4500"]
      diverging: ["#0000FF", "#FFFFFF", "#FF0000"]
      qualitative: ["#E63946", "#F1FAEE", "#A8DADC", "#457B9D", "#1D3557"]
```

```python
import sane_figs

# Load custom colorways
colorways = sane_figs.load_colorways('my_colorways.yaml')
for colorway in colorways:
    sane_figs.register_colorway(colorway)

# Use the custom colorway
sane_figs.setup(mode='article', colorway='my-lab-colors')
```

## Accessibility Tips

1. **Use colorblind-safe palettes** when possible
2. **Combine color with other visual cues** (line styles, markers)
3. **Test your figures** with colorblind simulation tools
4. **Provide legends** for all color-coded elements
5. **Avoid red-green combinations** for critical distinctions

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Good: Use colorblind-safe palette with different line styles
sane_figs.setup(mode='article', colorway='colorblind-safe')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label='sin(x)', linestyle='-')
plt.plot(x, y2, label='cos(x)', linestyle='--')
plt.legend()
plt.title('Accessible Figure')
plt.savefig('accessible_figure.png')
```

![Accessible Figure Example](assets/images/accessible_figure.png)
