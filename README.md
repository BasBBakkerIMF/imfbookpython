# imfpythonbook

`imfpythonbook` is a small collection of helper functions for producing publication-quality charts following the International Monetary Fund (IMF) and World Economic Outlook (WEO) style guides. The package provides two sets of utilities:

- **Matplotlib helpers** for configuring fonts, colors, themes, and axis tick behavior compatible with IMF and WEO charts.
- **Plotnine (ggplot-style) helpers** that mirror the look and feel of the same charts using the `plotnine` library.

The modules contained in this package were originally developed for the IMF Python book and have been packaged here for reuse.

## Installation

Install directly from GitHub:

```sh
pip install git+https://github.com/BasBBakkerIMF/imfbookpython.git
```

## Usage

Import the package once and use the concise API:

```python
import imfpythonbook as ip
```

### Usage Examples

#### Matplotlib: IMF theme + simple line chart

```python
import numpy as np
import matplotlib.pyplot as plt
import imfpythonbook as ip

ip.matplotlib.set_imf_theme()

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ip.matplotlib.set_titles(ax, "IMF Theme Example", "Subtitle")
ax.plot(x, np.sin(x), color=ip.colors.blue)
plt.show()
```

#### Plotnine: IMF theme + simple line chart

```python
import numpy as np, pandas as pd
from plotnine import ggplot, aes, geom_line
import imfpythonbook as ip

x = np.linspace(0, 10, 100)
df = pd.DataFrame({"x": x, "y": np.sin(x)})

p = (
    ggplot(df, aes("x", "y"))
    + geom_line(color=ip.colors.blue)
    + ip.plotnine.set_imf_theme()
)
for layer in ip.plotnine.set_titles("IMF Theme Example", "Subtitle"):
    p += layer

print(p)
```

#### IMF Matplotlib Bar Chart

```python
import matplotlib.pyplot as plt
import imfpythonbook as ip

ip.matplotlib.set_imf_panel_theme()

fig, ax = plt.subplots()
ax.bar(
    ["A", "B", "C", "D"], [3, 1, 4, 2],
    color=[ip.colors.blue, ip.colors.green, ip.colors.red, ip.colors.grey]
)
ip.matplotlib.set_panel_titles(ax, "Panel Title", "Panel Subtitle")
plt.show()
```

#### Plotnine Bar Chart (IMF style)

```python
import pandas as pd
from plotnine import ggplot, aes, geom_bar, scale_fill_manual
import imfpythonbook as ip

df = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [3, 1, 4, 2]})

p = (
    ggplot(df, aes("category", "value", fill="category"))
    + geom_bar(stat="identity")
    + scale_fill_manual(values=[ip.colors.blue, ip.colors.green, ip.colors.red, ip.colors.grey])
    + ip.plotnine.set_imf_panel_theme()
)

for layer in ip.plotnine.set_panel_titles("Panel Title", "Panel Subtitle"):
    p += layer

print(p)
```

---

## WEO-Styled Examples

> These examples use the WEO modules directly (unchanged API).

#### WEO-Styled Unemployment Chart (Matplotlib)

```python
import numpy as np, matplotlib.pyplot as plt
from imfpythonbook.WEO_matplotlib import (
    set_weo_theme, add_y_ticks, add_x_end_ticks,
    add_weo_title, generate_breaks_auto, weo_colors, weo_text_size
)

set_weo_theme()
years = np.arange(2000, 2026)
countries = ["BRA", "CHL", "COL", "MEX", "PER"]
data = {c: np.random.randn(len(years)).cumsum() for c in countries}
breaks = generate_breaks_auto(np.concatenate(list(data.values())))

fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
for i, country in enumerate(countries):
    ax.plot(years, data[country], label=country, color=weo_colors[i])

ax.set_xticks(years[::5]); ax.set_xlim(years.min(), years.max())
ax.set_yticks(breaks['major']); ax.set_ylim(breaks['limits'])

add_y_ticks(ax, breaks['major'], breaks['minor'], years.min(), years.max())
add_x_end_ticks(ax, years.min(), years.max())
add_weo_title(ax, "Figure 1.2. Unemployment Rate Change", "(Percentage point change, annual data)")
plt.show()
```

#### WEO-Styled Real GDP Panel (Plotnine)

```python
import numpy as np, pandas as pd
from plotnine import ggplot, aes, geom_line, facet_wrap, scale_y_continuous, ggtitle, labs
from imfpythonbook.WEO_plotnine import (
    set_weo_panel_theme_plotnine, generate_breaks_auto,
    add_forecast_shading_plotnine, blue
)

years = list(range(2000, 2026))
countries = ["BRA", "CHL", "COL", "MEX"]
df = []

for country in countries:
    growth = np.random.normal(0.02, 0.01, len(years))
    index = 100 * np.cumprod(1 + growth)
    df.append(pd.DataFrame({"year": years, "value": index, "country": country}))

df = pd.concat(df)
breaks = generate_breaks_auto(df["value"])

p = (
    ggplot(df, aes("year", "value"))
    + geom_line(color=blue, size=0.7)
    + facet_wrap("~country")
    + scale_y_continuous(breaks=breaks["major"], limits=breaks["limits"])
    + set_weo_panel_theme_plotnine()
    + add_forecast_shading_plotnine(start_year=2022, end_year=2025, y_range=breaks["limits"])
    + ggtitle("Figure X. Real GDP Panel")
    + labs(subtitle="(Index, 2010=100)", caption="Source: Synthetic data. Real GDP index rebased to 2010=100.")
)

print(p)
```
