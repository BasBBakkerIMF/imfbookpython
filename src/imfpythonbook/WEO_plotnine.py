import numpy as np
import pandas as pd
from pathlib import Path

# plotnine (ggplot-style) equivalents
from plotnine import (
    ggplot, aes, geom_line, scale_color_manual, scale_x_continuous, scale_y_continuous,
    coord_cartesian, labs, theme, element_text, element_blank,
    facet_wrap, geom_rect, geom_segment, guides, guide_legend
)

# ---- WEO color palette and sizing ----
def rgb2(red, green, blue):
    """Convert RGB values (0-255) to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(red, green, blue)

blue        = rgb2(0, 98, 175)
red         = rgb2(170, 31, 76)
gold        = rgb2(245, 189, 71)
green       = rgb2(73, 117, 39)
light_grey  = rgb2(200, 200, 200)
light_blue  = rgb2(141, 163, 210)
light_red   = rgb2(209, 145, 131)
light_gold  = rgb2(249, 219, 161)
light_green = rgb2(162, 176, 143)
dark_grey   = rgb2(150, 150, 150)
black       = rgb2(0, 0, 0)

weo_colors = [blue, red, gold, green, light_grey, light_blue, light_red,
              light_gold, light_green, dark_grey]

# Font and sizing
primary_font_weo = 'Arial'
weo_title_size   = 10
weo_unit_size    = 9
weo_text_size    = 8

def set_weo_theme_plotnine():
    """Return a plotnine theme approximating the WEO matplotlib theme, without axis lines."""
    return theme(
        # Font & text
        text=element_text(family=primary_font_weo, size=weo_text_size, color='black'),
        # Title styling; left align
        plot_title=element_text(size=weo_title_size, weight='bold', hjust=0, color=blue),
        plot_subtitle=element_text(size=weo_unit_size, style='italic', hjust=0, color=blue),

        # Remove axis lines (baseline added manually)
        axis_line_x=element_blank(),
        axis_line_y=element_blank(),

        # Axis text: right-align y so it sits closer to inward ticks
        axis_text_x=element_text(size=weo_text_size, color='black'),
        axis_text_y=element_text(size=weo_text_size, color='black', hjust=1),

        axis_title=element_text(size=weo_unit_size),
        axis_ticks=element_blank(),

        # Grid & background
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_blank(),
        plot_background=element_blank(),

        # Legend
        legend_position=(0.05, 0.95),
        legend_direction='horizontal',
        legend_background=element_blank(),
        legend_key=element_blank(),
        legend_title=element_blank(),
        legend_spacing=0.8,
        legend_box_spacing=0.4,

        # Caption left-aligned
        plot_caption=element_text(hjust=0, size=weo_text_size),
    )

def set_weo_panel_theme_plotnine():
    base = set_weo_theme_plotnine()
    return base + theme(
        plot_title=element_text(size=8, weight='bold', hjust=0, color=blue),
        plot_subtitle=element_text(size=7, style='italic', hjust=0, color=blue),
        axis_text_x=element_text(size=7, color='black'),
        axis_text_y=element_text(size=7, color='black', hjust=1),
        axis_title=element_text(size=7),
        legend_text=element_text(size=6.5),
        strip_background=element_blank(),  # remove grey shading behind facet labels
        strip_text=element_text(size=8, color='black', hjust=0, weight='bold'),  # left-aligned bold facet titles
        strip_text_x=element_text(size=8, color='black', hjust=0, weight='bold'),
    )

# ---- break generation (same as original) ----
def generate_minor_breaks(major_breaks):
    major = np.asarray(major_breaks)
    return (major[:-1] + np.diff(major) / 2).tolist()

def generate_breaks_auto(y, major_by=None):
    y = np.asarray(y)
    y = y[~np.isnan(y)]
    if y.size == 0:
        return {'major': [], 'minor': [], 'limits': [0, 1]}
    y_min, y_max = y.min(), y.max()
    y_span = y_max - y_min
    if major_by is None:
        if y_span <= 5:
            major_by = 1
        elif y_span <= 10:
            major_by = 2
        elif y_span <= 20:
            major_by = 5
        elif y_span <= 50:
            major_by = 10
        else:
            major_by = 20
    min_y = np.floor(y_min / major_by) * major_by
    max_y = np.ceil(y_max / major_by) * major_by
    major = np.arange(min_y, max_y + major_by, major_by)
    minor = generate_minor_breaks(major)
    return {'major': major.tolist(), 'minor': minor, 'limits': [min_y, max_y]}

def make_y_tick_segments(major_breaks, minor_breaks, x_min, x_max, style='default'):
    """Create DataFrame of major and minor y-axis inward ticks (left and right)."""
    if style.lower() == 'bar':
        major_length = 0.10
        minor_length = 0.06
    else:
        major_length = 0.15
        minor_length = 0.10

    major_size = 0.4
    minor_size = 0.3

    rows = []
    for y in minor_breaks:
        rows.append({'x': x_min, 'xend': x_min + minor_length, 'y': y, 'yend': y, 'size': minor_size})
        rows.append({'x': x_max - minor_length, 'xend': x_max, 'y': y, 'yend': y, 'size': minor_size})
    for y in major_breaks:
        rows.append({'x': x_min, 'xend': x_min + major_length, 'y': y, 'yend': y, 'size': major_size})
        rows.append({'x': x_max - major_length, 'xend': x_max, 'y': y, 'yend': y, 'size': major_size})
    return pd.DataFrame(rows)

def make_x_major_tick_segments(x_breaks, y_min, y_max, tick_length_fraction=0.02, size=0.4):
    """Create vertical inward major tick segments for X axis at bottom."""
    tick_length = tick_length_fraction * (y_max - y_min)
    rows = []
    for x in x_breaks:
        rows.append({
            'x': x,
            'xend': x,
            'y': y_min,
            'yend': y_min + tick_length,
            'size': size
        })
    return pd.DataFrame(rows)

def add_forecast_shading_plotnine(start_year, end_year, y_range, fill_color=light_grey, alpha=0.3):
    """
    Return a plotnine layer that shades the forecast window.

    Parameters
    ----------
    start_year : int or float
        Beginning of forecast window on the x-axis.
    end_year : int or float
        End of forecast window on the x-axis.
    y_range : (float, float)
        Tuple/list with (ymin, ymax) to cover the plot area vertically.
    fill_color : str
        Hex color for the rectangle fill. Defaults to WEO light_grey.
    alpha : float
        Opacity of the rectangle.

    Returns
    -------
    plotnine layer (geom_rect)
    """
    import pandas as pd
    from plotnine import aes, geom_rect

    df = pd.DataFrame({
        'xmin': [start_year],
        'xmax': [end_year],
        'ymin': [y_range[0]],
        'ymax': [y_range[1]],
    })
    return geom_rect(
        data=df,
        mapping=aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
        inherit_aes=False,
        fill=fill_color,
        alpha=alpha,
    )



### Examples
# # ---- example: unemployment rate change ----
# def unemployment_example_plotnine(save_path):
#     save_path = Path(save_path)
#     save_path.parent.mkdir(parents=True, exist_ok=True)

#     years = np.arange(2000, 2026)
#     countries = ['BRA', 'CHL', 'COL', 'MEX', 'PER']
#     np.random.seed(42)
#     data = {c: np.random.randn(len(years)).cumsum() for c in countries}

#     # long format
#     df = pd.DataFrame(data, index=years).reset_index().melt(
#         id_vars='index', var_name='country', value_name='value'
#     )
#     df = df.rename(columns={'index': 'year'})

#     combined = np.concatenate([df.loc[df['country'] == c, 'value'].values for c in countries])
#     breaks = generate_breaks_auto(combined)

#     # y-axis ticks (major + minor)
#     y_tick_segs = make_y_tick_segments(
#         breaks['major'], breaks['minor'], years.min(), years.max(), style='default'
#     )

#     # x-axis major inward ticks
#     x_major_breaks = list(range(years.min(), years.max() + 1, 5))
#     x_major_ticks = make_x_major_tick_segments(
#         x_major_breaks, breaks['limits'][0], breaks['limits'][1], tick_length_fraction=0.02
#     )

#     # baseline for X axis (horizontal line) – thicker
#     baseline_df = pd.DataFrame([{
#         'x': years.min(),
#         'xend': years.max(),
#         'y': breaks['limits'][0],
#         'yend': breaks['limits'][0]
#     }])

#     # build plot
#     p = (
#         ggplot(df, aes(x='year', y='value', color='country'))
#         + geom_line(size=1)
#         + scale_color_manual(values=weo_colors[:len(countries)])
#         + scale_x_continuous(breaks=x_major_breaks, expand=(0, 0))
#         + scale_y_continuous(breaks=breaks['major'], expand=(0, 0))
#         + coord_cartesian(xlim=(years.min(), years.max()), ylim=tuple(breaks['limits']))
#         + labs(
#             title="Figure 1.2.  Unemployment Rate Change",
#             subtitle="(Percentage point change, annual data)",
#             caption="Source: IMF WEO and staff calculations.",
#             x='',
#             y='',
#         )
#         + guides(color=guide_legend(ncol=5))
#         + set_weo_theme_plotnine()
#         + geom_segment(
#             data=y_tick_segs[y_tick_segs['size'] == 0.3],
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.3,
#             color='black',
#         )
#         + geom_segment(
#             data=y_tick_segs[y_tick_segs['size'] == 0.4],
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.4,
#             color='black',
#         )
#         + geom_segment(
#             data=x_major_ticks,
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.4,
#             color='black',
#         )
#         + geom_segment(
#             data=baseline_df,
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.8,
#             color='black',
#         )
#     )

#     p.save(str(save_path), dpi=300, verbose=False)
#     print(f"Saved unemployment example to {save_path}")
#     return p

# ---- example: real GDP panel ----
# def real_gdp_panel_example_plotnine(save_path):
#     save_path = Path(save_path)
#     save_path.parent.mkdir(parents=True, exist_ok=True)

#     years = np.arange(2000, 2026)
#     countries = ['BRA', 'CHL', 'COL', 'MEX']
#     np.random.seed(123)
#     growth = {c: np.random.normal(0.02, 0.01, len(years)) for c in countries}
#     index = {c: 100 * np.cumprod(1 + growth[c]) for c in countries}

#     # build DataFrame correctly
#     df = pd.DataFrame({'year': years})
#     for c in countries:
#         df[c] = index[c]
#     df_long = df.melt(id_vars='year', var_name='country', value_name='index')

#     # create facet label with subtitle under each country
#     country_labels = {c: f"{c}\n(Index, 2010=100)" for c in countries}
#     df_long['country_label'] = df_long['country'].map(country_labels)

#     combined = np.concatenate(
#         [df_long.loc[df_long['country'] == c, 'index'].values for c in countries]
#     )
#     breaks = generate_breaks_auto(combined)

#     # y-axis tick segments per facet (attach country_label)
#     y_tick_segs_base = make_y_tick_segments(
#         breaks['major'], breaks['minor'], years.min(), years.max(), style='default'
#     )
#     y_tick_segs = pd.concat(
#         [y_tick_segs_base.assign(country_label=country_labels[c]) for c in countries],
#         ignore_index=True
#     )

#     # x-axis major ticks per facet
#     x_major_breaks = list(range(years.min(), years.max() + 1, 5))
#     x_major_ticks_base = make_x_major_tick_segments(
#         x_major_breaks, breaks['limits'][0], breaks['limits'][1], tick_length_fraction=0.02
#     )
#     x_major_ticks = pd.concat(
#         [x_major_ticks_base.assign(country_label=country_labels[c]) for c in countries],
#         ignore_index=True
#     )

#     # baseline for X axis per facet – thicker
#     baseline_df = pd.concat([
#         pd.DataFrame([{
#             'x': years.min(),
#             'xend': years.max(),
#             'y': breaks['limits'][0],
#             'yend': breaks['limits'][0],
#             'country_label': country_labels[c]
#         }]) for c in countries
#     ], ignore_index=True)

#     # forecast shading rectangle per facet
#     rects = []
#     for c in countries:
#         rects.append({
#             'xmin': 2022,
#             'xmax': 2025,
#             'ymin': breaks['limits'][0],
#             'ymax': breaks['limits'][1],
#             'country_label': country_labels[c]
#         })
#     rects_df = pd.DataFrame(rects)

#     p = (
#         ggplot(df_long, aes(x='year', y='index'))
#         + geom_rect(
#             data=rects_df,
#             mapping=aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
#             inherit_aes=False,
#             fill=light_grey,
#             alpha=0.3,
#         )
#         + geom_line(size=1, color=blue)
#         + scale_x_continuous(breaks=x_major_breaks, expand=(0, 0))
#         + scale_y_continuous(breaks=breaks['major'], expand=(0, 0))
#         + coord_cartesian(xlim=(years.min(), years.max()), ylim=tuple(breaks['limits']))
#         + facet_wrap('~country_label', ncol=2, scales='fixed')
#         + labs(
#             title="Figure X. Real GDP Panel",
#             subtitle="",  # overall subtitle omitted since per-facet has subtitle
#             caption="Source: Synthetic data. Real GDP index rebased to 2010=100.",
#             x='',
#             y='',
#         )
#         + set_weo_panel_theme_plotnine()
#         + geom_segment(
#             data=y_tick_segs[y_tick_segs['size'] == 0.3],
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.3,
#             color='black',
#         )
#         + geom_segment(
#             data=y_tick_segs[y_tick_segs['size'] == 0.4],
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.4,
#             color='black',
#         )
#         + geom_segment(
#             data=x_major_ticks,
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.4,
#             color='black',
#         )
#         + geom_segment(
#             data=baseline_df,
#             mapping=aes(x='x', xend='xend', y='y', yend='yend'),
#             inherit_aes=False,
#             size=0.8,
#             color='black',
#         )
#     )

#     p.save(str(save_path), dpi=300, verbose=False)
#     print(f"Saved real GDP panel example to {save_path}")
#     return p

# # ---- entry point ----
# if __name__ == "__main__":
#     this_dir = Path(__file__).resolve().parent
#     figures_dir = this_dir / "figures"
#     figures_dir.mkdir(parents=True, exist_ok=True)

#     unemployment_example_plotnine(figures_dir / "weo_matplotlib_plotnine.png")
#     real_gdp_panel_example_plotnine(figures_dir / "weo_real_gdp_panel_plotnine.png")
