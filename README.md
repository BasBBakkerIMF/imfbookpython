# imfpythonbook

`imfpythonbook` is a small collection of helper functions for producing publication‑quality charts following the International Monetary Fund (IMF) and World Economic Outlook (WEO) style guides.  The package provides two sets of utilities:

- **Matplotlib helpers** for configuring fonts, colours, themes and axis tick behaviour compatible with IMF and WEO charts.
- **Plotnine (ggplot‑style) helpers** that mirror the look and feel of the same charts using the `plotnine` library.

The modules contained in this package were originally developed for the IMF Python book and have been packaged here for reuse.

## Installation

You can install the package from a source checkout by running:

```sh
pip install -e .
```

from the root of this repository.  This will install the package in editable mode so that any changes you make to the source are immediately reflected in your Python environment.

## Usage

Import the package and access the individual modules:

```python
import imfpythonbook

# Matplotlib: apply IMF theme and draw a simple line chart
import numpy as np
import matplotlib.pyplot as plt

imfpythonbook.IMF_matplotlib.set_imf_theme()
x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
imfpythonbook.IMF_matplotlib.apply_imf_titles(ax, "IMF Theme Example", "Subtitle")
ax.plot(x, np.sin(x), color=imfpythonbook.IMF_matplotlib.blue)
plt.show()

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

See the docstrings in each module for additional examples and usage details.

