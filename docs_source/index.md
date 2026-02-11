# Sane-Figs

Publication-ready figures for Matplotlib, Seaborn, Plotly, and Altair.

## Installation

```bash
pip install sane-figs
```

## Quick Start

```python
import sane_figs
import matplotlib.pyplot as plt

sane_figs.setup(mode='article')

plt.plot([1, 2, 3], [1, 4, 9])
plt.title('My Figure')
plt.savefig('figure.png', dpi=300)
```

## Examples

### Basic Usage

![Basic Usage](images/basic_usage.png)

```python
import matplotlib.pyplot as plt
import numpy as np
import sane_figs

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.savefig('docs/images/basic_usage.png', dpi=300)
```

### Article Mode

![Article Mode](images/article_mode.png)

```python
import matplotlib.pyplot as plt
import numpy as np
import sane_figs

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')
plt.legend()
plt.title('Trigonometric Functions')
plt.savefig('docs/images/article_mode.png', dpi=300)
```

### Colorways

![Default Colorway](images/colorway_default.png)
![Nature Colorway](images/colorway_nature.png)
![Vibrant Colorway](images/colorway_vibrant.png)

```python
import matplotlib.pyplot as plt
import numpy as np
import sane_figs

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
    plt.savefig(f'docs/images/colorway_{colorway}.png', dpi=300)
    plt.close()
```

### Presentation Mode

![Presentation Mode](images/presentation_mode.png)

```python
import matplotlib.pyplot as plt
import numpy as np
import sane_figs

sane_figs.setup(mode='presentation')

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y, linewidth=2)
plt.title('Sine Wave (Presentation Mode)')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.savefig('docs/images/presentation_mode.png', dpi=150)
```

## License

MIT License
