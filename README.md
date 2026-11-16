# In-hospital HbA1c measurement and 30-day readmission: a causal ML analysis

Mayank Futnani Arupula (mxa6067@psu.edu) · Mentor: Sisi Shao (UCLA)
Student 360 Research Scholar Program, 2026 Summer III · Manuscript submitted 5 October 2026 (v11) · Repository updated 2 November 2026

**[Read the paper (PDF)](docs/Mayank_Futnani_Arupula_manuscript_v11.pdf)** · [Word version](docs/Mayank_Futnani_Arupula_manuscript_v11.docx) · [TARGET reporting checklist](docs/Supplementary_File_1_TARGET_checklist.docx)

**Research question.** Among eligible hospitalized patients with diabetes, how does the estimated
effect of in-hospital HbA1c measurement on 30-day readmission vary across baseline patient
characteristics? Observational data from 1999–2008; this is not a contemporary treatment
recommendation.

> **No raw data in this repository.** See [`data/README.md`](data/README.md) for the official
> download link and instructions.

## Repository layout

```
hba1c_analysis_clean_v5.ipynb   Full analysis (59 cells), runs top to bottom; saved with the outputs of the 2 November run
hba1c_analysis_clean_v4.ipynb   Notebook behind the submitted manuscript (v11), kept unchanged with its September outputs
scripts/figstyle.py             Shared figure style (fonts, colours, sizes) used by the plotting scripts
scripts/make_figures_3_5.py     Draws the predicted-vs-observed and diagnosis forest plots (Figures 4 and 6)
scripts/make_fig_cohort_flow.py Draws the cohort-flow diagram (Figure 2) from the saved tables
scripts/make_fig_love_plot.py   Draws the covariate-balance (Love) plot (Figure A1) from balance_v2.csv
scripts/admission_labels.py     Readable labels for admission codes (checked against IDs_mapping.csv if present)
scripts/make_descriptives.py    Baseline/missing-data tables by arm (NOT YET RUN; needs the raw data)
requirements.txt                Pinned package versions from a verified run (Python 3.12, 2 November 2026)
requirements_lock_full.txt      The same environment including every dependency
data/README.md                  How to obtain diabetic_data.csv (not included)
results/tables/                 Output tables (CSV) behind the submitted manuscript (September run)
results/figures/                Output figures (PNG) behind the submitted manuscript
results/rerun_2026-11-02/       All outputs of the 2 November v5 run (see "Corrections and rerun")
docs/                           Manuscript, design memo, dated amendment, change summary
```

## Run order

1. **Get the data.** Download `diabetic_data.csv` as described in `data/README.md`.
2. **Run the notebook.** Create a Python 3.12 environment with `pip install -r requirements.txt`,
   put `diabetic_data.csv` in the working directory, and run `hba1c_analysis_clean_v5.ipynb` top to
   bottom. It also runs in Google Colab (*Runtime → Run all*), but Colab's preinstalled versions
   may differ from `requirements.txt`, and the estimates shift slightly between package versions
   (see "Corrections and rerun").
   - Fixed seed 20260828. The notebook asserts the cohort (69,990 patients, 12,846 tested,
     6,285 readmitted) before any modelling and stops if these do not match.
   - It installs the pinned `econml` itself (cell 30). Run time is 15–30 minutes, mostly the
     cross-fitted causal forest. The last cell prints the Python and package versions used.
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

As reported in the submitted manuscript (v11). See "Corrections and rerun" below for the two
corrected tests and the 2 November rerun.

| Quantity | Estimate (95% CI) |
|---|---|
| AIPW risk difference (primary) | −0.044 pp (−0.661 to 0.573) |
| AIPW risk, tested / untested | 8.910% / 8.954% |
| Sensitivity S1–S4 | −0.069 / −0.050 / −0.007 / −0.174 pp; all CIs include zero |
| Calibration slope | 0.269 (0.016 to 0.522); classical SE. With HC3 robust SEs the interval includes zero |
| AUTOC | −0.137 pp (−1.067 to 0.793) |
| Q1 − Q5 contrast | −1.880 pp (−3.998 to 0.238) |
| Joint test across diagnosis groups | Wald χ² = 23.32, df = 8, p = .003 (corrected; v11 reported 23.581) |

No clear evidence of a nonzero average effect; the interval is compatible with a small benefit
or a small harm. With robust standard errors the calibration slope does not show a clear
heterogeneity signal, and heterogeneity findings do not support reliable claims about which
patients would benefit. Diagnosis-stratified estimates are exploratory and are not causal effect
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
- `design_memo_amendment_2026-10-03.docx`: first dated amendment (covariate-timing review, removal
  of the diagnosis group, addition of S4), kept unchanged.
- `design_memo_amendment_2026-11-02.docx`: second dated amendment (status of S1–S3, the corrected
  joint test and calibration interval, and the 2 November rerun).
- `change_summary_2026-11-02.docx`: specification, results, and all changes, updated 2 November.
- `change_summary.docx`: the 3 October version, kept unchanged.

## Dependencies

Python 3.12 with the versions pinned in `requirements.txt` (numpy 2.3.5, scipy 1.16.3, pandas 2.2.2,
scikit-learn 1.6.1, statsmodels 0.14.5, matplotlib 3.10.7, econml 0.16.0).
`requirements_lock_full.txt` lists every dependency of that environment. The v5 notebook ran top to
bottom with these versions on 2 November 2026; its last cell prints the versions used.

## Corrections and rerun (2 November 2026)

After submission, the mentor review identified two statistical points. The submitted manuscript
(v11) is unchanged; corrections go into a new dated version.

- **Joint test across diagnosis groups.** v4 centred each group on the overall mean DR score, which
  is not a valid test of equality. v5 uses a joint Wald test of equality (8 contrasts; diagonal
  covariance because the groups contain different patients). From the published Table 7 estimates,
  χ² = 23.32, df = 8, p = .003 (v11: 23.581). Conclusion unchanged.
- **Calibration-slope interval.** v5 uses HC3 robust standard errors, about 15% larger than the
  classical ones. The interval includes zero (rerun: 0.214, −0.070 to 0.498; approximately −0.02 to
  0.56 for the published slope), so the slope no longer supports a heterogeneity signal.
- **Rerun.** `np.trapz` (removed in NumPy 2.4) was replaced and the notebook rerun in the pinned
  environment. The September outputs could not be reproduced exactly, because the package versions
  used in September were not recorded and the model fits shift slightly between releases. In the
  rerun the primary AIPW estimate is −0.082 pp (−0.696 to 0.532) instead of −0.044 pp; all other
  conclusions are unchanged. Outputs are in `results/rerun_2026-11-02/`.
- **Wording.** S1–S3 are no longer described as prespecified (see the second dated amendment).

## Data citation

Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US hospitals for years
1999–2008* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5230J
