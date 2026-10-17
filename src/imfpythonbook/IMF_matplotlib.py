"""
This module provides utility functions and colour definitions inspired by the
original R utilities used by IMF staff.  The original R code defined a
palette of RGB colours, a couple of ggplot2 themes and helper functions for
adding caption-like annotations above plots.  The functions in this module
mirror the intent of the R code using Matplotlib.

Functions
---------
rgb2(red, green, blue)
    Convert 0–255 RGB values to Matplotlib hex colour.
set_imf_theme(myfont, myfontColor)
    Apply the original IMF theme to Matplotlib rcParams.
set_imf_panel_theme(myfont, myfontColor)
    Apply the original IMF panel theme.
set_imf_2027_theme(myfont, myfontColor)
    Apply the IMF 2027 theme.
set_imf_panel_2027_theme(myfont, myfontColor)
    Apply the IMF 2027 panel theme.
apply_imf_titles(ax, title, subtitle=None)
    Helper to set both title (18pt bold) and subtitle (16pt normal).
apply_imf_panel_titles(ax, title, subtitle=None)
    Helper to set panel-title (14pt bold) and panel-subtitle (12pt normal).
add_text_to_figure(fig, text, y_offset)
    Add an italic caption above a figure.
add_text_to_figure_new(fig, text, y_offset)
    Alternate version: centers the caption and stacks via GridSpec.
"""
import os
os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
import numpy as np

# Colour definitions (0–255 -> hex)
def rgb2(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

blue        = rgb2(75,130,173)
blue_2027   = rgb2(0,76,151)
imf_blue_2027 = blue_2027
green       = rgb2(150,186,121)
red         = rgb2(192,0,80)
grey        = rgb2(166,168,172)
light_green = rgb2(150,215,130)
light_grey  = rgb2(211,211,211)
light_red   = rgb2(238,36,0)
dark_red    = rgb2(144,0,0)
light_blue  = rgb2(202,224,251)
dark_blue   = rgb2(14,16,116)
purple      = rgb2(146,60,194)
orange      = rgb2(255,133,71)

# Palette vectors
A4_colors     = [blue, green, grey, light_green, light_grey, light_red, dark_red]
A4_colors_bar = [blue, green, red, grey, "black", light_green, light_grey, light_red, dark_red]

def _set_imf_theme(myfont, myfontColor, panel, theme_2027):
    axis_size = 10 if panel else 14
    title_size = 14 if panel else 18
    rcParams.update({
        "font.family": myfont,
        "font.size": 14,
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.edgecolor": light_grey,
        "axes.linewidth": 1,
        "axes.titlesize": title_size,
        "axes.titleweight": "bold",
        "axes.titlecolor": myfontColor,
        "axes.labelsize": axis_size,
        "axes.labelcolor": "black",
        "xtick.labelsize": axis_size,
        "ytick.labelsize": axis_size,
        "xtick.color": "black",
        "xtick.major.size": 0,
        "xtick.minor.size": 0,
        "ytick.color": light_grey,
        "ytick.labelcolor": "black",
        "ytick.direction": "in",
        "ytick.major.size": 5.67,
        "ytick.major.pad": 3.5 * 72 / 25.4,
        "ytick.minor.pad": 3.5 * 72 / 25.4,
        "axes.grid": False,
        "figure.facecolor": "white",
        "figure.autolayout": True,
        "legend.fontsize": 14,
        "legend.frameon": False,
    })


def _set_imf_panel_title_theme(myfont, myfontColor, theme_2027):
    """Apply the centered overall panel-title styling used in the R helpers."""
    rcParams.update({
        "font.family": myfont,
        "axes.titlecolor": myfontColor,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
    })


def set_imf_theme(myfont="Segoe UI", myfontColor=blue):
    """Apply the original IMF theme, matching ``theme_imf`` in R."""
    _set_imf_theme(myfont, myfontColor, panel=False, theme_2027=False)


def set_imf_panel_theme(myfont="Segoe UI", myfontColor=blue):
    """Apply the original IMF panel theme, matching ``theme_imf_panel`` in R."""
    _set_imf_theme(myfont, myfontColor, panel=True, theme_2027=False)


def set_imf_2027_theme(myfont="Arial", myfontColor="black"):
    """Apply the IMF 2027 theme, matching ``theme_imf_2027`` in R."""
    _set_imf_theme(myfont, myfontColor, panel=False, theme_2027=True)


def set_imf_panel_2027_theme(myfont="Arial", myfontColor="black"):
    """Apply the IMF 2027 panel theme, matching ``theme_imf_panel_2027`` in R."""
    _set_imf_theme(myfont, myfontColor, panel=True, theme_2027=True)


def set_imf_panel_title_theme(myfont="Segoe UI", myfontColor=blue):
    """Apply the centered panel-title styling used in ``theme_imf_panel_title`` in R."""
    _set_imf_panel_title_theme(myfont, myfontColor, theme_2027=False)


def set_imf_panel_title_2027_theme(myfont="Arial", myfontColor=blue_2027):
    """Apply the centered panel-title styling used in ``theme_imf_panel_title_2027`` in R."""
    _set_imf_panel_title_theme(myfont, myfontColor, theme_2027=True)

# Helper: apply title and subtitle above plot for standard theme
def apply_imf_titles(ax, title, subtitle=None):
    """Set a left-aligned title and subtitle using the active IMF theme settings."""
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_edgecolor(light_grey)
        ax.spines[loc].set_linewidth(rcParams['axes.linewidth'])
    ax.tick_params(axis="x", length=0, labelcolor="black")
    ax.tick_params(axis="y", direction="in", length=5.67, color=light_grey, labelcolor="black")
    ax.set_title(
        title,
        loc='left',
        fontsize=rcParams["axes.titlesize"],
        fontweight=rcParams["axes.titleweight"],
        color=rcParams["axes.titlecolor"],
        pad=32
    )
    if subtitle:
        ax.text(
            0, 1.02, subtitle,
            transform=ax.transAxes,
            ha='left', va='bottom',
            fontsize=16,
            fontweight='normal',
            color=rcParams["axes.titlecolor"]
        )

# Helper: apply title and subtitle above plot for panel theme
def apply_imf_panel_titles(ax, title, subtitle=None):
    """Set a panel title and subtitle using the active IMF theme settings."""
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_edgecolor(light_grey)
        ax.spines[loc].set_linewidth(rcParams['axes.linewidth'])
    ax.tick_params(axis="x", length=0, labelcolor="black")
    ax.tick_params(axis="y", direction="in", length=5.67, color=light_grey, labelcolor="black")
    ax.set_title(
        title,
        loc='left',
        fontsize=rcParams["axes.titlesize"],
        fontweight=rcParams["axes.titleweight"],
        color=rcParams["axes.titlecolor"],
        pad=28
    )
    if subtitle:
        ax.text(
            0, 1.02, subtitle,
            transform=ax.transAxes,
            ha='left', va='bottom',
            fontsize=12,
            fontweight='normal',
            color=rcParams["axes.titlecolor"]
        )

# Add caption above figure
def add_text_to_figure(fig, text, y_offset=0.38, primary_font="Segoe UI"):
    """Place an italic caption above the figure using GridSpec."""
    fig.canvas.draw()
    gs = GridSpec(2, 1, height_ratios=[1, 5], figure=fig)
    for ax in fig.axes:
        ax.set_position(gs[1].get_position(fig))
    txt_ax = fig.add_subplot(gs[0])
    txt_ax.axis("off")
    txt_ax.text(
        0.5, y_offset, text,
        ha="center", va="center",
        fontsize=12, fontfamily=primary_font,
        fontstyle="italic", color="black"
    )
    return fig

# Alternate caption version
def add_text_to_figure_new(fig, text, y_offset=0.38, primary_font="Segoe UI"):
    return add_text_to_figure(fig, text, y_offset=y_offset, primary_font=primary_font)

# Simple self-tests run when the module is executed directly.
def _test_panel_title_theme_helpers():
    assert blue == "#4b82ad"
    assert blue_2027 == "#004c97"

    set_imf_panel_title_theme()
    assert "Segoe UI" in rcParams["font.family"]
    assert rcParams["axes.titlecolor"] == blue

    set_imf_panel_title_2027_theme()
    assert "Arial" in rcParams["font.family"]
    assert rcParams["axes.titlecolor"] == blue_2027

    set_imf_2027_theme()
    assert rcParams["axes.labelcolor"] == "black"


# Demonstrations
if __name__ == "__main__":
    _test_panel_title_theme_helpers()

    x = np.linspace(0, 10, 100)

    # 1. IMF theme line plot with title & subtitle above
    set_imf_theme()
    fig, ax = plt.subplots()
    apply_imf_titles(ax, "IMF Theme", "Subtitle")
    ax.plot(x, np.sin(x), color=blue)
    plt.show()

    # 2. IMF panel theme bar chart with panel title
    set_imf_panel_theme()
    fig, ax = plt.subplots()
    ax.bar(["A","B","C","D"],[3,1,4,2], color=[blue, green, red, grey])
    apply_imf_panel_titles(ax, "IMF Panel Theme Title", "Panel Subtitle")
    plt.show()

    # 3. Text annotation demo
    set_imf_theme()
    fig, ax = plt.subplots()
    ax.plot(x, np.cos(x), color=red)
    add_text_to_figure(fig, "Caption", y_offset=0.9)
    plt.show()

    # 4. Alternate annotation demo
    set_imf_theme()
    fig, ax = plt.subplots()
    ax.plot(x, np.tan(x), color=green)
    add_text_to_figure_new(fig, "Centered caption demo", y_offset=0.8)
    plt.show()
