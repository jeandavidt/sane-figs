# Altair

Sane-Figs provides full support for Altair, automatically applying publication-ready styling to your declarative visualizations.

## Installation

```bash
pip install sane-figs[altair]
```

## Basic Usage

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

# Apply publication defaults
sane_figs.setup(mode='article')

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

# Create a simple plot
chart = alt.Chart(df).mark_line().encode(
    x='x',
    y='y'
).properties(
    title='Sine Wave'
)

chart.save('figure.png')
```

![Basic Altair Example](../assets/images/altair_basic.png)

## Line Plots

### Simple Line Plot

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='sin(x)')
).properties(
    title='Simple Line Plot',
    width=600,
    height=400
)

chart.save('altair_line.png')
```

![Altair Line Plot](../assets/images/altair_line.png)

### Multiple Lines

```python
import sane_figs
import altair as alt
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

chart = alt.Chart(df_long).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='y'),
    color=alt.Color('Function', legend=alt.Legend(title='Function'))
).properties(
    title='Multiple Lines',
    width=600,
    height=400
)

chart.save('altair_multiple_lines.png')
```

![Altair Multiple Lines](../assets/images/altair_multiple_lines.png)

## Scatter Plots

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)

df = pd.DataFrame({'x': x, 'y': y, 'color': colors})

chart = alt.Chart(df).mark_circle(size=50, opacity=0.7).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='y'),
    color=alt.Color('color', legend=alt.Legend(title='Value'), scale=alt.Scale(scheme='viridis'))
).properties(
    title='Scatter Plot',
    width=600,
    height=400
)

chart.save('altair_scatter.png')
```

![Altair Scatter Plot](../assets/images/altair_scatter.png)

## Bar Charts

```python
import sane_figs
import altair as alt
import pandas as pd

sane_figs.setup(mode='article')

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

df = pd.DataFrame({'Category': categories, 'Value': values})

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Category', title='Category'),
    y=alt.Y('Value', title='Value')
).properties(
    title='Bar Chart',
    width=600,
    height=400
)

chart.save('altair_bar.png')
```

![Altair Bar Chart](../assets/images/altair_bar.png)

## Histograms

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

np.random.seed(42)
data = np.random.randn(1000)

df = pd.DataFrame({'Value': data})

chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
    x=alt.X('Value', bin=alt.Bin(maxbins=30), title='Value'),
    y=alt.Y('count()', title='Frequency')
).properties(
    title='Histogram',
    width=600,
    height=400
)

chart.save('altair_histogram.png')
```

![Altair Histogram](../assets/images/altair_histogram.png)

## Box Plots

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]
df = pd.DataFrame({
    'Group': ['A'] * 100 + ['B'] * 100 + ['C'] * 100,
    'Value': np.concatenate(data)
})

chart = alt.Chart(df).mark_boxplot().encode(
    x=alt.X('Group', title='Group'),
    y=alt.Y('Value', title='Value')
).properties(
    title='Box Plot',
    width=600,
    height=400
)

chart.save('altair_box.png')
```

![Altair Box Plot](../assets/images/altair_box.png)

## Area Charts

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
df = pd.DataFrame({
    'x': x,
    'sin(x)': np.sin(x),
    'cos(x)': np.cos(x)
})

df_long = df.melt('x', var_name='Function', value_name='y')

chart = alt.Chart(df_long).mark_area(opacity=0.5).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='y'),
    color=alt.Color('Function', legend=alt.Legend(title='Function'))
).properties(
    title='Area Chart',
    width=600,
    height=400
)

chart.save('altair_area.png')
```

![Altair Area Chart](../assets/images/altair_area.png)

## Subplots (Faceting)

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
df = pd.DataFrame({
    'x': x,
    'sin(x)': np.sin(x),
    'cos(x)': np.cos(x)
})

df_long = df.melt('x', var_name='Function', value_name='y')

chart = alt.Chart(df_long).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='y'),
    color=alt.Color('Function', legend=alt.Legend(title='Function'))
).properties(
    width=300,
    height=300
).facet(
    column=alt.Column('Function', title=None)
).properties(
    title='Subplots'
)

chart.save('altair_subplots.png')
```

![Altair Subplots](../assets/images/altair_subplots.png)

## Using Colorways

```python
import sane_figs
import altair as alt
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

chart = alt.Chart(df_long).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='y'),
    color=alt.Color('Series', legend=alt.Legend(title='Series'))
).properties(
    title='Nature Colorway',
    width=600,
    height=400
)

chart.save('altair_colorway.png')
```

![Altair Colorway](../assets/images/altair_colorway.png)

## Using Watermarks

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article', watermark='© 2025 My Lab')

x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='sin(x)')
).properties(
    title='Figure with Watermark',
    width=600,
    height=400
)

chart.save('altair_watermark.png')
```

![Altair Watermark](../assets/images/altair_watermark.png)

## Per-Library Setup

You can also use the Altair-specific setup function:

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

# Altair-specific setup
sane_figs.setup_altair(mode='article', colorway='nature')

x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='sin(x)')
).properties(
    title='Altair-Specific Setup',
    width=600,
    height=400
)

chart.save('altair_specific.png')
```

## Tips for Altair

1. **Set width and height**: Explicitly set figure dimensions for consistent sizing
2. **Use `save()`**: Save figures as PNG for publication
3. **Use faceting**: For subplots, use `.facet()` instead of multiple charts
4. **Encode titles**: Use `alt.X()` and `alt.Y()` with `title` parameter for axis labels
5. **Use properties**: Set chart properties for title and dimensions

```python
import sane_figs
import altair as alt
import numpy as np
import pandas as pd

sane_figs.setup(mode='article')

x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x=alt.X('x', title='x'),
    y=alt.Y('y', title='sin(x)')
).properties(
    title='Best Practices',
    width=600,
    height=400
)

chart.save('altair_best_practices.png')
```

## Note on Interactive Features

Altair charts are interactive by default. When saving to static images with `save()`, interactive features are preserved in the HTML output but not in PNG files. For publication, use PNG format.
