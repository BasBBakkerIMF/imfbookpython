# imfpythonbook

`imfpythonbook` is a small collection of helper functions for producing publication‑quality charts following the International Monetary Fund (IMF) and World Economic Outlook (WEO) style guides.  The package provides two sets of utilities:

- **Matplotlib helpers** for configuring fonts, colours, themes and axis tick behaviour compatible with IMF and WEO charts.
- **Plotnine (ggplot‑style) helpers** that mirror the look and feel of the same charts using the `plotnine` library.

The modules contained in this package were originally developed for the IMF Python book and have been packaged here for reuse.

## Installation

You can install the package direclty from GitHub using the following:

```sh
pip install git+https://github.com/BasBBakkerIMF/imfbookpython.git
```

## Usage

Import the package and access the individual modules:

```python
import imfpythonbook
```

### Usage Examples

Here is how you would use the matplotlib IMF style functionalities. 

```python
# Matplotlib: apply IMF theme and draw a simple line chart
import numpy as np
import matplotlib.pyplot as plt

imfpythonbook.IMF_matplotlib.set_imf_theme()
x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
imfpythonbook.IMF_matplotlib.apply_imf_titles(ax, "IMF Theme Example", "Subtitle")
ax.plot(x, np.sin(x), color=imfpythonbook.IMF_matplotlib.blue)
plt.show()
```
Here is how you would use the plotnine IMF style functionalities. 

```python
# Plotnine: build the same chart using ggplot syntax
import pandas as pd
from plotnine import ggplot, aes, geom_line

df = pd.DataFrame({"x": x, "y": np.sin(x)})
p = (
    ggplot(df, aes("x", "y"))
    + geom_line(color=imfpythonbook.IMF_plotnine.blue)
    + imfpythonbook.IMF_plotnine.set_imf_theme_plotnine()
)
for layer in imfpythonbook.IMF_plotnine.apply_imf_titles_plotnine("IMF Theme Example", "Subtitle"):
    p += layer
print(p)
```

Now let's look at some specific IMF style charts. Let's start wit the IMF Matplotlib Line Chart.

```python
import numpy as np
import matplotlib.pyplot as plt
import imfpythonbook

# Apply IMF theme
imfpythonbook.IMF_matplotlib.set_imf_theme()

# Line chart
x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color=imfpythonbook.IMF_matplotlib.blue)
imfpythonbook.IMF_matplotlib.apply_imf_titles(ax, "IMF Theme Example", "Subtitle")
plt.show()
```
The IMF Matplotlib Bar Chart

```python
import matplotlib.pyplot as plt
import imfpythonbook

# Apply IMF panel theme
imfpythonbook.IMF_matplotlib.set_imf_panel_theme()

# Bar chart
fig, ax = plt.subplots()
ax.bar(
    ["A", "B", "C", "D"], [3, 1, 4, 2],
    color=[
        imfpythonbook.IMF_matplotlib.blue,
        imfpythonbook.IMF_matplotlib.green,
        imfpythonbook.IMF_matplotlib.red,
        imfpythonbook.IMF_matplotlib.grey
    ]
)
imfpythonbook.IMF_matplotlib.apply_imf_panel_titles(ax, "Panel Title", "Panel Subtitle")
plt.show()
```
Plotnine Bar Chart

```python
import pandas as pd
from plotnine import ggplot, aes, geom_bar, scale_fill_manual
import imfpythonbook

df = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [3, 1, 4, 2]})

p = (
    ggplot(df, aes("category", "value", fill="category"))
    + geom_bar(stat="identity")
    + scale_fill_manual(values=[
        imfpythonbook.IMF_plotnine.blue,
        imfpythonbook.IMF_plotnine.green,
        imfpythonbook.IMF_plotnine.red,
        imfpythonbook.IMF_plotnine.grey
    ])
    + imfpythonbook.IMF_plotnine.set_imf_panel_theme_plotnine()
)

for layer in imfpythonbook.IMF_plotnine.apply_imf_panel_titles_plotnine("Panel Title", "Panel Subtitle"):
    p += layer

print(p)
```

WEO-Styled Unemployment Chart using Matplotlib

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
WEO-Styled GDP Panel using Plotnine
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