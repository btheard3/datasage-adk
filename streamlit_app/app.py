import streamlit as st
import os
import json
from agents.cost_estimator.agent import run_cost_estimator
from agents.benefits_interpreter.agent import run_benefits_interpreter
from agents.anomaly_detector.agent import run_anomaly_detector
from agents.insight_generator.agent import run_insight_generator
import plotly.graph_objects as go

st.set_page_config(page_title="DataSage", layout="wide")

st.title("💊 DataSage — Healthcare Cost Intelligence")
st.markdown("Use the filters below to run the agents and generate insights.")
st.divider()

# ---- Filters ----
with st.sidebar:
    st.header("🎚️ Input Filters")
    age_min = st.slider("Minimum Age", 0, 100, 25)
    age_max = st.slider("Maximum Age", 0, 100, 60)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    region = st.selectbox("Region", ["northeast", "southeast", "southwest", "northwest"])
    visit_type = st.selectbox("Visit Type", ["emergency", "routine", "urgent", "preventive"])

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "state": region,
    "visit_type": visit_type
}

if st.button("Run Agents 🧠"):
    with st.spinner("Running multi-agent system..."):
        # Run all agents
        estimate = run_cost_estimator(inputs)
        avg = estimate.get("avg_cost", 0)
        median = estimate.get("median_cost", 0)
        min_cost = estimate.get("min_cost", 0)
        max_cost = estimate.get("max_cost", 0)

        # Edge case guard
        if all(v == 0 for v in [avg, median, min_cost, max_cost]):
            st.warning("⚠️ No valid cost data returned. Please adjust your filters.")
            st.stop()

        # Compute delta
        if median != 0:
            delta = round(((avg - median) / median) * 100, 2)
            delta_symbol = "▲" if delta > 0 else "▼" if delta < 0 else ""
            delta_color = "green" if delta >= 0 else "red"
            delta_text = f"{delta_symbol} {abs(delta)}%"
        else:
            delta_text = "N/A"
            delta_color = "gray"

        # Display Raw Output
        st.subheader("📊 Cost Estimator Raw Output")
        st.json(estimate)

        # Gauge Chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg,
            delta={"reference": median if median > 0 else None,
                   "increasing": {"color": "green"},
                   "decreasing": {"color": "red"}},
            title={"text": "Average Cost Gauge"},
            gauge={
                "axis": {"range": [0, max_cost if max_cost > 0 else 5000]},
                "bar": {"color": "darkgreen"},
                "steps": [
                    {"range": [0, median], "color": "lightgray"},
                    {"range": [median, max_cost], "color": "lightgreen"},
                ]
            }
        ))

        st.subheader("📈 Average Cost Distribution")
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown(f"💡 **What this means:** The average healthcare cost is **${avg:,.2f}**, compared to a median of **${median:,.2f}**. The delta is **{delta_text}**, indicating if costs are above or below typical levels.")

        # Run other agents
        benefits = run_benefits_interpreter(estimate)
        anomalies = run_anomaly_detector(estimate)
        insights = run_insight_generator(estimate)

        # Display Results
        st.subheader("💡 Benefits Summary")
        st.write(benefits.get("benefit_summary", "No summary."))

        st.subheader("🚨 Anomaly Detection")
        st.write(anomalies.get("explanation", "No anomalies detected."))

        st.subheader("📌 AI-Powered Insights")
        st.write(insights.get("insights", "No insights found."))

        # Optional PDF Export (currently disabled)
        # st.download_button("📄 Export PDF Report", generate_pdf_report({...}), ...)
















