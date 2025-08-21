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
    Apply the IMF “classic” theme to Matplotlib rcParams with a full rectangle border in light_grey.
set_imf_panel_theme(myfont, myfontColor)
    Apply the IMF panel theme (smaller text) to Matplotlib rcParams with a full rectangle border in light_grey.
apply_imf_titles(ax, title, subtitle=None)
    Helper to set both title (18pt bold) and subtitle (16pt normal) left-aligned in blue above the plot area.
apply_imf_panel_titles(ax, title, subtitle=None)
    Helper to set panel-title (14pt bold) and panel-subtitle (12pt normal) left-aligned in blue above the plot area.
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

# Core theme: classic with IMF tweaks
def set_imf_theme(myfont="Segoe UI", myfontColor=blue):
    """Apply classic IMF theme with full rectangle border in light_grey."""
    rcParams.update({
        # Font
        "font.family": myfont,
        "font.size": 14,
        # Full border (all four spines)
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        # Border styling
        "axes.edgecolor": light_grey,
        "axes.linewidth": 1,
        # Title styling defaults (main title)
        "axes.titlesize": 18,
        "axes.titleweight": "bold",
        "axes.titlecolor": myfontColor,
        # Axis labels and ticks
        "axes.labelsize": 14,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.grid": False,
        # Figure
        "figure.facecolor": "white",
        "figure.autolayout": True,
        # Legend
        "legend.fontsize": 12,
        "legend.frameon": False,
    })

# Panel theme: similar but smaller text
def set_imf_panel_theme(myfont="Segoe UI", myfontColor=blue):
    """Apply IMF panel theme with full rectangle border in light_grey and smaller text."""
    rcParams.update({
        "font.family": myfont,
        "font.size": 10,
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.edgecolor": light_grey,
        "axes.linewidth": 1,
        "axes.labelsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.grid": False,
        "figure.facecolor": "white",
        "figure.autolayout": True,
        "legend.fontsize": 10,
        "legend.frameon": False,
    })

# Helper: apply title and subtitle above plot for standard theme
def apply_imf_titles(ax, title, subtitle=None):
    """Set main title (18pt bold) and subtitle (16pt normal) left-aligned above the plot."""
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_edgecolor(light_grey)
        ax.spines[loc].set_linewidth(rcParams['axes.linewidth'])
    ax.set_title(
        title,
        loc='left',
        fontsize=18,
        fontweight='bold',
        color=blue,
        pad=32
    )
    if subtitle:
        ax.text(
            0, 1.02, subtitle,
            transform=ax.transAxes,
            ha='left', va='bottom',
            fontsize=16,
            fontweight='normal',
            color=blue
        )

# Helper: apply title and subtitle above plot for panel theme
def apply_imf_panel_titles(ax, title, subtitle=None):
    """Set panel title (14pt bold) and subtitle (12pt normal) left-aligned above the plot."""
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_edgecolor(light_grey)
        ax.spines[loc].set_linewidth(rcParams['axes.linewidth'])
    ax.set_title(
        title,
        loc='left',
        fontsize=14,
        fontweight='bold',
        color=blue,
        pad=28
    )
    if subtitle:
        ax.text(
            0, 1.02, subtitle,
            transform=ax.transAxes,
            ha='left', va='bottom',
            fontsize=12,
            fontweight='normal',
            color=blue
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

# Demonstrations
if __name__ == "__main__":
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
