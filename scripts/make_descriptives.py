"""Descriptive tables by treatment arm (baseline characteristics, missing data,
primary diagnosis group, encounter-level exclusions).

NOT YET RUN. Needs diabetic_data.csv (and optionally IDs_mapping.csv) in the
repository root. Ask Sisi before running and before adding its outputs to the paper.

It rebuilds ONLY the primary cohort, using the same steps and assertions as the
notebook (cells 1-8). It fits no models and changes no estimate.

Outputs (results/tables/):
  baseline_by_arm.csv         n (%) of every covariate level, and mean (SD) of the
                              prior-year visit counts, by arm   -> TARGET item 9
  missing_by_arm.csv          frequency of unknown/missing codes, by arm -> item 11
  diag_group_by_arm.csv       primary diagnosis group by arm (source for the
                              16.0% vs 6.5% diabetes figure in Section 3.2)
  cohort_flow_encounters.csv  encounter-level counts for the flow diagram

Run from the repository root:  python scripts/make_descriptives.py
"""
import os, sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from admission_labels import ADMISSION_TYPE, ADMISSION_SOURCE, MISSING_TYPE, MISSING_SOURCE

CHECK = os.environ.get("SKIP_COHORT_ASSERTS") != "1"   # only for testing on fake data
TESTED = ["Norm", ">7", ">8"]
BAD = [11, 13, 14, 19, 20, 21]          # expired / hospice discharge codes
OUT = "results/tables/"

df = pd.read_csv("diabetic_data.csv", keep_default_na=False)

# same dxgroup rule as notebook cell 6
def dxgroup(c):
    if c in ("?", "", None): return "Missing"
    s = str(c)
    if s.startswith("V") or s.startswith("E"): return "Other"
    try: v = float(s)
    except ValueError: return "Other"
    if 390 <= v <= 459 or v == 785: return "Circulatory"
    if 460 <= v <= 519 or v == 786: return "Respiratory"
    if 520 <= v <= 579 or v == 787: return "Digestive"
    if int(v) == 250: return "Diabetes"
    if 800 <= v <= 999: return "Injury"
    if 710 <= v <= 739: return "Musculoskeletal"
    if 580 <= v <= 629 or v == 788: return "Genitourinary"
    if 140 <= v <= 239: return "Neoplasms"
    return "Other"

srt = df.sort_values("encounter_id")
kept_enc = srt.loc[~srt["discharge_disposition_id"].isin(BAD)]
d = kept_enc.drop_duplicates("patient_nbr", keep="first").reset_index(drop=True)
d["A"] = d["A1Cresult"].isin(TESTED).astype(int)
d["Y"] = (d["readmitted"] == "<30").astype(int)
d["diag_group"] = d["diag_1"].apply(dxgroup)
if CHECK:
    assert len(d) == 69990 and d["A"].sum() == 12846 and d["Y"].sum() == 6285

arm = {1: "Tested", 0: "Untested"}

# --- encounter-level flow
pd.DataFrame([
    ["Raw encounters", len(df)],
    ["Encounters ending in death or hospice discharge (excluded)", len(df) - len(kept_enc)],
    ["Remaining encounters", len(kept_enc)],
    ["Patients with no remaining encounter (excluded)", df["patient_nbr"].nunique() - len(d)],
    ["Primary cohort (earliest remaining encounter per patient)", len(d)],
], columns=["Step", "N"]).to_csv(OUT + "cohort_flow_encounters.csv", index=False)

# --- baseline characteristics by arm
d["admission_type"] = d["admission_type_id"].astype(int).map(ADMISSION_TYPE).fillna("Other code")
d["admission_source"] = d["admission_source_id"].astype(int).map(ADMISSION_SOURCE).fillna("Other code")
rows = []
for var in ["age", "gender", "race", "admission_type", "admission_source"]:
    for lev in sorted(d[var].astype(str).unique()):
        r = [var, lev]
        for a in (1, 0):
            g = d[d["A"] == a]
            k = int((g[var].astype(str) == lev).sum())
            r += [k, round(100 * k / len(g), 1)]
        rows.append(r)
for var in ["number_inpatient", "number_outpatient", "number_emergency"]:
    r = [var, "mean (SD)"]
    for a in (1, 0):
        g = d.loc[d["A"] == a, var].astype(float)
        r += [round(g.mean(), 2), round(g.std(), 2)]
    rows.append(r)
pd.DataFrame(rows, dtype=object, columns=["Variable", "Level",
                            "Tested n / mean", "Tested % / SD",
                            "Untested n / mean", "Untested % / SD"]
             ).to_csv(OUT + "baseline_by_arm.csv", index=False)

# --- missing / unknown codes by arm
miss = {
    "race recorded as '?'": d["race"] == "?",
    "gender Unknown/Invalid": d["gender"] == "Unknown/Invalid",
    "admission type Not Available/NULL/Not Mapped": d["admission_type_id"].astype(int).isin(MISSING_TYPE),
    "admission source Not Available/NULL/Not Mapped/Unknown": d["admission_source_id"].astype(int).isin(MISSING_SOURCE),
    "primary diagnosis (diag_1) missing": d["diag_1"].isin(["?", ""]),
    "medical_specialty '?' (not used)": d["medical_specialty"] == "?",
}
rows = []
for name, m in miss.items():
    r = [name]
    for a in (1, 0):
        g = m[d["A"] == a]
        r += [int(g.sum()), round(100 * g.mean(), 1)]
    r += [int(m.sum()), round(100 * m.mean(), 1)]
    rows.append(r)
pd.DataFrame(rows, columns=["Item", "Tested n", "Tested %", "Untested n", "Untested %",
                            "All n", "All %"]).to_csv(OUT + "missing_by_arm.csv", index=False)

# --- primary diagnosis group by arm
tab = pd.crosstab(d["diag_group"], d["A"]).rename(columns=arm)
for a in arm.values():
    tab[a + " %"] = (100 * tab[a] / tab[a].sum()).round(1)
tab.reset_index().to_csv(OUT + "diag_group_by_arm.csv", index=False)

print("wrote baseline_by_arm.csv, missing_by_arm.csv, diag_group_by_arm.csv, cohort_flow_encounters.csv")
