import pandas as pd

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "../data/urbanwatch_master_processed.csv"
)

# =====================================
# AVAILABLE JUNCTIONS
# =====================================

junctions = sorted(
    df["Site Name"]
    .dropna()
    .unique()
)

print("\nAvailable Junctions:\n")

for i, junction in enumerate(junctions):

    print(
        f"{i+1}. {junction}"
    )

# =====================================
# USER INPUT
# =====================================

choice = int(
    input(
        "\nChoose Junction Number: "
    )
)

junction = junctions[
    choice - 1
]

day = input(
    "\nEnter Day "
    "(Monday-Sunday): "
).strip()

# =====================================
# FILTER DATA
# =====================================

filtered = df[
    (df["Site Name"] == junction)
    &
    (df["weekday"] == day)
]

# =====================================
# CHECK DATA
# =====================================

if len(filtered) == 0:

    print(
        "\nNo records found."
    )

    exit()

# =====================================
# RISK SCORE
# =====================================

junction_day_counts = (
    df.groupby(
        ["Site Name", "weekday"]
    )
    .size()
)

max_count = (
    junction_day_counts.max()
)

current_count = (
    len(filtered)
)

risk_score = round(
    (
        current_count
        /
        max_count
    ) * 100
)

# =====================================
# PEAK HOURS
# =====================================

hour_counts = (
    filtered["hour"]
    .value_counts()
)

peak_hour = (
    hour_counts.idxmax()
)

def format_hour(hour):

    start = pd.Timestamp(
        hour=hour,
        year=2025,
        month=1,
        day=1
    ).strftime(
        "%I %p"
    ).lstrip("0")

    end_hour = (
        hour + 2
    ) % 24

    end = pd.Timestamp(
        hour=end_hour,
        year=2025,
        month=1,
        day=1
    ).strftime(
        "%I %p"
    ).lstrip("0")

    return (
        f"{start} - {end}"
    )

peak_hours = (
    format_hour(
        peak_hour
    )
)

# =====================================
# EXPECTED VIOLATIONS
# =====================================

days_present = (
    filtered["Time"]
    .astype(str)
    .str[:10]
    .nunique()
)

expected_violations = round(
    current_count
    /
    max(days_present, 1)
)

# =====================================
# MOST COMMON VIOLATION
# =====================================

most_common_violation = (
    filtered[
        "Vio Description"
    ]
    .mode()[0]
)

# =====================================
# HIGHEST RISK CAMERA
# =====================================

camera_counts = (
    filtered[
        "Camera Location"
    ]
    .value_counts()
)

highest_risk_camera = (
    camera_counts.idxmax()
)

# =====================================
# DISPLAY RESULTS
# =====================================

print("\n")
print("=" * 35)
print("URBANWATCH RISK REPORT")
print("=" * 35)

print(
    f"\nJunction: {junction}"
)

print(
    f"Day: {day}"
)

print(
    f"\nRisk Score: {risk_score}"
)

print(
    f"\nPeak Hours: {peak_hours}"
)

print(
    f"\nExpected Violations: "
    f"{expected_violations}"
)

print(
    f"\nMost Common Violation:"
)

print(
    most_common_violation
)

print(
    f"\nHighest Risk Camera:"
)

print(
    highest_risk_camera
)

print("\nReport Generated")