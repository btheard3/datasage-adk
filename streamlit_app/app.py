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

    # --- KPI + GAUGE BLOCK ---
    if "estimate_cost" in results:
        st.markdown("### 💲 Estimate Cost Summary")
        with st.container():
            st.markdown("""
                <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 0 6px rgba(0,0,0,0.05);'>
            """, unsafe_allow_html=True)

            cost = results["estimate_cost"]
            avg = cost.get("avg_cost", 0)
            median = cost.get("median_cost", 0)
            min_val = cost.get("min_cost", 0)
            max_val = cost.get("max_cost", 0)

            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Avg Cost", f"${avg:,.2f}")
            col2.metric("⚖️ Median Cost", f"${median:,.2f}")
            col3.metric("🔻 Min Cost", f"${min_val:,.2f}")

            st.markdown("---")

            st.markdown("#### 📈 Cost Distribution Gauge")
            gauge_max = max(max_val, median + 1000)

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg,
                delta={"reference": median, "increasing": {"color": "red"}, "decreasing": {"color": "green"}},
                gauge={"axis": {"range": [0, gauge_max]}},
                title={'text': "Average vs Median Cost"},
            ))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # --- EXPLANATIONS ---
        with st.expander("📘 What do these numbers mean?"):
            st.markdown("""
            - **Average Cost**: The overall mean amount people paid for the selected care type.
            - **Median Cost**: The midpoint — half paid less, half paid more.
            - **Minimum Cost**: The lowest cost recorded for this demographic group.
            """)

        with st.expander("📘 What does the gauge show?"):
            st.markdown("""
            The gauge compares the average cost to the median for your selected filters.

            - A red delta means the **average is higher**, possibly due to outliers.
            - If delta is low or green, it’s a **stable and consistent** cost distribution.
            - The range shows how this average fits against the **max expected cost** in the dataset.
            """)

    # --- BENEFIT INTERPRETATION ---
    if "interpret_benefits" in results:
        st.markdown("### 🧬 Interpret Benefits")
        b = results["interpret_benefits"]
        st.markdown(f"**Coverage**: {b.get('coverage', '')}")
        st.markdown(f"**Copay**: {b.get('copay', '')}")
        st.markdown(f"**Summary**: {b.get('summary', '')}")

    # --- ANOMALY DETECTION ---
    if "detect_anomalies" in results:
        st.markdown("### ⚠️ Detect Anomalies")
        a = results["detect_anomalies"]
        st.success(a.get("message", "No anomalies detected."))

    # --- INSIGHTS ---
    if "generate_insights" in results:
        st.markdown("### 🧠 Agent Summary")
        st.markdown(results["generate_insights"].get("insight", ""))

    # --- EXPORT TO PDF ---
    st.markdown("### 📄 Export Report")
    pdf_bytes = generate_pdf_report(results)
    st.download_button(
        label="⬇️ Download Report as PDF",
        data=BytesIO(pdf_bytes),
        file_name="datasage_report.pdf",
        mime="application/pdf"
    )








