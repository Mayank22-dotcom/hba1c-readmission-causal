"""Draw the covariate-balance (Love) plot (manuscript Appendix Figure A1).

Reads results/tables/balance_v2.csv (written by the notebook, cell 27) and plots the
absolute standardized mean differences before and after stabilized inverse
probability weighting. Plotting only: the values are those in the CSV.

Run from the repository root:  python scripts/make_fig_love_plot.py
"""
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import figstyle as fs
from admission_labels import label, check_against_mapping

fs.apply()
check_against_mapping("IDs_mapping.csv")   # checks labels if the UCI file is present

b = pd.read_csv("results/tables/balance_v2.csv")
assert len(b) == 42
b["before"] = b["SMD before"].abs()
b["after"] = b["SMD after"].abs()
assert (b["before"] > 0.1).sum() == 11 and (b["after"] > 0.1).sum() == 0
b = b.sort_values("before").reset_index(drop=True)
b["label"] = b["Variable"].map(label)

fig, ax = plt.subplots(figsize=(fs.FULL_WIDTH, 7.0))
y = range(len(b))
for i, r in b.iterrows():
    ax.plot([r["after"], r["before"]], [i, i], color=fs.GREY_MID, lw=0.6, zorder=1)
ax.scatter(b["before"], y, s=17, facecolors=fs.WHITE, edgecolors=fs.ACCENT, linewidths=0.9,
           label="Before weighting", zorder=2, clip_on=False)
ax.scatter(b["after"], y, s=17, color=fs.ACCENT, linewidths=0.9, label="After weighting", zorder=3,
           clip_on=False)
ax.axvline(0.1, color=fs.GREY_DARK, ls=(0, (4, 3)), lw=0.8, zorder=1)
ax.set_yticks(list(y)); ax.set_yticklabels(b["label"], fontsize=7.5)
ax.set_ylim(-0.8, len(b) - 0.2)
ax.set_xlim(0, 0.32)
ax.set_xlabel("Absolute standardized mean difference")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(loc="lower right", frameon=True, facecolor=fs.WHITE, edgecolor="none", framealpha=1.0,
          handletextpad=0.3, borderaxespad=0.6)
fig.tight_layout(pad=0.4)
fs.save(fig, "results/figures/figA1_love_plot.png")
