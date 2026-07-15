import pandas as pd
import glob

files = glob.glob(
    "data/new_junctions/*.xlsx"
)

all_data = []

for file in files:

    print("Reading:", file)

    df = pd.read_excel(
    file,
    header=5
)

    all_data.append(df)

new_data = pd.concat(
    all_data,
    ignore_index=True
)

print(
    "Rows:",
    len(new_data)
)

new_data.to_csv(
    "data/new_junctions_cleaned.csv",
    index=False
)

print(
    "Saved successfully"
)