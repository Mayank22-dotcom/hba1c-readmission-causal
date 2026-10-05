"""Shared figure style for the manuscript (plotting only; no estimates are computed).

One visual family for every redrawn figure:
  - lettering in the document's sans typeface (Calibri; metric-compatible Carlito,
    then Arial / DejaVu Sans as fallbacks), 8.5 pt at final printed size
  - one accent colour (navy, the same #1F4E79 used in the figures that are not
    redrawn) plus a grey scale; nothing relies on colour alone
  - 0.6 pt axes, no top/right spines, light horizontal/vertical grid
  - saved at 300 dpi at the exact size the figure is placed in the manuscript,
    so the lettering is not rescaled in Word
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ACCENT = "#1F4E79"      # navy: data marks
INK = "#1A1A1A"         # text, axes
GREY_DARK = "#595959"   # secondary text, reference lines
GREY_MID = "#9A9A9A"    # connectors
GREY_LIGHT = "#E3E5E8"  # grid
WHITE = "#FFFFFF"

FULL_WIDTH = 6.0        # inches: the text measure of the manuscript
MID_WIDTH = 4.5         # inches: for near-square plots
DPI = 300

_PREFERRED = ["Calibri", "Carlito", "Arial", "Liberation Sans", "DejaVu Sans"]


def _first_available(names):
    have = {f.name for f in font_manager.fontManager.ttflist}
    for n in names:
        if n in have:
            return n
    return "DejaVu Sans"


FONT = _first_available(_PREFERRED)


def apply():
    """Set the rcParams shared by every figure."""
    plt.rcParams.update({
        "font.family": FONT,
        "font.size": 8.5,
        "axes.labelsize": 8.5,
        "axes.titlesize": 8.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.edgecolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GREY_LIGHT,
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.2,
        "lines.markersize": 5,
        "legend.frameon": False,
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.facecolor": WHITE,
        "axes.unicode_minus": True,
    })
    return FONT


def save(fig, path):
    fig.savefig(path, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print("wrote", path)
