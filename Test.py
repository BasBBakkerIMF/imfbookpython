import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import (
    ggplot, aes, geom_line, geom_bar, scale_fill_manual,
    scale_y_continuous, facet_wrap, ggtitle, labs
)
import imfpythonbook as ip

# Setup
x = np.linspace(0, 10, 100)
df = pd.DataFrame({"x": x, "sinx": np.sin(x), "cosx": np.cos(x), "tanx": np.tan(x)})
df_bar = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [3, 1, 4, 2]})

# --- IMF_matplotlib Tests ---
def test_imf_matplotlib_line():
    ip.matplotlib.set_imf_theme()
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), color=ip.colors.blue)
    ip.matplotlib.set_titles(ax, "IMF Theme", "Subtitle")
    plt.show()

def test_imf_matplotlib_bar():
    ip.matplotlib.set_imf_panel_theme()
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C", "D"], [3, 1, 4, 2],
           color=[ip.colors.blue, ip.colors.green, ip.colors.red, ip.colors.grey])
    ip.matplotlib.set_panel_titles(ax, "Panel Title", "Panel Subtitle")
    plt.show()

def test_imf_matplotlib_annotation():
    fig, ax = plt.subplots()
    ax.plot(x, np.cos(x), color=ip.colors.red)
    # Keep module-specific helpers as-is (not aliased on purpose)
    ip.IMF_matplotlib.add_text_to_figure(fig, "Figure Caption", y_offset=0.9)
    plt.show()

def test_imf_matplotlib_alt_annotation():
    fig, ax = plt.subplots()
    ax.plot(x, np.tan(x), color=ip.colors.green)
    ip.IMF_matplotlib.add_text_to_figure_new(fig, "Centered Caption", y_offset=0.8)
    plt.show()

# --- IMF_plotnine Tests ---
def test_imf_plotnine_line():
    p = (
        ggplot(df, aes("x", "sinx"))
        + geom_line(color=ip.colors.blue)
        + ip.plotnine.set_imf_theme()
    )
    for layer in ip.plotnine.set_titles("IMF Theme", "Subtitle"):
        p += layer
    print(p)

def test_imf_plotnine_bar():
    p = (
        ggplot(df_bar, aes("category", "value", fill="category"))
        + geom_bar(stat="identity" )
        + scale_fill_manual(values=[ip.colors.blue, ip.colors.green, ip.colors.red, ip.colors.grey])
        + ip.plotnine.set_imf_panel_theme()
    )
    for layer in ip.plotnine.set_panel_titles("Panel Title", "Panel Subtitle"):
        p += layer
    print(p)

def test_imf_plotnine_annotation():
    p = ip.IMF_plotnine.add_text_to_figure_plotnine(
        ggplot(df, aes("x", "cosx"))
        + geom_line(color=ip.colors.red)
        + ip.plotnine.set_imf_theme(),
        "Caption", y_offset=1.05
    )
    print(p)

def test_imf_plotnine_alt_annotation():
    p = ip.IMF_plotnine.add_text_to_figure_new_plotnine(
        ggplot(df, aes("x", "tanx"))
        + geom_line(color=ip.colors.green)
        + ip.plotnine.set_imf_theme(),
        "Centered Caption", y_offset=1.05
    )
    print(p)

# --- WEO Matplotlib Example Rebuilds ---
def test_weo_theme_unemployment_demo():
    from imfpythonbook.WEO_matplotlib import (
        set_weo_theme, add_y_ticks, add_x_end_ticks, add_weo_title,
        generate_breaks_auto, weo_colors, weo_text_size
    )

    set_weo_theme()
    years = np.arange(2000, 2026)
    countries = ['BRA', 'CHL', 'COL', 'MEX', 'PER']
    np.random.seed(42)
    data = {c: np.random.randn(len(years)).cumsum() for c in countries}
    breaks = generate_breaks_auto(np.concatenate(list(data.values())))

    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    for i, country in enumerate(countries):
        ax.plot(years, data[country], label=country, color=weo_colors[i], linewidth=1)

    ax.set_xticks(years[::5])
    ax.set_xlim(years.min(), years.max())
    ax.set_yticks(breaks['major'])
    ax.set_ylim(breaks['limits'])

    for spine in ['top', 'left', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.4)
    ax.grid(False)

    add_y_ticks(ax, breaks['major'], breaks['minor'], years.min(), years.max())
    add_x_end_ticks(ax, years.min(), years.max())

    ax.legend(
        loc='upper left',
        bbox_to_anchor=(0.05, 0.95),
        frameon=False,
        fontsize=weo_text_size,
        ncol=5
    )

    add_weo_title(ax, "Figure 1.2. Unemployment Rate Change", "(Percentage point change, annual data)")
    ax.text(0, -0.25, "Source: IMF WEO and staff calculations.", transform=ax.transAxes, ha='left', fontsize=weo_text_size)

    plt.tight_layout()
    plt.show()

def test_weo_theme_gdp_panel_demo():
    from imfpythonbook.WEO_matplotlib import (
        set_weo_panel_theme, add_y_ticks, add_x_end_ticks, add_forecast_shading,
        generate_breaks_auto, weo_colors, blue
    )

    years = np.arange(2000, 2026)
    countries = ['BRA', 'CHL', 'COL', 'MEX']
    np.random.seed(123)
    growth = {c: np.random.normal(0.02, 0.01, len(years)) for c in countries}
    index = {c: 100 * np.cumprod(1 + growth[c]) for c in countries}
    combined = np.concatenate([index[c] for c in countries])
    breaks = generate_breaks_auto(combined)

    set_weo_panel_theme()
    fig, axs = plt.subplots(2, 2, figsize=(10, 6), sharey=True)
    axs_flat = axs.flatten()

    for ax, country in zip(axs_flat, countries):
        ax.plot(years, index[country], linewidth=1, color=blue)
        ax.set_xticks(years[::5])
        ax.set_xlim(years.min(), years.max())
        ax.set_yticks(breaks['major'])
        ax.set_ylim(breaks['limits'])

        for spine in ['top', 'left', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_linewidth(0.4)
        ax.grid(False)

        add_y_ticks(ax, breaks['major'], breaks['minor'], years.min(), years.max())
        add_x_end_ticks(ax, years.min(), years.max())
        ax.set_title(country, loc='left', fontsize=8, fontweight='bold')
        add_forecast_shading(ax, start_year=2022, end_year=2025, y_range=breaks['limits'])

    fig.suptitle("Figure X. Real GDP Panel", x=0.01, ha='left',
                 fontsize=10, fontweight='bold', color=blue)
    fig.text(0.01, 0.93, "(Index, 2010=100)", ha='left', fontsize=9, fontstyle='italic', color=blue)
    fig.text(0, -0.02, "Source: Synthetic data. Real GDP index rebased to 2010=100.",
             ha='left', fontsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.show()

# --- WEO Plotnine Example Rebuilds ---
def test_weo_plotnine_unemployment_demo():
    from imfpythonbook.WEO_plotnine import (
        set_weo_theme_plotnine, generate_breaks_auto, weo_colors
    )

    years = list(range(2000, 2026))
    countries = ['BRA', 'CHL', 'COL', 'MEX', 'PER']
    np.random.seed(42)
    data = {"year": [], "country": [], "value": []}

    for i, c in enumerate(countries):
        vals = np.random.randn(len(years)).cumsum()
        data["year"] += years
        data["country"] += [c] * len(years)
        data["value"] += list(vals)

    df = pd.DataFrame(data)
    breaks = generate_breaks_auto(df["value"])

    p = (
        ggplot(df, aes("year", "value", color="country"))
        + geom_line(size=0.7)
        + scale_y_continuous(breaks=breaks["major"], limits=breaks["limits"])
        + set_weo_theme_plotnine()
        + ggtitle("Figure 1.2. Unemployment Rate Change")
        + labs(
            subtitle="(Percentage point change, annual data)",
            caption="Source: IMF WEO and staff calculations."
        )
    )
    print(p)

def test_weo_plotnine_gdp_panel_demo():
    from imfpythonbook.WEO_plotnine import (
        set_weo_panel_theme_plotnine,
        generate_breaks_auto,
        add_forecast_shading_plotnine,
        blue
    )

    years = list(range(2000, 2026))
    countries = ['BRA', 'CHL', 'COL', 'MEX']
    np.random.seed(123)
    df = []

    for country in countries:
        growth = np.random.normal(0.02, 0.01, len(years))
        index = 100 * np.cumprod(1 + growth)
        df.append(pd.DataFrame({
            "year": years,
            "value": index,
            "country": country
        }))

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
        + labs(
            subtitle="(Index, 2010=100)",
            caption="Source: Synthetic data. Real GDP index rebased to 2010=100."
        )
    )
    print(p)

# --- Entry Point ---
if __name__ == "__main__":
    test_imf_matplotlib_line()
    test_imf_matplotlib_bar()
    test_imf_matplotlib_annotation()
    test_imf_matplotlib_alt_annotation()

    test_imf_plotnine_line()
    test_imf_plotnine_bar()
    test_imf_plotnine_annotation()
    test_imf_plotnine_alt_annotation()

    test_weo_theme_unemployment_demo()
    test_weo_theme_gdp_panel_demo()

    test_weo_plotnine_unemployment_demo()
    test_weo_plotnine_gdp_panel_demo()
