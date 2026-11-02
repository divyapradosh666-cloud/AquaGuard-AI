import pandas as pd
import joblib

FEATURES = ["hour","zone","flow_m3h","pressure_bar","consumption_m3h","night_flow_m3h"]

def add_predictions(df):
    model = joblib.load("models/leak_model.joblib")
    out = df.copy()
    out["leak_probability"] = model.predict_proba(out[FEATURES])[:, 1]
    out["estimated_water_loss_m3h"] = (
        (out["flow_m3h"] - out["consumption_m3h"]).clip(lower=0) *
        out["leak_probability"]
    ).round(2)

    out["severity"] = pd.cut(
        out["leak_probability"],
        bins=[-0.01, 0.35, 0.65, 0.85, 1.0],
        labels=["Low", "Medium", "High", "Critical"]
    ).astype(str)

    # Priority combines probability and estimated water loss.
    out["priority_score"] = (
        0.65 * out["leak_probability"] +
        0.35 * (out["estimated_water_loss_m3h"] /
                max(out["estimated_water_loss_m3h"].max(), 1))
    )
    out["repair_priority"] = out["priority_score"].rank(
        ascending=False, method="dense"
    ).astype(int)
    return out

if __name__ == "__main__":
    df = pd.read_csv("data/water_sensor_data.csv").tail(120)
    result = add_predictions(df)
    result.sort_values("repair_priority").to_csv("data/predictions.csv", index=False)
    print("Created data/predictions.csv")
