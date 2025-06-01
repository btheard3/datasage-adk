import streamlit as st
import os
import json
from agents.cost_estimator.agent import run_cost_estimator
from agents.benefits_interpreter.agent import run_benefits_interpreter
from agents.anomaly_detector.agent import run_anomaly_detector
from agents.insight_generator.agent import run_insight_generator
from streamlit_app.pdf_export import generate_pdf_report
import plotly.graph_objects as go

st.set_page_config(page_title="DataSage", layout="wide")
st.title("💊 DataSage — Healthcare Cost Intelligence")
st.markdown("Use the filters below to run the agents and generate insights.")
st.divider()

# ---- Filters ----
with st.sidebar:
    st.header("🔧 Input Filters")
    age_min = st.slider("Minimum Age", 0, 100, 25)
    age_max = st.slider("Maximum Age", 0, 100, 40)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])
    visit_type = st.selectbox("Visit Type", ["emergency", "routine", "preventive", "urgent care"])

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "state": region,
    "visit_type": visit_type
}

if st.button("🔍 Run Agents"):
    st.subheader("📊 Cost Estimator Output")
    result = run_cost_estimator(inputs)
    st.session_state["results"] = result
    avg_cost = result["avg_cost"]
    median_cost = result["median_cost"]
    min_cost = result["min_cost"]
    max_cost = result["max_cost"]

    st.markdown(f"""
    - **Average Cost**: `${avg_cost:,.2f}`
    - **Median Cost**: `${median_cost:,.2f}`
    - **Minimum Cost**: `${min_cost:,.2f}`
    - **Maximum Cost**: `${max_cost:,.2f}`
    """)

    # Gauge chart
    delta_value = avg_cost - median_cost
    delta_color = "green" if delta_value >= 0 else "red"
    st.subheader("📈 Average Cost Gauge")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_cost,
        delta={'reference': median_cost, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        title={'text': "Average Cost ($)"},
        gauge={
            'axis': {'range': [None, max_cost]},
            'bar': {'color': "darkgreen"},
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.info("ℹ️ **What this means**: This gauge shows the average healthcare cost compared to the median. Green indicates above-median spending (possibly overutilization), red indicates below-median (possibly underutilization or cost control).")

    # Run other agents
    kpis = {
        "avg_cost": avg_cost,
        "median_cost": median_cost,
        "min_cost": min_cost,
        "max_cost": max_cost,
    }

    benefits = run_benefits_interpreter(kpis)
    anomaly = run_anomaly_detector(kpis)
    insights = run_insight_generator(kpis)

    st.subheader("🧠 Benefit Summary")
    st.markdown(benefits.get("benefit_summary", "No summary available."))
    st.info("ℹ️ **What this means**: This AI-powered summary interprets the cost KPIs to highlight potential healthcare benefit scenarios like full coverage or lack of utilization.")

    st.subheader("🚨 Anomaly Detection")
    st.markdown(anomaly.get("explanation", "No anomalies detected."))
    st.info("ℹ️ **What this means**: Flags data quality issues or unusual cost patterns such as zero values, spikes, or missing records.")

    st.subheader("🔎 AI Cost Insights")
    st.markdown(insights.get("insights", "No insights generated."))
    st.info("ℹ️ **What this means**: This section provides a contextual business recommendation using OpenAI to improve cost efficiency or highlight non-obvious trends.")

    st.download_button("📥 Export PDF Report", generate_pdf_report({
        "Cost Estimator": result,
        "Benefit Summary": benefits.get("benefit_summary"),
        "Anomalies": anomaly.get("explanation"),
        "Insights": insights.get("insights")
    }), file_name="datasage_report.pdf", mime="application/pdf")














