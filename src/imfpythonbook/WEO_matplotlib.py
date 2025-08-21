import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle
import numpy as np

def rgb2(red, green, blue):
    """Convert RGB values (0-255) to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(red, green, blue)

# WEO color palette
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

def set_weo_theme(font=primary_font_weo, font_color=blue):
    """Apply the IMF WEO theme to matplotlib figures."""
    mpl.rcParams.update({
        # Font & text
        'font.family':       font,
        'font.size':         weo_text_size,

        # Title styling
        'axes.titlesize':    weo_title_size,
        'axes.titleweight':  'bold',
        'axes.titlecolor':   font_color,

        # Axes lines
        'axes.edgecolor':    'black',
        'axes.linewidth':    0.4,

        # Tick label colors & sizes
        'xtick.color':       'black',
        'ytick.color':       'black',
        'xtick.labelsize':   weo_text_size,
        'ytick.labelsize':   weo_text_size,

        # Grid & background
        'grid.color':        'none',
        'figure.facecolor':  'white',

        # Legend
        'legend.frameon':    False,
        'legend.loc':        'upper left',
        'legend.columnspacing':  0.8,    # space between columns
        'legend.handletextpad':  0.4,    # space between line and label

        # Reserve space for subtitle under the title
        'figure.subplot.top': 0.82,

        # X-axis ticks: inward, 4pt major, no minor
        'xtick.direction':    'in',
        'xtick.major.size':   4,
        'xtick.major.width':  0.4,
        'xtick.minor.size':   0,

        # Y-axis: disable default ticks so only add_y_ticks applies
        'ytick.major.size':   0,
        'ytick.minor.size':   0,
    })

def set_weo_panel_theme(font=primary_font_weo, font_color=black):
    """Apply WEO panel theme to matplotlib (smaller text, etc.)."""
    set_weo_theme(font, font_color)
    mpl.rcParams.update({
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'axes.labelsize': 7,
        'axes.titlesize': 8,
        'legend.fontsize': 6.5,
    })

def generate_minor_breaks(major_breaks):
    """Generate one minor break between each pair of major breaks."""
    major = np.asarray(major_breaks)
    return (major[:-1] + np.diff(major) / 2).tolist()

def generate_breaks_auto(y, major_by=None):
    """Generate clean major and minor breaks from Y data range."""
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

def add_y_ticks(ax, major_breaks, minor_breaks, x_min, x_max,
                style='default', major_length=None, minor_length=None,
                major_size=0.4, minor_size=0.3):
    """Add both major and minor Y ticks on left and right (R-matched defaults)."""
    style = style.lower()

    if style == 'bar':
        if major_length is None:
            major_length = 0.10
        if minor_length is None:
            minor_length = 0.06
    else:
        if major_length is None:
            major_length = 0.15
        if minor_length is None:
            minor_length = 0.10

    for y in minor_breaks:
        ax.plot([x_min, x_min + minor_length], [y, y],
                linewidth=minor_size, color='black')
        ax.plot([x_max - minor_length, x_max], [y, y],
                linewidth=minor_size, color='black')

    for y in major_breaks:
        ax.plot([x_min, x_min + major_length], [y, y],
                linewidth=major_size, color='black')
        ax.plot([x_max - major_length, x_max], [y, y],
                linewidth=major_size, color='black')

def add_forecast_shading(ax, start_year, end_year, y_range=None, fill_color=light_grey):
    """Add forecast shading to a plot between start_year and end_year."""
    if y_range is None:
        ymin, ymax = ax.get_ylim()
    else:
        ymin, ymax = y_range
    rect = Rectangle((start_year, ymin), end_year - start_year, ymax - ymin,
                     facecolor=fill_color, alpha=0.3, edgecolor=None, zorder=0)
    ax.add_patch(rect)

def add_weo_title(
    ax,
    title: str,
    subtitle: str = None,
    title_color: str = blue,
    title_size: float = weo_title_size,
    subtitle_size: float = weo_unit_size,
    subtitle_style: str = 'italic',
    pad: float = 12
):
    """
    Add a left-aligned WEO title and optional subtitle.
    """
    ax.set_title(
        title,
        loc='left',
        color=title_color,
        fontsize=title_size,
        fontweight='bold',
        pad=pad
    )
    if subtitle:
        ax.text(
            0, 1.00,
            subtitle,
            transform=ax.transAxes,
            ha='left', va='bottom',
            color=title_color,
            fontsize=subtitle_size,
            fontstyle=subtitle_style
        )

def add_x_end_ticks(ax, x_min, x_max,
                    major_length: float = 0.15,
                    size: float = 0.4):
    """
    Draw inward-facing ticks at the start and end of the X-axis.
    """
    y0, _ = ax.get_ylim()
    ax.plot([x_min, x_min + major_length], [y0, y0],
            linewidth=size, color='black')
    ax.plot([x_max - major_length, x_max], [y0, y0],
            linewidth=size, color='black')

### Example charts

# def unemployment_example(save_path):
#     """Create and save the unemployment rate change example."""
#     from pathlib import Path
#     save_path = Path(save_path)
#     save_path.parent.mkdir(parents=True, exist_ok=True)

#     set_weo_theme()
#     years = np.arange(2000, 2026)
#     countries = ['BRA', 'CHL', 'COL', 'MEX', 'PER']
#     np.random.seed(42)
#     data = {c: np.random.randn(len(years)).cumsum() for c in countries}

#     breaks = generate_breaks_auto(np.concatenate(list(data.values())))

#     fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

#     for i, country in enumerate(countries):
#         ax.plot(
#             years,
#             data[country],
#             label=country,
#             color=weo_colors[i],
#             linewidth=1
#         )

#     for spine in ['top', 'left', 'right']:
#         ax.spines[spine].set_visible(False)
#     ax.spines['bottom'].set_linewidth(0.4)
#     ax.grid(False)

#     ax.set_xticks(years[::5])
#     ax.set_xlim(years.min(), years.max())
#     ax.set_yticks(breaks['major'])
#     ax.set_ylim(breaks['limits'])

#     add_y_ticks(ax, breaks['major'], breaks['minor'], years.min(), years.max())
#     add_x_end_ticks(ax, years.min(), years.max())

#     ax.legend(
#         loc='upper left',
#         bbox_to_anchor=(0.05, 0.95),
#         frameon=False,
#         fontsize=weo_text_size,
#         ncol=5
#     )

#     add_weo_title(
#         ax,
#         "Figure 1.2.  Unemployment Rate Change",
#         "(Percentage point change, annual data)"
#     )

#     ax.text(
#         0,
#         -0.25,
#         "Source: IMF WEO and staff calculations.",
#         transform=ax.transAxes,
#         ha='left',
#         fontsize=weo_text_size
#     )

#     plt.tight_layout()
#     fig.savefig(save_path, dpi=300, bbox_inches='tight')
#     print(f"Saved example plot to {save_path}")
#     return fig

# def real_gdp_panel_example(save_path):
#     """Create and save the real GDP panel example."""
#     from pathlib import Path
#     save_path = Path(save_path)
#     save_path.parent.mkdir(parents=True, exist_ok=True)

#     set_weo_panel_theme()
#     years = np.arange(2000, 2026)
#     countries = ['BRA', 'CHL', 'COL', 'MEX']
#     np.random.seed(123)
#     growth = {c: np.random.normal(0.02, 0.01, len(years)) for c in countries}
#     index = {c: 100 * np.cumprod(1 + growth[c]) for c in countries}

#     combined = np.concatenate([index[c] for c in countries])
#     breaks = generate_breaks_auto(combined)

#     fig, axs = plt.subplots(2, 2, figsize=(10, 6), sharey=True)
#     axs_flat = axs.flatten()

#     for ax, country in zip(axs_flat, countries):
#         for spine in ['top', 'left', 'right']:
#             ax.spines[spine].set_visible(False)
#         ax.spines['bottom'].set_linewidth(0.4)
#         ax.grid(False)

#         ax.plot(years, index[country], linewidth=1, color=blue)

#         ax.set_xticks(years[::5])
#         ax.set_xlim(years.min(), years.max())
#         ax.set_yticks(breaks['major'])
#         ax.set_ylim(breaks['limits'])

#         add_y_ticks(ax, breaks['major'], breaks['minor'], years.min(), years.max())
#         add_x_end_ticks(ax, years.min(), years.max())

#         ax.set_title(country, loc='left', fontsize=8, fontweight='bold')

#         add_forecast_shading(ax, start_year=2022, end_year=2025, y_range=breaks['limits'])

#     fig.suptitle("Figure X. Real GDP Panel", x=0.01, ha='left',
#                  fontsize=10, fontweight='bold', color=blue)
#     fig.text(0.01, 0.93, "(Index, 2010=100)", ha='left',
#              fontsize=9, fontstyle='italic', color=blue)
#     fig.text(0, -0.02, "Source: Synthetic data. Real GDP index rebased to 2010=100.",
#              ha='left', fontsize=8)

#     plt.tight_layout(rect=[0, 0, 1, 0.90])
#     fig.savefig(save_path, dpi=300, bbox_inches='tight')
#     print(f"Saved real GDP panel to {save_path}")
#     return fig

# # Entry point
# if __name__ == "__main__":
#     from pathlib import Path

#     base_dir = Path(r"C:\Users\gpolo\Desktop\Python Book\PythonBookCode\Python\PythonBookExamples\Utils")
#     # Singular unemployment plot
#     singular_path = base_dir / "weo_matplotlib.png"
#     unemployment_example(singular_path)

#     # Panel real GDP plot
#     panel_path = base_dir / "weo_real_gdp_panel.png"
#     real_gdp_panel_example(panel_path)

#     # Show both (interactive)
#     try:
#         plt.show()
#     except KeyboardInterrupt:
#         pass
