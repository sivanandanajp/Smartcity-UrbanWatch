import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("data/urbanwatch_master_processed.csv")

print("Dataset Shape:", df.shape)

# =====================================
# CLEAN RARE CLASSES
# =====================================

# =====================================
# CLEAN VIOLATION CLASSES
# =====================================

df["Vio Description"] = df["Vio Description"].replace(
    {
        "No Helmet, Triple Riding": "Triple Riding",

        "Violation of Red Light, No Helmet":
            "Multiple Violations",

        "Violation of Red Light, Triple Riding":
            "Multiple Violations",

        "Violation of Red Light, No Helmet, Triple Riding":
            "Multiple Violations"
    }
)

# =====================================
# JUNCTION -> CAMERA MAPPING
# =====================================

junction_cameras = (
    df.groupby("Site Name")["Camera Location"]
      .unique()
      .to_dict()
)


# =====================================
# SELECT FEATURES
# =====================================

X = df[
    [
        "Site Name",
        "Camera Location",
        "hour",
        "weekday_num",
        "month"
    ]
]

y = df["Vio Description"]

# =====================================
# ENCODE CATEGORICAL FEATURES
# =====================================

site_encoder = LabelEncoder()

X = X.copy()

X["Site Name"] = site_encoder.fit_transform(X["Site Name"])
target_encoder = LabelEncoder()

camera_encoder = LabelEncoder()

X["Camera Location"] = camera_encoder.fit_transform(
    X["Camera Location"]
)

y = target_encoder.fit_transform(y)

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# TRAIN MODEL
# =====================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================
# EVALUATE MODEL
# =====================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nAccuracy:")
print(accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

# =====================================
# SAVE MODEL
# =====================================
joblib.dump(model, "models/model.pkl")

joblib.dump(
    site_encoder,
    "models/site_encoder.pkl"
)

joblib.dump(
    target_encoder,
    "models/target_encoder.pkl"
)

joblib.dump(
    camera_encoder,
    "models/camera_encoder.pkl"
)

joblib.dump(
    junction_cameras,
    "models/junction_cameras.pkl"
)

print("\nModel Saved Successfully")
