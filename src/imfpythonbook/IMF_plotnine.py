"""
Utilities for IMF-styled Plotnine charts, mirroring original R/ggplot2 utilities.
Provides:
- RGB-to-hex palette definitions
- Original and 2027 IMF standard and panel themes
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
blue_2027   = rgb2(0, 76, 151)
imf_blue_2027 = blue_2027
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

def _imf_theme_plotnine(
    font,
    font_color,
    panel,
    hide_axis_titles,
    legend_title_format,
    legend_position,
    legend_direction,
    legend_key_height,
    legend_key_width,
    legend_spacing_x,
    legend_spacing_y,
    figure_size,
):
    text_size = 14 if panel else 18
    axis_size = 14 if panel else 18
    title_size = 18 if panel else 24
    subtitle_size = 16 if panel else 20
    axis_titles = (
        element_blank()
        if hide_axis_titles
        else element_text(size=axis_size, family=font)
    )
    return (
        theme_classic()
        + theme(
            text=element_text(family=font, size=text_size, color="black"),
            axis_title=axis_titles,
            axis_text=element_text(
                size=axis_size,
                family=font,
                color="black",
            ),
            axis_text_y=element_text(
                size=axis_size,
                family=font,
                color="black",
                margin={"r": 3.5 * 72 / 25.4, "unit": "pt"},
            ),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_line(color=light_grey),
            axis_ticks_length_major_y=-(2 * 72 / 25.4),
            axis_line=element_line(color=light_grey),
            panel_border=element_rect(color=light_grey, fill=None, size=1),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            plot_title=element_text(
                size=title_size,
                family=font,
                weight="bold",
                color=font_color,
                ha="left",
            ),
            plot_subtitle=element_text(
                size=subtitle_size,
                family=font,
                style="normal",
                color=font_color,
                ha="left",
            ),
            plot_caption=element_text(
                size=12 if panel else 16,
                family=font,
                ha="left",
                va="bottom",
            ),
            figure_size=figure_size,
            plot_margin=0.02,
            legend_title=(
                element_blank()
                if legend_title_format is None
                else legend_title_format
            ),
            legend_text=element_text(size=text_size, family=font),
            legend_position=legend_position,
            legend_direction=legend_direction,
            legend_key_height=legend_key_height,
            legend_key_width=legend_key_width,
            legend_key_spacing_x=legend_spacing_x,
            legend_key_spacing_y=legend_spacing_y,
        )
    )


def set_imf_theme_plotnine(
    font="Segoe UI",
    font_color=blue,
    legend_title_format=None,
    legend_position="bottom",
    legend_direction="horizontal",
    legend_key_height=4.5 * 72 / 25.4,
    legend_key_width=13 * 72 / 25.4,
    legend_spacing_x=2 * 72 / 25.4,
    legend_spacing_y=2.5 * 72 / 25.4,
    figure_size=(8.5, 5.5),
):
    """Return the original IMF Plotnine theme, matching ``theme_imf`` in R."""
    return _imf_theme_plotnine(
        font, font_color, False, False, legend_title_format, legend_position,
        legend_direction, legend_key_height, legend_key_width, legend_spacing_x,
        legend_spacing_y, figure_size,
    )


def set_imf_panel_theme_plotnine(
    font="Segoe UI",
    font_color=blue,
    legend_title_format=None,
    legend_position="bottom",
    legend_direction="horizontal",
    legend_key_height=4.5 * 72 / 25.4,
    legend_key_width=13 * 72 / 25.4,
    legend_spacing_x=2 * 72 / 25.4,
    legend_spacing_y=2.5 * 72 / 25.4,
    figure_size=(8.5, 5.5),
):
    """Return the original IMF panel theme, matching ``theme_imf_panel`` in R."""
    return _imf_theme_plotnine(
        font, font_color, True, False, legend_title_format, legend_position,
        legend_direction, legend_key_height, legend_key_width, legend_spacing_x,
        legend_spacing_y, figure_size,
    )


def set_imf_2027_theme_plotnine(
    font="Arial",
    font_color="black",
    legend_title_format=None,
    legend_position="bottom",
    legend_direction="horizontal",
    legend_key_height=4.5 * 72 / 25.4,
    legend_key_width=13 * 72 / 25.4,
    legend_spacing_x=2 * 72 / 25.4,
    legend_spacing_y=2.5 * 72 / 25.4,
    figure_size=(8.5, 5.5),
):
    """Return the 2027 IMF Plotnine theme, matching ``theme_imf_2027`` in R."""
    return _imf_theme_plotnine(
        font, font_color, False, True, legend_title_format, legend_position,
        legend_direction, legend_key_height, legend_key_width, legend_spacing_x,
        legend_spacing_y, figure_size,
    )


def set_imf_panel_2027_theme_plotnine(
    font="Arial",
    font_color="black",
    legend_title_format=None,
    legend_position="bottom",
    legend_direction="horizontal",
    legend_key_height=4.5 * 72 / 25.4,
    legend_key_width=13 * 72 / 25.4,
    legend_spacing_x=2 * 72 / 25.4,
    legend_spacing_y=2.5 * 72 / 25.4,
    figure_size=(8.5, 5.5),
):
    """Return the 2027 IMF panel theme, matching ``theme_imf_panel_2027`` in R."""
    return _imf_theme_plotnine(
        font, font_color, True, True, legend_title_format, legend_position,
        legend_direction, legend_key_height, legend_key_width, legend_spacing_x,
        legend_spacing_y, figure_size,
    )


def set_imf_panel_title_theme_plotnine(font="Segoe UI", font_color=blue):
    """Return a centered title theme matching ``theme_imf_panel_title`` in R."""
    return theme(
        plot_title=element_text(
            family=font,
            size=26,
            weight="bold",
            color=font_color,
            ha="center",
        ),
        plot_subtitle=element_text(
            family=font,
            size=20,
            color=font_color,
            ha="center",
        ),
    )


def set_imf_panel_title_2027_theme_plotnine(font="Arial", font_color=blue_2027):
    """Return a centered 2027 panel title theme matching ``theme_imf_panel_title_2027`` in R."""
    return theme(
        plot_title=element_text(
            family=font,
            size=26,
            weight="bold",
            color=font_color,
            ha="center",
        ),
        plot_subtitle=element_text(
            family=font,
            size=20,
            color=font_color,
            ha="center",
        ),
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
    assert blue_2027 == rgb2(0, 76, 151)

def _test_palettes():
    assert isinstance(A4_colors, list) and len(A4_colors) >= 3
    assert A4_colors[0] == blue
    assert "black" in A4_colors_bar
    assert blue == rgb2(75, 130, 173)

# Additional self-tests for the panel title helpers.
def _test_panel_title_theme_helpers():
    standard = set_imf_panel_title_theme_plotnine()
    assert standard.themeables["plot_title"]._properties["color"] == blue
    assert standard.themeables["plot_title"]._properties["ha"] == "center"
    assert standard.themeables["plot_title"]._properties["size"] == 26
    assert standard.themeables["plot_subtitle"]._properties["color"] == blue

    updated = set_imf_panel_title_2027_theme_plotnine()
    assert updated.themeables["plot_title"]._properties["color"] == blue_2027
    assert updated.themeables["plot_title"]._properties["family"] == "Arial"
    assert updated.themeables["plot_title"]._properties["size"] == 26


def _test_panel_theme_font_sizes():
    standard = set_imf_theme_plotnine()
    panel = set_imf_panel_theme_plotnine()
    standard_2027 = set_imf_2027_theme_plotnine()
    panel_2027 = set_imf_panel_2027_theme_plotnine()

    for standard_theme, panel_theme in (
        (standard, panel),
        (standard_2027, panel_2027),
    ):
        for element in ("text", "axis_text", "plot_title", "plot_subtitle", "legend_text"):
            assert (
                panel_theme.themeables[element]._properties["size"]
                < standard_theme.themeables[element]._properties["size"]
            )


# Demonstrations
if __name__ == "__main__":
    # Run tests
    _test_rgb2()
    _test_palettes()
    _test_panel_title_theme_helpers()
    _test_panel_theme_font_sizes()

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
