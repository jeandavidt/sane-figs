# Seaborn

Sane-Figs provides full support for Seaborn, automatically applying publication-ready styling to your statistical visualizations.

## Installation

```bash
pip install sane-figs[seaborn]
```

## Basic Usage

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Apply publication defaults
sane_figs.setup(mode='article')

# Create sample data
np.random.seed(42)
data = np.random.randn(100)

# Create a simple plot
sns.histplot(data)
plt.title('Histogram with Seaborn')
plt.savefig('figure.png', dpi=300)
```

![Basic Seaborn Example](../assets/images/seaborn_basic.png)

## Distribution Plots

### Histogram

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(1000)

sns.histplot(data, bins=30, kde=True, edgecolor='black', linewidth=0.5)
plt.title('Histogram with KDE')
plt.xlabel('Value')
plt.ylabel('Count')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_histogram.png', dpi=300)
plt.close()
```

![Seaborn Histogram](../assets/images/seaborn_histogram.png)

### Box Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]

sns.boxplot(data=data)
plt.title('Box Plot')
plt.xlabel('Group')
plt.ylabel('Value')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_boxplot.png', dpi=300)
plt.close()
```

![Seaborn Box Plot](../assets/images/seaborn_boxplot.png)

### Violin Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]

sns.violinplot(data=data)
plt.title('Violin Plot')
plt.xlabel('Group')
plt.ylabel('Value')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_violin.png', dpi=300)
plt.close()
```

![Seaborn Violin Plot](../assets/images/seaborn_violin.png)

## Categorical Plots

### Bar Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
categories = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(10, 100, 5)

sns.barplot(x=categories, y=values, edgecolor='black', linewidth=0.5)
plt.title('Bar Plot')
plt.xlabel('Category')
plt.ylabel('Value')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_barplot.png', dpi=300)
plt.close()
```

![Seaborn Bar Plot](../assets/images/seaborn_barplot.png)

### Count Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
categories = np.random.choice(['A', 'B', 'C', 'D', 'E'], 100)

sns.countplot(x=categories, edgecolor='black', linewidth=0.5)
plt.title('Count Plot')
plt.xlabel('Category')
plt.ylabel('Count')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_countplot.png', dpi=300)
plt.close()
```

![Seaborn Count Plot](../assets/images/seaborn_countplot.png)

## Relational Plots

### Scatter Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)

sns.scatterplot(x=x, y=y, s=50, alpha=0.7, edgecolor='black', linewidth=0.5)
plt.title('Scatter Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('seaborn_scatter.png', dpi=300)
plt.close()
```

![Seaborn Scatter Plot](../assets/images/seaborn_scatter.png)

### Line Plot

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

sns.lineplot(x=x, y=y)
plt.title('Line Plot')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('seaborn_lineplot.png', dpi=300)
plt.close()
```

![Seaborn Line Plot](../assets/images/seaborn_lineplot.png)

## Matrix Plots

### Heatmap

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(10, 10)

sns.heatmap(data, cmap='coolwarm', center=0, annot=False, cbar_kws={'label': 'Value'})
plt.title('Heatmap')
plt.tight_layout()
plt.savefig('seaborn_heatmap.png', dpi=300)
plt.close()
```

![Seaborn Heatmap](../assets/images/seaborn_heatmap.png)

## Regression Plots

### Linear Regression

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
x = np.random.randn(100)
y = 2 * x + np.random.randn(100)

sns.regplot(x=x, y=y, scatter_kws={'s': 50, 'alpha': 0.7})
plt.title('Linear Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('seaborn_regplot.png', dpi=300)
plt.close()
```

![Seaborn Regression Plot](../assets/images/seaborn_regplot.png)

## Using Colorways

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article', colorway='nature')

np.random.seed(42)
categories = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(10, 100, 5)

sns.barplot(x=categories, y=values, edgecolor='black', linewidth=0.5)
plt.title('Nature Colorway')
plt.xlabel('Category')
plt.ylabel('Value')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_colorway.png', dpi=300)
plt.close()
```

![Seaborn Colorway](../assets/images/seaborn_colorway.png)

## Using Watermarks

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article', watermark='© 2025 My Lab')

np.random.seed(42)
data = np.random.randn(1000)

sns.histplot(data, bins=30, kde=True, edgecolor='black', linewidth=0.5)
plt.title('Figure with Watermark')
plt.xlabel('Value')
plt.ylabel('Count')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_watermark.png', dpi=300)
plt.close()
```

![Seaborn Watermark](../assets/images/seaborn_watermark.png)

## Per-Library Setup

You can also use the Seaborn-specific setup function:

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Seaborn-specific setup
sane_figs.setup_seaborn(mode='article', colorway='nature')

np.random.seed(42)
data = np.random.randn(1000)

sns.histplot(data, bins=30, kde=True)
plt.title('Seaborn-Specific Setup')
plt.xlabel('Value')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('seaborn_specific.png', dpi=300)
plt.close()
```

## Tips for Seaborn

1. **Use `tight_layout()`**: Always call `plt.tight_layout()` before saving
2. **Set DPI**: Use `dpi=300` for print, `dpi=150` for presentations
3. **Close figures**: Always call `plt.close()` after saving
4. **Use Seaborn themes**: Sane-Figs overrides Seaborn themes, but you can still use them
5. **Combine with Matplotlib**: You can use Matplotlib functions alongside Seaborn

```python
import sane_figs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(1000)

sns.histplot(data, bins=30, kde=True, edgecolor='black', linewidth=0.5)
plt.title('Best Practices')
plt.xlabel('Value')
plt.ylabel('Count')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('seaborn_best_practices.png', dpi=300)
plt.close()
```
