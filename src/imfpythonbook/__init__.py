"""
imfpythonbook

A small library of helper functions for producing charts styled in accordance
with the International Monetary Fund (IMF) and World Economic Outlook (WEO)
style guides.

The package exposes four modules:

* :mod:`imfpythonbook.IMF_matplotlib`  – utilities for Matplotlib charts
* :mod:`imfpythonbook.IMF_plotnine`    – utilities for Plotnine charts
* :mod:`imfpythonbook.WEO_matplotlib`  – helpers for WEO-style Matplotlib charts
* :mod:`imfpythonbook.WEO_plotnine`    – helpers for WEO-style Plotnine charts

Import the modules directly from the package and consult their docstrings for
details and examples.
"""

# Expose the individual modules at the top level for convenience
from . import IMF_matplotlib
from . import IMF_plotnine
from . import WEO_matplotlib
from . import WEO_plotnine

__all__ = [
    "IMF_matplotlib",
    "IMF_plotnine",
    "WEO_matplotlib",
    "WEO_plotnine",
]

# ---- Ergonomic aliases (short, stable API) ----
from types import SimpleNamespace

# 1) Unified colors (reuse the IMF_matplotlib palette everywhere)
colors = SimpleNamespace(
    blue=IMF_matplotlib.blue,
    green=IMF_matplotlib.green,
    red=IMF_matplotlib.red,
    grey=IMF_matplotlib.grey,
    light_green=IMF_matplotlib.light_green,
    light_grey=IMF_matplotlib.light_grey,
    light_red=IMF_matplotlib.light_red,
    dark_red=IMF_matplotlib.dark_red,
    light_blue=IMF_matplotlib.light_blue,
    dark_blue=IMF_matplotlib.dark_blue,
    purple=IMF_matplotlib.purple,
    orange=IMF_matplotlib.orange,
)

# 2) Short Matplotlib facade
matplotlib = SimpleNamespace(
    set_imf_theme=IMF_matplotlib.set_imf_theme,
    set_imf_panel_theme=IMF_matplotlib.set_imf_panel_theme,
    set_titles=IMF_matplotlib.apply_imf_titles,
    set_panel_titles=IMF_matplotlib.apply_imf_panel_titles,
)

# 3) Short Plotnine facade
plotnine = SimpleNamespace(
    set_imf_theme=IMF_plotnine.set_imf_theme_plotnine,
    set_imf_panel_theme=IMF_plotnine.set_imf_panel_theme_plotnine,
    set_titles=IMF_plotnine.apply_imf_titles_plotnine,
    set_panel_titles=IMF_plotnine.apply_imf_panel_titles_plotnine,
)

# Export new aliases (keep legacy API intact)
__all__ += ["colors", "matplotlib", "plotnine"]
