"""
imfpythonbook

A small library of helper functions for producing charts styled in accordance
with the International Monetary Fund (IMF) and World Economic Outlook (WEO)
style guides.

The package exposes four modules:

* :mod:`imfpythonbook.IMF_matplotlib` – utilities for Matplotlib charts
* :mod:`imfpythonbook.IMF_plotnine`  – utilities for Plotnine charts
* :mod:`imfpythonbook.WEO_matplotlib` – helpers for WEO‑style Matplotlib charts
* :mod:`imfpythonbook.WEO_plotnine`  – helpers for WEO‑style Plotnine charts

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