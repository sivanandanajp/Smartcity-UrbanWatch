import pandas as pd

df = pd.read_csv(
    "data/urbanwatch_master_processed.csv"
)

for junction in sorted(
    df["Site Name"].dropna().unique()
):
    print(junction)