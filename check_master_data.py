import pandas as pd

df = pd.read_csv(
    "data/urbanwatch_master_processed.csv"
)

for junction in sorted(
    df["Site Name"].unique()
):

    cameras = (

        df[
            df["Site Name"]
            == junction
        ]

        ["Camera Location"]

        .dropna()

        .unique()
    )

    print("\n" + junction)

    print(
        "Camera Count:",
        len(cameras)
    )

    print(
        list(cameras)
    )