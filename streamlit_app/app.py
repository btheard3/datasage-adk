import os
import math
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
st.sidebar.header("🛠️ Configure Inputs")
age_min = st.sidebar.slider("Minimum Age", 0, 100, 30)
age_max = st.sidebar.slider("Maximum Age", age_min + 1, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
region = st.sidebar.selectbox("Region", ["Northeast", "Midwest", "South", "West"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Mental Health", "Emergency", "Specialist"])

selected_tasks = st.sidebar.multiselect(
    "🧩 Select Agents to Run",
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

    # --- ESTIMATED COST METRICS ---
    if "estimate_cost" in results:
        st.subheader("💲 Estimate Cost Summary")
        cost = results["estimate_cost"]

        avg = cost.get("avg_cost")
        median = cost.get("median_cost")
        min_cost = cost.get("min_cost")
        max_cost = cost.get("max_cost")

        if any(x is None or (isinstance(x, float) and math.isnan(x)) for x in [avg, median, min_cost]):
            st.warning("🚫 No cost data available for this filter combination. Try adjusting the age range, region, or visit type.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Avg Cost", f"${avg:,.2f}")
            col2.metric("📘 Median Cost", f"${median:,.2f}")
            col3.metric("📉 Min Cost", f"${min_cost:,.2f}")

            with st.expander("ℹ️ What do these numbers mean?"):
                st.markdown("""
                - **Average Cost**: The mean amount paid by users for this service type.
                - **Median Cost**: The midpoint — half paid more, half paid less. Less sensitive to outliers.
                - **Min Cost**: The lowest recorded cost for the selected criteria.
                """)

            # --- GAUGE ---
            st.subheader("📈 Cost Distribution Gauge")
            max_val = max(max_cost or 0, median + 1000)

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg,
                delta={"reference": median, "increasing": {"color": "red"}},
                gauge={"axis": {"range": [0, max_val]}},
                title={'text': "Average vs Median Cost"}
            ))

            st.plotly_chart(fig, use_container_width=True)

            with st.expander("ℹ️ What does the gauge show?"):
                st.markdown("""
                This gauge shows how the **average cost** compares to the **median**:
                - The needle shows the **average cost** for your filters.
                - The delta below it tells how far off it is from the **typical (median)** cost.
                - A **big red delta**? The average is likely skewed by outliers.
                - A small delta? That’s a stable and predictable price range.
                """)

    # --- DISPLAY BENEFITS ---
    if "interpret_benefits" in results:
        st.subheader("🧬 Interpret Benefits")
        b = results["interpret_benefits"]
        st.markdown(f"**Coverage**: {b.get('coverage', '')}")
        st.markdown(f"**Copay**: {b.get('copay', '')}")
        st.markdown(f"**Summary**: {b.get('summary', '')}")

    # --- DISPLAY ANOMALIES ---
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








