import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.predict import add_predictions

st.set_page_config(page_title="AquaGuard AI", page_icon="💧", layout="wide")
st.title("💧 AquaGuard AI")
st.caption("Water-loss detection, leak localisation and repair prioritisation — prototype using simulated sensor data.")

data = pd.read_csv("data/water_sensor_data.csv").tail(240)
pred = add_predictions(data)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Readings analysed", len(pred))
c2.metric("High/Critical alerts", int(pred["severity"].isin(["High","Critical"]).sum()))
c3.metric("Highest leak probability", f"{pred['leak_probability'].max():.1%}")
c4.metric("Potential loss (sample)", f"{pred['estimated_water_loss_m3h'].sum():.1f} m³/h")

st.subheader("🚨 Highest-priority repairs")
top = pred.sort_values("repair_priority").head(10)[
    ["repair_priority","zone","leak_probability","severity","estimated_water_loss_m3h"]
]
st.dataframe(top, use_container_width=True)

st.subheader("Leak probability by zone")
zone = pred.groupby("zone", as_index=False).agg(
    leak_probability=("leak_probability","mean"),
    estimated_water_loss_m3h=("estimated_water_loss_m3h","sum")
)
st.plotly_chart(px.bar(zone, x="zone", y="leak_probability",
                       hover_data=["estimated_water_loss_m3h"]), use_container_width=True)

st.subheader("Pressure and flow monitoring")
st.plotly_chart(px.scatter(pred, x="pressure_bar", y="flow_m3h",
                           color="severity", hover_data=["zone","leak_probability"]),
                use_container_width=True)

st.info("Responsible-use notice: This dashboard is a hackathon prototype using simulated data. Field validation and human utility-operator review are required before deployment.")
