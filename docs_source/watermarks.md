# Watermarks

Sane-Figs supports adding watermarks to your figures for branding, copyright protection, or draft identification.

## Text Watermarks

Add a text watermark to your figures:

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Add a text watermark
sane_figs.setup(
    mode='article',
    watermark='© 2025 My Lab'
)

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Figure with Text Watermark')
plt.savefig('text_watermark.png')
```

![Text Watermark](images/watermark_text.png)

## Image Watermarks

Add an image watermark (logo, signature, etc.):

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Add an image watermark
sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_image_watermark('logo.png', opacity=0.2)
)

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Figure with Image Watermark')
plt.savefig('image_watermark.png')
```

![Image Watermark](images/watermark_image.png)

## Watermark Positions

Watermarks can be positioned in any corner of the figure:

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']

for pos in positions:
    sane_figs.setup(
        mode='article',
        watermark=sane_figs.create_text_watermark(
            'DRAFT',
            position=pos,
            opacity=0.3
        )
    )

    plt.figure()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title(f'Watermark: {pos}')
    plt.savefig(f'watermark_{pos}.png')
    plt.close()
```

![Watermark Top Left](images/watermark_top-left.png)
![Watermark Top Right](images/watermark_top-right.png)
![Watermark Bottom Left](images/watermark_bottom-left.png)
![Watermark Bottom Right](images/watermark_bottom-right.png)

## Customizing Text Watermarks

### Create Text Watermark with Custom Options

```python
import sane_figs

watermark = sane_figs.create_text_watermark(
    text='CONFIDENTIAL',
    position='bottom-right',
    opacity=0.2,
    scale=0.15,
    margin=[0.02, 0.02],
    font_size=14.0,
    font_family='sans-serif',
    font_weight='bold',
    font_color='#FF0000'
)

sane_figs.setup(mode='article', watermark=watermark)
```

### Text Watermark Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `text` | `str` | Required | Watermark text |
| `position` | `str` | `'bottom-right'` | Position: `'top-left'`, `'top-right'`, `'bottom-left'`, `'bottom-right'` |
| `opacity` | `float` | `0.3` | Opacity (0.0 to 1.0) |
| `scale` | `float` | `0.1` | Scale relative to figure size |
| `margin` | `[x, y]` | `[0.02, 0.02]` | Margin from edges (0.0 to 1.0) |
| `font_size` | `float` | `12.0` | Font size in points |
| `font_family` | `str` | `'sans-serif'` | Font family |
| `font_weight` | `str` | `'normal'` | Font weight: `'normal'`, `'bold'`, etc. |
| `font_color` | `str` | `'#000000'` | Font color (hex or name) |

## Customizing Image Watermarks

### Create Image Watermark with Custom Options

```python
import sane_figs

watermark = sane_figs.create_image_watermark(
    image_path='logo.png',
    position='top-right',
    opacity=0.15,
    scale=0.1,
    margin=[0.01, 0.01]
)

sane_figs.setup(mode='article', watermark=watermark)
```

### Image Watermark Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `image_path` | `str` | Required | Path to image file |
| `position` | `str` | `'bottom-right'` | Position: `'top-left'`, `'top-right'`, `'bottom-left'`, `'bottom-right'` |
| `opacity` | `float` | `0.3` | Opacity (0.0 to 1.0) |
| `scale` | `float` | `0.1` | Scale relative to figure size |
| `margin` | `[x, y]` | `[0.02, 0.02]` | Margin from edges (0.0 to 1.0) |

## Common Use Cases

### Draft Figures

```python
import sane_figs

sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_text_watermark(
        'DRAFT - DO NOT CITE',
        position='center',
        opacity=0.4,
        font_weight='bold',
        font_color='#FF0000'
    )
)
```

### Copyright Protection

```python
import sane_figs

sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_text_watermark(
        '© 2025 My Lab. All rights reserved.',
        position='bottom-right',
        opacity=0.2
    )
)
```

### Branding with Logo

```python
import sane_figs

sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_image_watermark(
        'logo.png',
        position='top-right',
        opacity=0.2,
        scale=0.08
    )
)
```

### Confidential Documents

```python
import sane_figs

sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_text_watermark(
        'CONFIDENTIAL',
        position='center',
        opacity=0.3,
        font_weight='bold',
        font_color='#FF0000'
    )
)
```

## Watermarks in Presets

You can include watermark settings in your custom presets:

```yaml
name: "branded-figures"
mode: "custom"

figure:
  size: [6.4, 4.8]
  dpi: 300

typography:
  font_family: "sans-serif"
  font_sizes:
    title: 14.0
    label: 12.0
    legend: 10.0
    tick: 10.0

watermark:
  type: "text"
  text: "© 2025 My Lab"
  position: "bottom-right"
  opacity: 0.2
  font_size: 10.0
  font_color: "#000000"
```

## Tips for Effective Watermarks

1. **Keep it subtle**: Use low opacity (0.1-0.3) so it doesn't distract from the data
2. **Position carefully**: Avoid covering important data or labels
3. **Use appropriate text**: Keep it short and meaningful
4. **Consider accessibility**: Ensure the watermark doesn't make the figure hard to read
5. **Test on different backgrounds**: Make sure the watermark is visible on both light and dark backgrounds

```python
import sane_figs
import matplotlib.pyplot as plt
import numpy as np

# Good: Subtle watermark in corner
sane_figs.setup(
    mode='article',
    watermark=sane_figs.create_text_watermark(
        '© 2025 My Lab',
        position='bottom-right',
        opacity=0.15
    )
)

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Effective Watermark')
plt.savefig('effective_watermark.png')
```

![Effective Watermark](images/watermark_effective.png)
