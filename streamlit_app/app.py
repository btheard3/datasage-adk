# streamlit_app/app.py

import streamlit as st
from agents.planner import execute_agents
from streamlit_app.pdf_export import generate_pdf_report
import plotly.graph_objects as go

st.set_page_config(page_title="DataSage Multi-Agent System", layout="wide")
st.title("🧠 DataSage Multi-Agent System")
st.caption("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# Sidebar filters
st.sidebar.header("📋 Member Profile")
min_age = st.sidebar.slider("Min Age", 18, 100, 30)
max_age = st.sidebar.slider("Max Age", 18, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Specialist", "Emergency"])
region = st.sidebar.selectbox("Region", ["Northeast", "South", "West", "Midwest"])

st.sidebar.header("🧠 Select Agent Tasks")
selected_tasks = st.sidebar.multiselect("Choose which agents to run", [
    "estimate_cost", "interpret_benefits", "detect_anomalies", "generate_insights"
], default=["estimate_cost", "generate_insights"])

if st.sidebar.button("▶️ Run Agents"):
    input_data = {
        "age_min": min_age,
        "age_max": max_age,
        "gender": gender,
        "visit_type": visit_type,
        "region": region
    }

    results = execute_agents(input_data, selected_tasks)

    # --- DISPLAY COST METRICS ---
    if "estimate_cost" in results:
        st.header("🧾 Estimate Cost")
        cost_data = results["estimate_cost"]

        st.subheader("📊 Key Cost Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Cost", f"${cost_data.get('avg_cost', 0):,.2f}")
        col2.metric("Median Cost", f"${cost_data.get('median_cost', 0):,.2f}")
        col3.metric("Min Cost", f"${cost_data.get('min_cost', 0):,.2f}")
        col4.metric("Max Cost", f"${cost_data.get('max_cost', 0):,.2f}")

    st.caption("What these KPIs mean")
    with st.expander("What these KPIs mean"):
        st.markdown("- **Avg Cost**: Mean of all costs\n- **Median**: Midpoint in cost distribution\n- **Min/Max**: Extremes in the data.")


        st.subheader("📈 Cost Distribution")
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=cost_data.get("avg_cost", 0),
            delta={"reference": cost_data.get("median_cost", 0)},
            title={"text": "Average Cost Comparison"},
            gauge={
                "axis": {"range": [None, cost_data.get("max_cost", 5000)]},
                "bar": {"color": "green"},
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    # --- BENEFITS INTERPRETATION ---
    if "interpret_benefits" in results:
        st.header("🩺 Interpret Benefits")
        benefits = results["interpret_benefits"]
        st.info(benefits.get("summary", ""))
        st.info(f"Coverage: {benefits.get('coverage', '')}")
        st.info(f"Copay: {benefits.get('copay', '')}")

    # --- ANOMALY DETECTION ---
    if "detect_anomalies" in results:
        st.header("🚨 Detect Anomalies")
        anomaly = results["detect_anomalies"]
        st.success(anomaly.get("message", "No anomalies detected."))

    # --- INSIGHT SUMMARY ---
    if "generate_insights" in results:
        st.header("🧠 Summary")
        insight = results["generate_insights"]
        st.markdown(insight.get("insight", ""), unsafe_allow_html=True)

    # --- DOWNLOAD REPORT BUTTON ---
    st.header("📄 Export Report")
    pdf_bytes = generate_pdf_report(results)
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="datasage_report.pdf",
        mime="application/pdf"
    )





