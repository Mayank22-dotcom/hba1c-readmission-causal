# In-hospital HbA1c measurement and 30-day readmission: a causal ML analysis

Mayank Futnani Arupula (mxa6067@psu.edu) · Mentor: Sisi Shao (UCLA)
Student 360 Research Scholar Program, 2026 Summer III · Final version, 3 October 2026

**Research question.** Among eligible hospitalized patients with diabetes, how does the estimated
effect of in-hospital HbA1c measurement on 30-day readmission vary across baseline patient
characteristics? Observational data from 1999–2008; this is not a contemporary treatment
recommendation.

> **No raw data in this repository.** See [`data/README.md`](data/README.md) for the official
> download link and instructions.

## Repository layout

```
hba1c_analysis_clean_v4.ipynb   Full analysis (57 cells), runs top to bottom
scripts/figstyle.py             Shared figure style (fonts, colours, sizes) used by the plotting scripts
scripts/make_figures_3_5.py     Draws the predicted-vs-observed and diagnosis forest plots (Figures 4 and 6)
scripts/make_fig_cohort_flow.py Draws the cohort-flow diagram (Figure 2) from the saved tables
scripts/make_fig_love_plot.py   Draws the covariate-balance (Love) plot (Figure A1) from balance_v2.csv
scripts/admission_labels.py     Readable labels for admission codes (checked against IDs_mapping.csv if present)
scripts/make_descriptives.py    Baseline/missing-data tables by arm (NOT YET RUN; needs the raw data)
requirements.txt                Python dependencies
data/README.md                  How to obtain diabetic_data.csv (not included)
results/tables/                 Output tables (CSV) written by the notebook
results/figures/                Output figures (PNG)
docs/                           Manuscript, design memo, dated amendment, change summary
```

## Run order

1. **Get the data.** Download `diabetic_data.csv` as described in `data/README.md`.
2. **Run the notebook.** Open `hba1c_analysis_clean_v4.ipynb` in Google Colab, upload
   `diabetic_data.csv` to the working directory, and choose *Runtime → Run all*.
   - Fixed seed 20260828. The notebook asserts the cohort (69,990 patients, 12,846 tested,
     6,285 readmitted) before any modelling and stops if these do not match.
   - It installs `econml` itself (cell 30). Run time is about 15 minutes, mostly the
     cross-fitted causal forest.
   - Outputs are written to the working directory, and the last cell zips them into
     `results.zip` (the raw data are excluded). Download it before the session ends.
3. **File the outputs.** Unzip `results.zip`; put the `.csv` files in `results/tables/` and the
   `.png` files in `results/figures/`.
4. **Draw the figures made by scripts.** From the repository root:
   `python scripts/make_figures_3_5.py`, `python scripts/make_fig_cohort_flow.py`,
   `python scripts/make_fig_love_plot.py`. These only plot the saved tables; they recompute
   nothing. If `IDs_mapping.csv` (from the UCI download) is in the repository root, the Love-plot
   script also checks the admission-code labels against it.
5. **Optional, not yet run (ask Sisi first):** `python scripts/make_descriptives.py` rebuilds only
   the primary cohort (same assertions as the notebook, no models) and writes baseline
   characteristics, missing-data frequencies and primary diagnosis group by arm.

## Final specification

- **Cohort (Order A):** exclude death and hospice discharges (codes 11, 13, 14, 19, 20, 21), then
  take each patient's earliest remaining encounter by `encounter_id`: 69,990 patients.
- **Treatment:** A = 1 if `A1Cresult` is Norm, >7, or >8; A = 0 if None (file read with
  `keep_default_na=False`). **Outcome:** `readmitted == "<30"`.
- **Adjustment set (42 columns):** race, gender, age, admission type, admission source, and
  prior-year inpatient, outpatient, and emergency visits. The primary diagnosis group was removed
  after a covariate-timing review (see the dated amendment in `docs/`) and is retained as S4.
- **Estimation:** cross-fitted AIPW (5-fold GroupKFold by patient), logistic propensity score
  clipped to [0.01, 0.99], gradient boosting outcome models per arm, influence-function CIs.
- **Heterogeneity:** `econml` CausalForestDML (500 trees) in an outer 5-fold loop so every patient
  has an out-of-fold CATE, evaluated against cross-fitted doubly robust scores.

## Headline results

| Quantity | Estimate (95% CI) |
|---|---|
| AIPW risk difference (primary) | −0.044 pp (−0.661 to 0.573) |
| AIPW risk, tested / untested | 8.910% / 8.954% |
| Sensitivity S1–S4 | −0.069 / −0.050 / −0.007 / −0.174 pp; all CIs include zero |
| Calibration slope | 0.269 (0.016 to 0.522) |
| AUTOC | −0.137 pp (−1.067 to 0.793) |
| Q1 − Q5 contrast | −1.880 pp (−3.998 to 0.238) |

No clear evidence of a nonzero average effect; the interval is compatible with a small benefit
or a small harm. Heterogeneity findings do not support reliable claims about which patients
would benefit. Diagnosis-stratified estimates are exploratory and are not causal effect
modification.

## Outputs and where they appear in the manuscript

Manuscript numbering below follows v11 (same numbering as v10) (a new Figure 2 and Table 1 were added after v7).

| File | Contents | Manuscript (v11) |
|---|---|---|
| `cohort_flow_v2.csv` | Cohort construction, Order A vs Order B | Figure 2 and its note |
| `covariate_timing_table_v2.csv` | Timing of each variable, included or excluded | Appendix Table A1 |
| `master_table.csv` | N, events, unadjusted, standardized, and AIPW risks by arm | Table 2, Figure 2 |
| `ate_estimates_v2.csv` | Crude, outcome regression, IPW, AIPW | Table 3 |
| `sensitivity_analyses.csv` | S1–S4 | Table 4 |
| `weight_diagnostics.csv`, `ess_by_arm.csv` | Weights, ESS | §3.2 |
| `balance_v2.csv` | SMDs before and after weighting | §3.2, Appendix Figure A1 |
| `cate_quintiles_oof.csv` | Out-of-fold CATE quintiles | Table 5, Figure 4 |
| `heterogeneity_summary.csv` | Calibration slope, AUTOC, Q1 − Q5 | Table 6 |
| `diagnosis_subgroups_v2.csv` | Exploratory diagnosis-stratified estimates | Table 7, Figure 6 |
| `timeline_v2.png` | Study timeline | Figure 1 |
| `fig2_cohort_flow.png` | Cohort flow (scripts/make_fig_cohort_flow.py) | Figure 2 |
| `ps_overlap_v2.png` | Propensity score overlap | Figure 3 |
| `fig3_calibration_quintiles.png` | Predicted vs observed by quintile | Figure 4 |
| `toc_curve.png` | TOC from 5% (display restriction) | Figure 5 |
| `fig5_diagnosis_forest.png` | Diagnosis forest plot | Figure 6 |
| `figA1_love_plot.png` | Covariate balance (scripts/make_fig_love_plot.py) | Appendix Figure A1 |
| `toc_curve_full.png` | Complete TOC curve | Appendix Figure A2 |

Table 1 (target trial specification and emulation) is text only and has no output file.

## Documents (`docs/`)

- `Mayank_Futnani_Arupula_manuscript_v11.docx`: final manuscript (v10 content with the final visual design).
- `Supplementary_File_1_TARGET_checklist.docx`: completed TARGET reporting checklist (Supplementary File 1).
- `change_list_v7_to_v11.md`: what changed between v7 and v11.
- `design_memo_2026-09-10.docx`: original design memo, kept unchanged as a historical record.
- `design_memo_amendment_2026-10-03.docx`: dated amendment (covariate-timing review, removal of
  the diagnosis group, addition of S4).
- `change_summary.docx`: final specification, results, and changes since 11 September.

## Dependencies

Python 3 with the packages in `requirements.txt`. The analysis was run in Google Colab. To record
exact versions, run this in the same Colab session after the notebook and paste the output into
`requirements.txt` as `package==version` lines:

```python
import sys, numpy, pandas, scipy, matplotlib, sklearn, statsmodels, econml
print(sys.version)
for m in (numpy, pandas, scipy, matplotlib, sklearn, statsmodels, econml):
    print(m.__name__, m.__version__)
```

## Data citation

Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US hospitals for years
1999–2008* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5230J
