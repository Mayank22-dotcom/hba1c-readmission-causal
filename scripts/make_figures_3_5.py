"""Draw manuscript Figures 3 and 5 from the notebook's saved output tables.

Run after the notebook, from the repository root:
    python scripts/make_figures_3_5.py

Reads  results/tables/cate_quintiles_oof.csv and results/tables/diagnosis_subgroups_v2.csv
Writes results/figures/fig3_calibration_quintiles.png and results/figures/fig5_diagnosis_forest.png
Plotting only: no estimates are recomputed.
"""
import pandas as pd
import matplotlib.pyplot as plt

TAB, FIG = "results/tables", "results/figures"
BLUE = "#1f4e79"

# Figure 3: mean predicted CATE vs observed DR estimate by out-of-fold quintile
q = pd.read_csv(f"{TAB}/cate_quintiles_oof.csv")
x, y = q["Mean pred CATE"], q["DR (pp)"]
err = [y - q["CI low"], q["CI high"] - y]
fig, ax = plt.subplots(figsize=(5.5, 4.2), dpi=200)
ax.plot([-4.2, 4.2], [-4.2, 4.2], ls="--", lw=1, color="grey", alpha=0.8,
        label="perfect calibration (slope 1)")
ax.axhline(0, color="lightgrey", lw=0.8); ax.axvline(0, color="lightgrey", lw=0.8)
ax.errorbar(x, y, yerr=err, fmt="o", color=BLUE, capsize=3, lw=1.5)
for xi, yi, g in zip(x, y, q["Group"]):
    ax.annotate(g, (xi, yi), xytext=(6, 4), textcoords="offset points", fontsize=9)
ax.set_xlim(-4.2, 4.2); ax.set_ylim(-4.2, 4.2)
ax.set_xlabel("Mean predicted CATE within quintile (pp)")
ax.set_ylabel("Observed doubly robust estimate (pp)")
ax.grid(alpha=0.25); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(f"{FIG}/fig3_calibration_quintiles.png"); plt.close(fig)

# Figure 5: exploratory diagnosis-stratified DR risk differences (forest plot)
s = pd.read_csv(f"{TAB}/diagnosis_subgroups_v2.csv").sort_values("DR (pp)")
labels = [f"{d}  (n={n:,})" for d, n in zip(s["Diagnosis"], s["N"])]
ypos = list(range(len(s)))[::-1]
fig, ax = plt.subplots(figsize=(7, 4), dpi=200)
ax.hlines(ypos, s["CI low"], s["CI high"], color=BLUE, lw=1.8)
ax.plot(s["DR (pp)"], ypos, "o", color=BLUE)
ax.axvline(0, color="grey", lw=1)
ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel("Doubly robust risk difference (percentage points)")
ax.grid(axis="x", alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig5_diagnosis_forest.png"); plt.close(fig)
print("wrote Figures 3 and 5 to", FIG)
