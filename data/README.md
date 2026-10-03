# Data access

The raw data are **not included** in this repository and must not be committed.

Dataset: Diabetes 130-US Hospitals for Years 1999–2008, UCI Machine Learning Repository.
Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). https://doi.org/10.24432/C5230J
License: CC BY 4.0.

1. Go to https://doi.org/10.24432/C5230J and download the dataset archive.
2. Unzip it and take `diabetic_data.csv` (101,766 rows).
3. Place `diabetic_data.csv` in the same working directory as the notebook
   (in Google Colab, upload it to `/content` alongside the notebook).

`.gitignore` excludes `diabetic_data.csv` everywhere in the repository. Check `git status`
before every commit to confirm it is not staged.
