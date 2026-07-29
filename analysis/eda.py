import pandas as pd
import matplotlib.pyplot as plt

# ============================
# LOAD DATASET
# ============================

df = pd.read_csv("data\cleaned_data.csv")

print("\n==========================")
print("DATASET INFO")
print("==========================")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

# ============================
# JUNCTION ANALYSIS
# ============================

print("\n==========================")
print("JUNCTION COUNTS")
print("==========================")

junction_counts = df["Site Name"].value_counts()

print(junction_counts)

plt.figure(figsize=(10, 5))
junction_counts.plot(kind="bar")
plt.title("Violations by Junction")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================
# VIOLATION ANALYSIS
# ============================

print("\n==========================")
print("VIOLATION COUNTS")
print("==========================")

violation_counts = df["Vio Description"].value_counts()

print(violation_counts)

plt.figure(figsize=(10, 5))
violation_counts.plot(kind="bar")
plt.title("Violation Distribution")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================
# HOUR ANALYSIS
# ============================

print("\n==========================")
print("HOUR DISTRIBUTION")
print("==========================")

hour_counts = df["hour"].value_counts().sort_index()

print(hour_counts)

plt.figure(figsize=(10, 5))
hour_counts.plot(kind="bar")
plt.title("Violations by Hour")
plt.xlabel("Hour")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================
# WEEKDAY ANALYSIS
# ============================

print("\n==========================")
print("WEEKDAY DISTRIBUTION")
print("==========================")

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_counts = (
    df["weekday"]
    .value_counts()
    .reindex(weekday_order)
)

print(weekday_counts)

plt.figure(figsize=(10, 5))
weekday_counts.plot(kind="bar")
plt.title("Violations by Weekday")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================
# MONTH ANALYSIS
# ============================

print("\n==========================")
print("MONTH DISTRIBUTION")
print("==========================")

month_counts = df["month_name"].value_counts()

print(month_counts)

plt.figure(figsize=(10, 5))
month_counts.plot(kind="bar")
plt.title("Violations by Month")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================
# JUNCTION VS VIOLATION
# ============================

print("\n==========================")
print("JUNCTION VS VIOLATION")
print("==========================")

cross_tab = pd.crosstab(
    df["Site Name"],
    df["Vio Description"]
)

print(cross_tab)

cross_tab.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6)
)

plt.title("Violation Types by Junction")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

print("\nEDA COMPLETED SUCCESSFULLY")