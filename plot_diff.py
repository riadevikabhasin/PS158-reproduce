"""Each country's trust in government AI regulation relative to the 30-country average, 2025.

Same data, country order and typography as plot.py, but bars show the percentage-point
difference from the "Global" row of the CSV. Writes
figures/trust_gov_regulate_ai_2025_diff_from_avg.png. Run get_data.py first.

Usage: python plot_diff.py
"""

import matplotlib.pyplot as plt

from plot import BAR, GREY, GRID, HIGHLIGHT, HERE, SOFT, TEXT, load, pick_fonts

OUT = HERE / "figures" / "trust_gov_regulate_ai_2025_diff_from_avg.png"
BELOW = "#DB444B"  # countries below the average
MINUS = "−"


def signed(x):
    return f"+{x:.0f}" if x > 0 else f"{MINUS}{abs(x):.0f}" if x < 0 else "0"


def main():
    fonts = pick_fonts()
    data = load()  # same order as plot.py
    average = dict(data)["Global"]
    countries = [c for c, _ in data]
    diffs = [round(v - average, 6) for _, v in data]  # rounding clears float noise
    is_avg = [c == "Global" for c in countries]
    labels = [f"30-country average ({average:.0f}%)" if a else c
              for c, a in zip(countries, is_avg)]

    fig, ax = plt.subplots(figsize=(7.2, 10.5))
    fig.subplots_adjust(left=0.30, right=0.94, top=0.795, bottom=0.085)

    y = list(range(len(diffs)))
    for yi, d, a in zip(y, diffs, is_avg):
        if a:
            continue  # the zero line stands in for the average
        ax.barh(yi, d, color=BAR if d > 0 else BELOW, height=0.62, zorder=2)
        ax.text(d + (1 if d > 0 else -1), yi, signed(d), va="center",
                ha="left" if d > 0 else "right", fontsize=9.5, color=SOFT,
                fontproperties=fonts["body"])

    ax.axvline(0, color=TEXT, linewidth=1.2, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    for tick, a in zip(ax.get_yticklabels(), is_avg):
        tick.set_fontproperties(fonts["emphasis" if a else "body"])
        tick.set_fontsize(10)
        tick.set_color(TEXT if a else SOFT)

    ax.set_xlim(-30, 35)
    ax.set_ylim(-0.6, len(diffs) - 0.4)
    ax.xaxis.tick_top()
    ticks = list(range(-30, 31, 10))
    ax.set_xticks(ticks)
    ax.set_xticklabels([signed(t) for t in ticks])
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(fonts["body"])
        tick.set_fontsize(9)
        tick.set_color(GREY)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(False)

    # Direction cues in the otherwise empty average row, either side of the zero line.
    avg_y = y[is_avg.index(True)]
    ax.text(-1, avg_y, "Below average", ha="right", va="center",
            fontsize=8.5, color=BELOW, fontproperties=fonts["emphasis"])
    ax.text(1, avg_y, "Above average", ha="left", va="center",
            fontsize=8.5, color=BAR, fontproperties=fonts["emphasis"])

    x0 = 0.04
    fig.add_artist(plt.Rectangle((x0, 0.968), 0.06, 0.006, color=HIGHLIGHT,
                                 transform=fig.transFigure, clip_on=False))
    fig.text(x0, 0.950, "Trust in government AI regulation,\nrelative to the average",
             fontsize=17, color=TEXT, va="top", linespacing=1.15,
             fontproperties=fonts["headline"])
    fig.text(x0, 0.880,
             "“I trust the government of my country to regulate AI responsibly”"
             f"\nPercentage-point difference from the 30-country average of {average:.0f}%, 2025",
             fontsize=10.5, color=SOFT, va="top", linespacing=1.5,
             fontproperties=fonts["body"])

    fig.text(x0, 0.045,
             "Source: Ipsos AI Monitor 2025, via Stanford HAI AI Index Report 2026 (Fig. 9.3.1)",
             fontsize=8, color=GREY, fontproperties=fonts["body"])
    fig.text(x0, 0.027,
             "~500-2,200 adults per country, Mar 21st-Apr 4th 2025; 30-country average is unweighted",
             fontsize=8, color=GREY, fontproperties=fonts["body"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, facecolor="white")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
