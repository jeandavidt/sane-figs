# Matplotlib

Sane-Figs provides full support for Matplotlib, automatically applying publication-ready styling to your figures.

## Installation

```bash
pip install sane-figs[matplotlib]
```

## Basic Usage

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Apply publication defaults
sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.savefig('figure.png', dpi=300)
```

![Basic Matplotlib Example](../assets/images/matplotlib_basic.png)

## Line Plots

### Simple Line Plot

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Simple Line Plot')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True, alpha=0.3)
plt.savefig('line_plot.png', dpi=300)
```

![Simple Line Plot](../assets/images/matplotlib_line.png)

### Multiple Lines

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x + np.pi/4)

plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')
plt.plot(x, y3, label='sin(x + π/4)')
plt.legend()
plt.title('Multiple Lines')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.savefig('multiple_lines.png', dpi=300)
```

![Multiple Lines](../assets/images/matplotlib_multiple_lines.png)

## Scatter Plots

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)

plt.scatter(x, y, c=colors, s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
plt.title('Scatter Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar(label='Value')
plt.grid(True, alpha=0.3)
plt.savefig('scatter_plot.png', dpi=300)
```

![Scatter Plot](../assets/images/matplotlib_scatter.png)

## Bar Charts

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

plt.bar(categories, values, edgecolor='black', linewidth=0.5)
plt.title('Bar Chart')
plt.xlabel('Category')
plt.ylabel('Value')
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('bar_chart.png', dpi=300)
```

![Bar Chart](../assets/images/matplotlib_bar.png)

## Histograms

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(1000)

plt.hist(data, bins=30, edgecolor='black', linewidth=0.5, alpha=0.7)
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('histogram.png', dpi=300)
```

![Histogram](../assets/images/matplotlib_histogram.png)

## Subplots

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2.625))

ax1.plot(x, y1)
ax1.set_title('Sine Wave')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')
ax1.grid(True, alpha=0.3)

ax2.plot(x, y2)
ax2.set_title('Cosine Wave')
ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('subplots.png', dpi=300)
```

![Subplots](../assets/images/matplotlib_subplots.png)

## Using Colorways

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
plt.title('Nature Colorway')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.savefig('colorway_example.png', dpi=300)
```

![Colorway Example](../assets/images/matplotlib_colorway.png)

## Using Watermarks

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(
    mode='article',
    watermark='© 2025 My Lab'
)

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Figure with Watermark')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True, alpha=0.3)
plt.savefig('watermark_example.png', dpi=300)
```

![Watermark Example](../assets/images/matplotlib_watermark.png)

## Context Manager

For scoped styling, use the context manager:

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Apply styling only within the context
with sane_figs.publication_style(mode='article'):
    plt.plot(x, y)
    plt.title('Styled Figure')
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.savefig('styled.png', dpi=300)

# Styling is reset after the context
plt.plot(x, y)  # Back to default styling
plt.title('Unstyled Figure')
plt.savefig('unstyled.png')
```

## Per-Library Setup

You can also use the Matplotlib-specific setup function:

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib-specific setup
sane_figs.setup_matplotlib(mode='article', colorway='nature')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Matplotlib-Specific Setup')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.savefig('matplotlib_specific.png', dpi=300)
```

## Tips for Matplotlib

1. **Use `tight_layout()`**: Always call `plt.tight_layout()` before saving to prevent label cutoff
2. **Set DPI**: Use `dpi=300` for print, `dpi=150` for presentations
3. **Use `bbox_inches='tight'`**: Prevents whitespace around the figure
4. **Close figures**: Always call `plt.close()` after saving to free memory
5. **Use subplots**: For multiple plots, use `plt.subplots()` for better control

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Best Practices')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True, alpha=0.3)
plt.tight_layout()  # Prevent label cutoff
plt.savefig('best_practices.png', dpi=300, bbox_inches='tight')
plt.close()  # Free memory
```
