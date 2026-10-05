"""Draw the calibration-by-quintile figure and the diagnosis forest plot
(manuscript Figures 4 and 6) from the notebook's saved output tables.

Run after the notebook, from the repository root:
    python scripts/make_figures_3_5.py

Reads  results/tables/cate_quintiles_oof.csv and results/tables/diagnosis_subgroups_v2.csv
Writes results/figures/fig3_calibration_quintiles.png and results/figures/fig5_diagnosis_forest.png
(file names kept from the earlier figure numbering so existing links do not break).
Plotting only: no estimates are recomputed; every plotted value is read from the CSVs.
"""
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import figstyle as fs

fs.apply()
TAB, FIG = "results/tables", "results/figures"

# ---- Manuscript Figure 4: mean predicted CATE vs observed DR estimate, by OOF quintile
q = pd.read_csv(f"{TAB}/cate_quintiles_oof.csv")
assert list(q["Group"]) == ["Q1", "Q2", "Q3", "Q4", "Q5"]
x, y = q["Mean pred CATE"], q["DR (pp)"]
err = [y - q["CI low"], q["CI high"] - y]
fig, ax = plt.subplots(figsize=(fs.MID_WIDTH, 3.7))
lim = 4.2
ax.plot([-lim, lim], [-lim, lim], ls=(0, (4, 3)), lw=0.8, color=fs.GREY_DARK,
        label="perfect calibration (slope 1)", zorder=1)
ax.axhline(0, color=fs.GREY_MID, lw=0.6, zorder=1)
ax.axvline(0, color=fs.GREY_MID, lw=0.6, zorder=1)
ax.errorbar(x, y, yerr=err, fmt="o", color=fs.ACCENT, ecolor=fs.ACCENT, elinewidth=1.2,
            capsize=2.5, capthick=1.0, markersize=5.5, markeredgecolor=fs.WHITE,
            markeredgewidth=0.6, zorder=3)
for xi, yi, g in zip(x, y, q["Group"]):
    ax.annotate(g, (xi, yi), xytext=(7, 4), textcoords="offset points", fontsize=8.5,
                color=fs.INK)
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
ax.set_xticks(range(-4, 5)); ax.set_yticks(range(-4, 5))
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("Mean predicted CATE within quintile (pp)")
ax.set_ylabel("Observed doubly robust estimate (pp)")
ax.legend(loc="upper left", handlelength=2.4, borderaxespad=0.5, frameon=True,
          facecolor=fs.WHITE, edgecolor="none", framealpha=1.0)
fig.tight_layout(pad=0.4)
fs.save(fig, f"{FIG}/fig3_calibration_quintiles.png")

# ---- Manuscript Figure 6: exploratory diagnosis-stratified DR risk differences
s = pd.read_csv(f"{TAB}/diagnosis_subgroups_v2.csv").sort_values("DR (pp)")
assert len(s) == 9
labels = [f"{d}  (n={n:,})" for d, n in zip(s["Diagnosis"], s["N"])]
ypos = list(range(len(s)))[::-1]
fig, ax = plt.subplots(figsize=(fs.FULL_WIDTH, 3.3))
ax.axvline(0, color=fs.GREY_DARK, lw=0.8, zorder=1)
ax.hlines(ypos, s["CI low"], s["CI high"], color=fs.ACCENT, lw=1.4, zorder=2)
ax.plot(s["DR (pp)"], ypos, "o", color=fs.ACCENT, markersize=5.5,
        markeredgecolor=fs.WHITE, markeredgewidth=0.6, zorder=3)
ax.set_yticks(ypos); ax.set_yticklabels(labels)
ax.set_ylim(-0.6, len(s) - 0.4)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Doubly robust risk difference (percentage points)")
fig.tight_layout(pad=0.4)
fs.save(fig, f"{FIG}/fig5_diagnosis_forest.png")
print("font used:", fs.FONT)
