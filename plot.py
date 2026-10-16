"""Ranked bar chart of trust in government to regulate AI, 2025.

Reads the CSV saved by get_data.py and writes figures/trust_gov_regulate_ai_2025.png
(and .pdf). Run get_data.py first.

Usage: python plot.py
"""

import csv
import logging
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from fontTools.ttLib import TTCollection, TTFont
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

HERE = Path(__file__).parent
DATA = HERE / "data" / "raw" / "fig_9.3.1.csv"
OUT = HERE / "figures" / "trust_gov_regulate_ai_2025"

BAR = "#006BA2"      # blue for countries
HIGHLIGHT = "#E3120B"  # red for the 30-country average
TEXT = "#0C0C0C"
SOFT = "#3A3A3A"     # country names and values, a touch lighter than the headline
GREY = "#758D99"
GRID = "#D5DEE3"

# Preferred typefaces, first one installed wins. Each maps a role to a named weight.
FAMILIES = [
    ("Avenir Next", {"headline": "Bold", "body": "Regular", "emphasis": "Demi Bold"}),
    ("Helvetica Neue", {"headline": "Bold", "body": "Light", "emphasis": "Medium"}),
    ("Inter", {"headline": "Bold", "body": "Light", "emphasis": "SemiBold"}),
]

mpl.rcParams["pdf.fonttype"] = 42  # embed real TrueType fonts in the PDF
logging.getLogger("fontTools").setLevel(logging.ERROR)  # quiet warnings about system fonts


def installed_faces():
    """Map (family, style) -> (font file, face index) for installed faces of FAMILIES."""
    wanted = [family.replace(" ", "").lower() for family, _ in FAMILIES]
    faces = {}
    for path in font_manager.findSystemFonts():
        if not any(w in Path(path).name.replace(" ", "").lower() for w in wanted):
            continue
        try:
            if path.lower().endswith(".ttc"):
                fonts = TTCollection(path, lazy=True).fonts
            else:
                fonts = [TTFont(path, lazy=True)]
        except Exception:
            continue
        for i, font in enumerate(fonts):
            name = font["name"]
            family = name.getDebugName(16) or name.getDebugName(1)
            style = name.getDebugName(17) or name.getDebugName(2)
            faces.setdefault((family, style), (path, i))
    return faces


def face_file(path, index, family, style):
    """Matplotlib 3.9 only reads the first face of a .ttc, so save other faces as .ttf."""
    if not path.lower().endswith(".ttc"):
        return path
    cache = Path(mpl.get_cachedir()) / "ttc_faces"
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / f"{family}-{style}.ttf".replace(" ", "")
    if not out.exists():
        TTCollection(path).fonts[index].save(out)
    return str(out)


def pick_fonts():
    """Return {role: FontProperties} for the first preferred family that is installed."""
    faces = installed_faces()
    for family, roles in FAMILIES:
        if all((family, style) in faces for style in roles.values()):
            print(f"Using {family}")
            return {role: FontProperties(fname=face_file(*faces[(family, style)], family, style))
                    for role, style in roles.items()}
    print("None of the preferred fonts found; using matplotlib defaults")
    return {"headline": FontProperties(weight="bold"), "body": FontProperties(),
            "emphasis": FontProperties(weight="bold")}


def load():
    with open(DATA, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    data = [(r["Country"], float(r["% of respondents"]) * 100) for r in rows]
    assert {r["Year"] for r in rows} == {"2025"}
    # barh draws the first row at the bottom: ascending values, ties read A-Z from the top.
    data = sorted(data, key=lambda d: d[0], reverse=True)
    return sorted(data, key=lambda d: d[1])


def main():
    fonts = pick_fonts()
    data = load()
    countries = [c for c, _ in data]
    values = [v for _, v in data]
    is_avg = [c == "Global" for c in countries]
    labels = ["30-country average" if a else c for c, a in zip(countries, is_avg)]
    colors = [HIGHLIGHT if a else BAR for a in is_avg]

    fig, ax = plt.subplots(figsize=(7.2, 10.5))
    fig.subplots_adjust(left=0.27, right=0.94, top=0.795, bottom=0.085)

    y = range(len(values))
    ax.barh(y, values, color=colors, height=0.62, zorder=2)

    for yi, v, a in zip(y, values, is_avg):
        ax.text(v + 1.2, yi, f"{v:.0f}", va="center", fontsize=9.5,
                color=HIGHLIGHT if a else SOFT,
                fontproperties=fonts["emphasis" if a else "body"])

    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    for tick, a in zip(ax.get_yticklabels(), is_avg):
        tick.set_fontproperties(fonts["emphasis" if a else "body"])
        tick.set_fontsize(10)
        tick.set_color(HIGHLIGHT if a else SOFT)

    # Economist-style axes: values on top, vertical gridlines, no frame.
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(values) - 0.4)
    ax.xaxis.tick_top()
    ax.set_xticks(range(0, 101, 20))
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(fonts["body"])
        tick.set_fontsize(9)
        tick.set_color(GREY)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    for side in ["top", "right", "bottom"]:
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(TEXT)
    ax.spines["left"].set_linewidth(1.0)

    # Red tag, headline and subtitle, aligned to the left edge of the figure.
    x0 = 0.04
    fig.add_artist(plt.Rectangle((x0, 0.968), 0.06, 0.006, color=HIGHLIGHT,
                                 transform=fig.transFigure, clip_on=False))
    fig.text(x0, 0.950, "Trust in government AI regulation\nvaries sharply across countries",
             fontsize=17, color=TEXT, va="top", linespacing=1.15,
             fontproperties=fonts["headline"])
    fig.text(x0, 0.880,
             "“I trust the government of my country to regulate AI responsibly”"
             "\n% agreeing, 2025",
             fontsize=10.5, color=SOFT, va="top", linespacing=1.5,
             fontproperties=fonts["body"])

    fig.text(x0, 0.045,
             "Source: Ipsos AI Monitor 2025, via Stanford HAI AI Index Report 2026 (Fig. 9.3.1)",
             fontsize=8, color=GREY, fontproperties=fonts["body"])
    fig.text(x0, 0.027,
             "~500-2,200 adults per country, Mar 21st-Apr 4th 2025; 30-country average is unweighted",
             fontsize=8, color=GREY, fontproperties=fonts["body"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".png"), dpi=200, facecolor="white")
    fig.savefig(OUT.with_suffix(".pdf"), facecolor="white")
    print(f"Saved {OUT}.png and .pdf")


if __name__ == "__main__":
    main()
