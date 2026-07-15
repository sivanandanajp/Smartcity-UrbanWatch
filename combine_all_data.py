import pandas as pd

old_df = pd.read_csv(
    "data/cleaned_data.csv"
)

new_df = pd.read_csv(
    "data/new_junctions_cleaned.csv"
)

combined = pd.concat(
    [old_df, new_df],
    ignore_index=True
)

combined.to_csv(
    "data/urbanwatch_master.csv",
    index=False
)

print(
    "Total rows:",
    len(combined)
)