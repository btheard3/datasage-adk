import os
import streamlit as st
from io import BytesIO
from agents.planner import execute_agents
from streamlit_app.pdf_export import generate_pdf_report
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="DataSage Multi-Agent System", layout="wide")
st.title("🧠 DataSage Multi-Agent System")
st.caption("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Configure Inputs")
age_min = st.sidebar.slider("Minimum Age", 0, 100, 30)
age_max = st.sidebar.slider("Maximum Age", age_min + 1, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
region = st.sidebar.selectbox("Region", ["Northeast", "Midwest", "South", "West"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Mental Health", "Emergency", "Specialist"])

selected_tasks = st.sidebar.multiselect(
    "Select Agents to Run",
    ["estimate_cost", "interpret_benefits", "detect_anomalies", "generate_insights"],
    default=["estimate_cost", "generate_insights"]
)

# --- AGENT EXECUTION ---
input_data = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "visit_type": visit_type,
    "region": region
}

if st.sidebar.button("▶️ Run Agents"):
    results = execute_agents(input_data, selected_tasks)

    # --- DISPLAY ESTIMATED COST ---
    if "estimate_cost" in results:
        st.header("📊 Estimate Cost")
        cost = results["estimate_cost"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Cost", f"${cost.get('avg_cost', 0):,.2f}")
        col2.metric("Median Cost", f"${cost.get('median_cost', 0):,.2f}")
        col3.metric("Min Cost", f"${cost.get('min_cost', 0):,.2f}")

        with st.expander("ℹ️ What these KPIs mean"):
            st.markdown("""
            - **Avg Cost**: Average healthcare cost across the sample population.
            - **Median Cost**: Midpoint cost — half the costs are lower, half are higher.
            - **Min Cost**: Lowest observed cost in the dataset.
            """)

        # --- COST DISTRIBUTION GAUGE ---
        st.subheader("📈 Cost Distribution Gauge")
        avg = cost.get("avg_cost", 0)
        median = cost.get("median_cost", 0)
        max_val = max(cost.get("max_cost", 0), median + 1000)

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg,
            delta={"reference": median, "increasing": {"color": "red"}},
            gauge={"axis": {"range": [0, max_val]}},
            title={'text': "Average Cost Comparison"}
        ))

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("ℹ️ What the cost gauge shows"):
            st.markdown("""
            This gauge visualizes how the average cost compares to the median cost:
            - **Needle value**: Current average cost
            - **Delta**: Difference from the median
            - **Gauge range**: Scaled from 0 to just above the maximum observed cost
            """)

    # --- DISPLAY BENEFIT INTERPRETATION ---
    if "interpret_benefits" in results:
        st.subheader("🧬 Interpret Benefits")
        b = results["interpret_benefits"]
        st.markdown(f"**Coverage**: {b.get('coverage', '')}")
        st.markdown(f"**Copay**: {b.get('copay', '')}")
        st.markdown(f"**Summary**: {b.get('summary', '')}")

    # --- DISPLAY ANOMALY DETECTION ---
    if "detect_anomalies" in results:
        st.subheader("⚠️ Detect Anomalies")
        a = results["detect_anomalies"]
        st.success(a.get("message", "No anomalies detected."))

    # --- DISPLAY INSIGHTS ---
    if "generate_insights" in results:
        st.subheader("🧠 Insights")
        st.markdown(results["generate_insights"].get("insight", ""))

    # --- EXPORT TO PDF ---
    st.subheader("📄 Export Report")
    pdf_bytes = generate_pdf_report(results)
    st.download_button(
        label="⬇️ Download Report as PDF",
        data=BytesIO(pdf_bytes),
        file_name="datasage_report.pdf",
        mime="application/pdf"
    )









