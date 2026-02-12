# Plotly

Sane-Figs provides full support for Plotly, automatically applying publication-ready styling to your interactive visualizations.

## Installation

```bash
pip install sane-figs[plotly]
```

## Basic Usage

```python
import sane_figs
import plotly.express as px
import numpy as np

# Apply publication defaults
sane_figs.setup(mode='article')

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a simple plot
fig = px.line(x=x, y=y, title='Sine Wave')
fig.write_image('figure.png', scale=2)
```

![Basic Plotly Example](../assets/images/plotly_basic.png)

## Line Plots

### Simple Line Plot

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = px.line(x=x, y=y, title='Simple Line Plot', labels={'x': 'x', 'y': 'sin(x)'})
fig.update_layout(showlegend=True)
fig.write_image('plotly_line.png', scale=2)
```

![Plotly Line Plot](../assets/images/plotly_line.png)

### Multiple Lines

```python
import sane_figs
import plotly.express as px
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
df = pd.DataFrame({
    'x': x,
    'sin(x)': np.sin(x),
    'cos(x)': np.cos(x),
    'sin(x + π/4)': np.sin(x + np.pi/4)
})

df_long = df.melt('x', var_name='Function', value_name='y')

fig = px.line(df_long, x='x', y='y', color='Function', title='Multiple Lines')
fig.update_layout(showlegend=True)
fig.write_image('plotly_multiple_lines.png', scale=2)
```

![Plotly Multiple Lines](../assets/images/plotly_multiple_lines.png)

## Scatter Plots

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)

fig = px.scatter(x=x, y=y, color=colors, title='Scatter Plot',
                 labels={'x': 'x', 'y': 'y', 'color': 'Value'},
                 color_continuous_scale='Viridis')
fig.update_traces(marker=dict(size=8, opacity=0.7))
fig.update_layout(showlegend=True)
fig.write_image('plotly_scatter.png', scale=2)
```

![Plotly Scatter Plot](../assets/images/plotly_scatter.png)

## Bar Charts

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article')

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

fig = px.bar(x=categories, y=values, title='Bar Chart',
             labels={'x': 'Category', 'y': 'Value'})
fig.update_layout(showlegend=False)
fig.write_image('plotly_bar.png', scale=2)
```

![Plotly Bar Chart](../assets/images/plotly_bar.png)

## Histograms

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(1000)

fig = px.histogram(data, nbins=30, title='Histogram',
                   labels={'value': 'Value', 'count': 'Frequency'})
fig.update_layout(showlegend=False)
fig.write_image('plotly_histogram.png', scale=2)
```

![Plotly Histogram](../assets/images/plotly_histogram.png)

## Box Plots

```python
import sane_figs
import plotly.express as px
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
df = pd.DataFrame({
    'Group': ['A'] * 100 + ['B'] * 100 + ['C'] * 100,
    'Value': np.concatenate(data)
})

fig = px.box(df, x='Group', y='Value', title='Box Plot')
fig.update_layout(showlegend=False)
fig.write_image('plotly_box.png', scale=2, width=800, height=500)
```

![Plotly Box Plot](../assets/images/plotly_box.png)

## Violin Plots

```python
import sane_figs
import plotly.express as px
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
df = pd.DataFrame({
    'Group': ['A'] * 100 + ['B'] * 100 + ['C'] * 100,
    'Value': np.concatenate(data)
})

fig = px.violin(df, x='Group', y='Value', title='Violin Plot')
fig.update_layout(showlegend=False)
fig.write_image('plotly_violin.png', scale=2, width=800, height=500)
```

![Plotly Violin Plot](../assets/images/plotly_violin.png)

## Subplots

```python
import sane_figs
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig = make_subplots(rows=1, cols=2, subplot_titles=('Sine Wave', 'Cosine Wave'))

fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='sin(x)'), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='cos(x)'), row=1, col=2)

fig.update_xaxes(title_text='x', row=1, col=1)
fig.update_xaxes(title_text='x', row=1, col=2)
fig.update_yaxes(title_text='sin(x)', row=1, col=1)
fig.update_yaxes(title_text='cos(x)', row=1, col=2)

fig.update_layout(showlegend=True, width=1200, height=500)
fig.write_image('plotly_subplots.png', scale=2)
```

![Plotly Subplots](../assets/images/plotly_subplots.png)

## Using Colorways

```python
import sane_figs
import plotly.express as px
import numpy as np
import pandas as pd

sane_figs.setup(mode='article', colorway='nature')

x = np.linspace(0, 10, 100)
df = pd.DataFrame({
    'x': x,
    'Series 1': np.sin(x),
    'Series 2': np.cos(x),
    'Series 3': np.sin(x + np.pi/4)
})

df_long = df.melt('x', var_name='Series', value_name='y')

fig = px.line(df_long, x='x', y='y', color='Series', title='Nature Colorway')
fig.update_layout(showlegend=True)
fig.write_image('plotly_colorway.png', scale=2, width=800, height=500)
```

![Plotly Colorway](../assets/images/plotly_colorway.png)

## Using Watermarks

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article', watermark='© 2025 My Lab')

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = px.line(x=x, y=y, title='Figure with Watermark', labels={'x': 'x', 'y': 'sin(x)'})
fig.update_layout(showlegend=True)
fig.write_image('plotly_watermark.png', scale=2, width=800, height=500)
```

![Plotly Watermark](../assets/images/plotly_watermark.png)

## Per-Library Setup

You can also use the Plotly-specific setup function:

```python
import sane_figs
import plotly.express as px
import numpy as np

# Plotly-specific setup
sane_figs.setup_plotly(mode='article', colorway='nature')

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = px.line(x=x, y=y, title='Plotly-Specific Setup', labels={'x': 'x', 'y': 'sin(x)'})
fig.update_layout(showlegend=True)
fig.write_image('plotly_specific.png', scale=2, width=800, height=500)
```

## Tips for Plotly

1. **Use `scale=2`**: For high-resolution output, use `scale=2` when saving
2. **Set width and height**: Explicitly set figure dimensions for consistent sizing
3. **Use `write_image()`**: Save figures as PNG for publication
4. **Update layout**: Use `fig.update_layout()` for fine-tuning
5. **Combine with Plotly Graph Objects**: Use `go` for more complex figures

```python
import sane_figs
import plotly.express as px
import numpy as np

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = px.line(x=x, y=y, title='Best Practices', labels={'x': 'x', 'y': 'sin(x)'})
fig.update_layout(showlegend=True, width=800, height=500)
fig.write_image('plotly_best_practices.png', scale=2)
```

## Note on Interactive Features

Plotly figures are interactive by default. When saving to static images with `write_image()`, interactive features are preserved in the HTML output but not in PNG files. For publication, use PNG format with appropriate scaling.
