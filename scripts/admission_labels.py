"""Readable labels for the one-hot covariate columns used in the analysis.

The admission code descriptions are transcribed from IDs_mapping.csv, which is
distributed with the UCI dataset (https://doi.org/10.24432/C5230J). If that file is
present, `check_against_mapping()` confirms every transcribed label matches it.

Plotting/labelling only: nothing here changes any estimate.
"""
import csv
import os

ADMISSION_TYPE = {
    1: "Emergency", 2: "Urgent", 3: "Elective", 4: "Newborn",
    5: "Not Available", 6: "NULL", 7: "Trauma Center", 8: "Not Mapped",
}

ADMISSION_SOURCE = {
    1: "Physician Referral", 2: "Clinic Referral", 3: "HMO Referral",
    4: "Transfer from a hospital", 5: "Transfer from a SNF",
    6: "Transfer from another health care facility", 7: "Emergency Room",
    8: "Court/Law Enforcement", 9: "Not Available",
    10: "Transfer from critical access hospital", 11: "Normal Delivery",
    13: "Sick Baby", 14: "Extramural Birth", 17: "NULL", 20: "Not Mapped",
    22: "Transfer from hospital inpatient/same facility",
    25: "Transfer from Ambulatory Surgery Center",
}

# Where the display label above shortens or corrects the wording in IDs_mapping.csv,
# this is the exact text in the file (used only by check_against_mapping).
SOURCE_TEXT_IN_FILE = {
    5: "Transfer from a Skilled Nursing Facility (SNF)",
    10: "Transfer from critial access hospital",   # spelling as in the source file
    22: "Transfer from hospital inpt/same fac reslt in a sep claim",
}

# Codes that record missing or unknown information rather than a real category.
MISSING_TYPE = {5, 6, 8}
MISSING_SOURCE = {9, 15, 17, 20, 21}


def label(col: str) -> str:
    """Turn a get_dummies column name into a readable label."""
    if col.startswith("admission_type_id_"):
        code = int(col.rsplit("_", 1)[1])
        return f"Admission type: {ADMISSION_TYPE[code]}"
    if col.startswith("admission_source_id_"):
        code = int(col.rsplit("_", 1)[1])
        return f"Admission source: {ADMISSION_SOURCE[code]}"
    if col.startswith("race_"):
        return "Race: " + {"AfricanAmerican": "African American"}.get(col[5:], col[5:])
    if col.startswith("gender_"):
        return f"Gender: {col[7:]}"
    if col.startswith("age_"):
        return f"Age {col[4:]}"
    return {
        "number_inpatient": "Prior-year inpatient visits",
        "number_outpatient": "Prior-year outpatient visits",
        "number_emergency": "Prior-year emergency visits",
    }.get(col, col)


def check_against_mapping(path: str = "IDs_mapping.csv") -> bool:
    """Assert the transcribed labels match the UCI mapping file, if it is present."""
    if not os.path.exists(path):
        print(f"{path} not found; labels not checked against the source file.")
        return False
    section, found = None, {"admission_type_id": {}, "admission_source_id": {}}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                section = None
                continue
            if not row[0].strip().isdigit():
                section = row[0].strip()
                continue
            if section in found:
                found[section][int(row[0])] = row[1].strip()
    for code, text in ADMISSION_TYPE.items():
        assert found["admission_type_id"][code].lower() == text.lower(), (code, text)
    for code, text in ADMISSION_SOURCE.items():
        src = found["admission_source_id"][code]
        assert src.lower() == SOURCE_TEXT_IN_FILE.get(code, text).lower(), (code, src, text)
    print("Labels match", path)
    return True


if __name__ == "__main__":
    check_against_mapping()
