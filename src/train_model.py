import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

df = pd.read_csv("data/water_sensor_data.csv")
features = ["hour","zone","flow_m3h","pressure_bar","consumption_m3h","night_flow_m3h"]
X, y = df[features], df["leak"]

pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["zone"]),
    ("num", "passthrough", ["hour","flow_m3h","pressure_bar","consumption_m3h","night_flow_m3h"])
])

model = Pipeline([
    ("preprocessor", pre),
    ("classifier", RandomForestClassifier(
        n_estimators=250, random_state=42, class_weight="balanced", min_samples_leaf=2
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(classification_report(y_test, pred))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/leak_model.joblib")
print("Saved models/leak_model.joblib")
