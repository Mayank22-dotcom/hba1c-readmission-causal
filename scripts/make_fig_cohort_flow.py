"""Draw the cohort-flow diagram (manuscript Figure 2) from the saved tables.

Reads results/tables/cohort_flow_v2.csv and results/tables/master_table.csv.
Plotting only: every number comes from those files or is a difference of two of
them (patients excluded = unique patients - primary cohort). Nothing is re-estimated.

Run from the repository root:  python scripts/make_fig_cohort_flow.py
"""
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, os.path.dirname(__file__))
import figstyle as fs

fs.apply()
T = "results/tables/"
flow = pd.read_csv(T + "cohort_flow_v2.csv").set_index("Step")["N"]
mt = pd.read_csv(T + "master_table.csv").set_index("Quantity")

n_enc = int(flow["Raw encounters"])
n_pat = int(flow["Unique patients"])
n_a = int(flow["Order A: exclude then first (PRIMARY)"])
n_excl = n_pat - n_a
n1, n0 = int(mt.loc["N", "Tested (A=1)"]), int(mt.loc["N", "Untested (A=0)"])
e1, e0 = int(mt.loc["Outcome events", "Tested (A=1)"]), int(mt.loc["Outcome events", "Untested (A=0)"])
r1, r0 = float(mt.loc["Unadjusted 30-day risk (%)", "Tested (A=1)"]), float(mt.loc["Unadjusted 30-day risk (%)", "Untested (A=0)"])

# consistency checks against the locked results
assert (n_enc, n_pat, n_a) == (101766, 71518, 69990)
assert n1 + n0 == n_a and (n1, n0, e1, e0) == (12846, 57144, 1079, 5206)

W, H = fs.FULL_WIDTH, 3.9                      # inches; coordinates below are inches too
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
LW = 0.8


def box(x, y, w, h, text, edge=fs.ACCENT):
    """Rounded box with its lower-left corner at (x, y)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=fs.WHITE, ec=edge, lw=LW))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", linespacing=1.4, color=fs.INK)


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.22", lw=LW,
                                color=fs.GREY_DARK, shrinkA=0, shrinkB=0))


def line(xs, ys):
    ax.plot(xs, ys, color=fs.GREY_DARK, lw=LW, solid_capstyle="butt")


xm = 2.25                                       # x of the main (vertical) flow
box(xm - 1.45, 3.33, 2.9, 0.50,
    f"Diabetes 130-US Hospitals, 1999–2008\n{n_enc:,} encounters from {n_pat:,} patients")
box(3.62, 2.32, 2.32, 0.78,
    f"Excluded: {n_excl:,} patients\nevery encounter ended in death or\nhospice discharge (disposition codes\n11, 13, 14, 19, 20, 21)",
    edge=fs.GREY_MID)
box(xm - 1.45, 1.56, 2.9, 0.64,
    f"Primary cohort: {n_a:,} patients\nearliest remaining encounter per patient\n(ordered by encounter_id)")
box(0.06, 0.06, 2.55, 0.98,
    f"HbA1c measured (A = 1)\nn = {n1:,} ({n1 / n_a:.2%})\n\nReadmitted within 30 days\n{e1:,} ({r1:.2f}%)")
box(3.39, 0.06, 2.55, 0.98,
    f"HbA1c not measured (A = 0)\nn = {n0:,} ({n0 / n_a:.2%})\n\nReadmitted within 30 days\n{e0:,} ({r0:.2f}%)")

arrow(xm, 3.33, xm, 2.20)                       # source -> primary cohort
arrow(xm, 2.71, 3.62, 2.71)                     # -> excluded
line([xm, xm], [1.56, 1.30])                    # primary cohort -> split
x_l, x_r = 0.06 + 2.55 / 2, 3.39 + 2.55 / 2
line([x_l, x_r], [1.30, 1.30])
arrow(x_l, 1.30, x_l, 1.04)
arrow(x_r, 1.30, x_r, 1.04)

fs.save(fig, "results/figures/fig2_cohort_flow.png")
