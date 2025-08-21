# imf_plotnine_utils.py
"""
Utilities for IMF-styled Plotnine charts, mirroring original R/ggplot2 utilities.
Provides:
- RGB-to-hex palette definitions
- `set_imf_theme_plotnine` and `set_imf_panel_theme_plotnine` for classic and panel themes
- Title/subtitle helpers
- Caption annotation helpers
- Simple built-in tests for core functions
"""

from plotnine import (
    ggplot, aes, geom_line, geom_bar, scale_fill_manual,
    theme_classic, theme, element_text, element_rect, element_line,
    element_blank, labs, annotate
)
import numpy as np
import pandas as pd

# Colour definitions (0–255 -> hex)
def rgb2(r, g, b):
    """Convert integer RGB values (0–255) to hex string."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

blue        = rgb2(75, 130, 173)
green       = rgb2(150, 186, 121)
red         = rgb2(192,   0,  80)
grey        = rgb2(166, 168, 172)
light_green = rgb2(150, 215, 130)
light_grey  = rgb2(211, 211, 211)
light_red   = rgb2(238,  36,   0)
dark_red    = rgb2(144,   0,   0)
light_blue  = rgb2(202, 224, 251)
dark_blue   = rgb2( 14,  16, 116)
purple      = rgb2(146,  60, 194)
orange      = rgb2(255, 133,  71)

# Palette vectors
A4_colors     = [blue, green, grey, light_green, light_grey, light_red, dark_red]
A4_colors_bar = [
    blue, green, red, grey,
    "black", light_green, light_grey, light_red, dark_red
]

# Core theme: classic with IMF tweaks
def set_imf_theme_plotnine(font="Segoe UI", font_color=blue):
    """
    Return a Plotnine theme matching IMF classic style (full border),
    including axis ticks, grid, and border settings per IMF guidelines.
    """
    return (
        theme_classic()
        + theme(
            text=element_text(family=font, size=14, color="black"),
            axis_title_x=element_text(size=14, family=font),
            axis_title_y=element_text(size=14, family=font),
            axis_text_x=element_text(size=14, color="black"),
            axis_text_y=element_text(size=14, color="black"),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_line(color=light_grey),
            axis_line=element_line(color=light_grey),
            panel_border=element_rect(color=light_grey, fill=None, size=1),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            plot_title=element_text(
                size=18, family=font, weight="bold", color=font_color, ha="left"
            ),
            plot_subtitle=element_text(
                size=16, family=font, style="normal", color=font_color, ha="left"
            ),
            plot_caption=element_text(size=12, family=font),
            legend_text=element_text(size=12),
            legend_position="right"
        )
    )

# Panel theme: similar style, smaller text
def set_imf_panel_theme_plotnine(font="Segoe UI", font_color=blue):
    """
    Return a Plotnine theme matching IMF panel style (full border, smaller text).
    """
    return (
        theme_classic()
        + theme(
            text=element_text(family=font, size=10, color="black"),
            axis_title_x=element_text(size=10, family=font),
            axis_title_y=element_text(size=10, family=font),
            axis_text_x=element_text(size=10, color="black"),
            axis_text_y=element_text(size=10, color="black"),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_line(color=light_grey),
            axis_line=element_line(color=light_grey),
            panel_border=element_rect(color=light_grey, fill=None, size=1),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            plot_title=element_text(
                size=14, family=font, weight="bold", color=font_color, ha="left"
            ),
            plot_subtitle=element_text(
                size=12, family=font, style="normal", color=font_color, ha="left"
            ),
            plot_caption=element_text(size=10, family=font),
            legend_text=element_text(size=10),
            legend_position="right"
        )
    )

# Title/subtitle helpers
def apply_imf_titles_plotnine(title, subtitle=None):
    """Return labs layers for main title and optional subtitle."""
    layers = [labs(title=title)]
    if subtitle:
        layers.append(labs(subtitle=subtitle))
    return layers

def apply_imf_panel_titles_plotnine(title, subtitle=None):
    """Same as apply_imf_titles_plotnine (panel uses same logic)."""
    return apply_imf_titles_plotnine(title, subtitle)

# Caption annotation
def add_text_to_figure_plotnine(plot, text, y_offset=1.02):
    """
    Annotate the plot with italic caption text above the plotting area.
    Parameters:
      plot: a plotnine ggplot object
      text: string caption
      y_offset: vertical position relative to axes (e.g., >1 places above)
    """
    # Removed inherit_aes to avoid duplication error
    return plot + annotate(
        "text", x=0.5, y=y_offset, label=text,
        ha="center", va="bottom", size=12, fontstyle="italic"
    )

# Alias for alternative caption version
add_text_to_figure_new_plotnine = add_text_to_figure_plotnine

# Simple unit tests
def _test_rgb2():
    assert rgb2(0, 0, 0)       == "#000000"
    assert rgb2(255, 255, 255) == "#ffffff"
    assert blue == rgb2(75, 130, 173)

def _test_palettes():
    assert isinstance(A4_colors, list) and len(A4_colors) >= 3
    assert A4_colors[0] == blue
    assert "black" in A4_colors_bar

# Demonstrations
if __name__ == "__main__":
    # Run tests
    _test_rgb2()
    _test_palettes()

    # Demo data
    x  = np.linspace(0, 10, 100)
    df = pd.DataFrame({'x': x, 'sinx': np.sin(x), 'cosx': np.cos(x), 'tanx': np.tan(x)})

    # 1. IMF theme line plot with title & subtitle above
    p1 = (
        ggplot(df, aes('x', 'sinx'))
        + geom_line(color=blue)
        + set_imf_theme_plotnine()
    )
    for layer in apply_imf_titles_plotnine("IMF Theme", "Subtitle"):
        p1 += layer
    print(p1)

    # 2. IMF panel theme bar chart with panel title & subtitle
    df2 = pd.DataFrame({'category': ['A','B','C','D'], 'value': [3, 1, 4, 2]})
    p2 = (
        ggplot(df2, aes('category', 'value', fill='category'))
        + geom_bar(stat='identity')
        + scale_fill_manual(values=[blue, green, red, grey])
        + set_imf_panel_theme_plotnine()
    )
    for layer in apply_imf_panel_titles_plotnine("IMF Panel Theme Title", "Panel Subtitle"):
        p2 += layer
    print(p2)

    # 3. Text annotation demo
    p3 = add_text_to_figure_plotnine(
        ggplot(df, aes('x', 'cosx'))
        + geom_line(color=red)
        + set_imf_theme_plotnine(),
        "Caption", y_offset=1.05
    )
    print(p3)

    # 4. Alternate annotation demo
    p4 = add_text_to_figure_new_plotnine(
        ggplot(df, aes('x', 'tanx'))
        + geom_line(color=green)
        + set_imf_theme_plotnine(),
        "Centered caption demo", y_offset=1.05
    )
    print(p4)
