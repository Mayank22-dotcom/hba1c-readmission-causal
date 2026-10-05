# Change list: manuscript v7 → v11

No result number changed. No model was refitted and no new estimate was added.

v8: structural and wording changes drafted by Claude as tracked changes (listed below).
v9: the author rewrote all Claude-drafted passages (v6 and v8) and the statements; the
16.0% vs 6.5% diabetes figure was removed; ethics, registration, funding, conflicts and
AI-use statements were completed.
v10: one sentence added to Section 2.2 citing the TARGET guideline and Supplementary File 1
(the completed TARGET checklist); Cashin et al. (2025) added to the references.
v11: visual design only (Direction B: Calibri headings, Cambria body, one navy accent, tinted abstract
panel, restyled tables, running head). Text identical to v10. Figures 2, 4, 6 and A1 redrawn from
the same CSVs with a shared style (scripts/figstyle.py). Checklist page numbers updated.

## Corrections (wording claimed more than the evidence)
- §2.4: the target-trial sentence no longer says eligibility, assignment and follow-up were aligned; it says where alignment fails.
- §3.1: reproducing Strack's crude numbers now "indicates" consistency rather than "shows" that any difference reflects the analysis; notes 69,990 vs 69,984.
- §3.3: "none are distinguishable from zero" replaced (only AIPW has a confidence interval).
- §4.3: landmark analysis sentence made consistent with Figure 1B and the 10 Sep framework paragraphs (discharge landmark is effectively the current design).
- §3.2: admission codes replaced by their labels from IDs_mapping.csv (Emergency Room, Elective, NULL, Not Available).
- §3.2: flagged (not changed) the 16.0% vs 6.5% diabetes figure, which no saved output produces.

## Additions
- Keywords line after the abstract.
- §2.2: what "None" means; pointer to the new Table 1.
- §2.3: handling of unknown codes (own categories; race reference is "?"); pointer to Table A1.
- §2.6: how quintiles and each confidence interval were computed (as in notebook cells 33–39).
- §3.1: 1,528 patients excluded (71,518 − 69,990).
- §4.3: ADA 2025 citation for the data-age limitation; new paragraph on no hospital identifier,
  unrecorded deaths after discharge (competing event), recent outpatient HbA1c, and the five
  code-11 patients with later encounters; eligibility uses discharge information.
- Statements: Ethics, Registration, Funding, Conflicts of Interest, Acknowledgments, Use of AI Tools (template).
- References (3): ADA Professional Practice Committee (2025); Cashin et al. (2025, TARGET); Young et al. (2020).
- Table 1: target trial specification and emulation (replaces the cohort-construction table).
- Figure 2: cohort-flow diagram (scripts/make_fig_cohort_flow.py). Old Figures 2–5 renumbered 3–6.
- Table 5 note: why quintile sizes differ.
- Appendix Table A1: covariate timing table (from covariate_timing_table_v2.csv).
- Appendix Figure A1: Love plot (scripts/make_fig_love_plot.py). Old Figure A1 renumbered A2.

## Flagged for the author to rewrite (drafted by Claude in v6)
BH explanation (§2.6), equation notes, diagnosis-subgroup wording (§2.3, §3.4 ¶2, §4.1 ¶3,
Conclusion, Table 7 note, Figure 6 note), Data and Code Availability.

## Repository
- New: scripts/admission_labels.py, scripts/make_fig_cohort_flow.py, scripts/make_fig_love_plot.py,
  scripts/make_descriptives.py (not run), results/figures/fig2_cohort_flow.png,
  results/figures/figA1_love_plot.png, docs/change_list_v7_to_v8.md.
- README.md: new scripts, run order, outputs table renumbered to v8.
- Notebook: unchanged (new outputs are drawn from saved CSVs instead of rerunning it).
