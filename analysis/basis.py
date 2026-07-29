import pandas as pd

# ===========================
# LOAD DATASET
# ===========================

df = pd.read_csv("../data/cleaned_data.csv")

# ===========================
# DATASET INFORMATION
# ===========================

print("\n==========================")
print("DATASET INFORMATION")
print("==========================")

print("Rows :", len(df))
print("Columns :", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

# ===========================
# JUNCTION COUNTS
# ===========================

print("\n==========================")
print("JUNCTION COUNTS")
print("==========================")

print(df["Site Name"].value_counts())

# ===========================
# VIOLATION COUNTS
# ===========================

print("\n==========================")
print("VIOLATION COUNTS")
print("==========================")

print(df["Vio Description"].value_counts())

# ===========================
# HOUR DISTRIBUTION
# ===========================

print("\n==========================")
print("HOUR DISTRIBUTION")
print("==========================")

hour_counts = df["hour"].value_counts().sort_index()

for hour, count in hour_counts.items():
    print(f"{hour}:00 - {hour}:59 --> {count}")

# ===========================
# WEEKDAY DISTRIBUTION
# ===========================

print("\n==========================")
print("WEEKDAY DISTRIBUTION")
print("==========================")

print(df["weekday"].value_counts())

# ===========================
# MONTH DISTRIBUTION
# ===========================

print("\n==========================")
print("MONTH DISTRIBUTION")
print("==========================")

print(df["month_name"].value_counts())

# ===========================
# CAMERA LOCATION COUNTS
# ===========================

print("\n==========================")
print("TOP CAMERA LOCATIONS")
print("==========================")

print(df["Camera Location"].value_counts().head(20))

# ===========================
# DATE RANGE
# ===========================

print("\n==========================")
print("DATE RANGE")
print("==========================")

df["Time"] = pd.to_datetime(df["Time"])

print("Start :", df["Time"].min())
print("End   :", df["Time"].max())

# ===========================
# MISSING VALUES
# ===========================

print("\n==========================")
print("MISSING VALUES")
print("==========================")

print(df.isnull().sum())

print("\nAnalysis Completed Successfully")