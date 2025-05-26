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
    "🤖 Select Agents to Run",
    ["estimate_cost", "interpret_benefits", "detect_anomalies", "generate_insights"],
    default=["estimate_cost", "generate_insights"]
)

# --- INPUT DATA PACKAGE ---
input_data = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "visit_type": visit_type,
    "region": region
}

# Track if PDF exported
pdf_exported = False

# --- RUN AGENTS ---
if st.sidebar.button("▶️ Run Agents"):
    results = execute_agents(input_data, selected_tasks)

    # --- ESTIMATED COST ---
    if "estimate_cost" in results:
        st.header("💲 Estimate Cost Summary")
        cost = results["estimate_cost"]

        avg = cost.get("avg_cost", None)
        median = cost.get("median_cost", None)
        min_cost = cost.get("min_cost", None)
        max_cost = cost.get("max_cost", 0)

        if all(val is not None and val > 0 for val in [avg, median, min_cost]):
            # KPI metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Avg Cost", f"${avg:,.2f}")
            col2.metric("📏 Median Cost", f"${median:,.2f}")
            col3.metric("🔻 Min Cost", f"${min_cost:,.2f}")

            # --- GAUGE ---
            st.subheader("📈 Cost Distribution Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg,
                delta={"reference": median, "increasing": {"color": "red"}},
                gauge={"axis": {"range": [0, max(max_cost, median + 1000)]}},
                title={"text": "Average vs Median Cost"}
            ))
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ No cost data available for this filter combination. Try adjusting age, region, or visit type.")

        with st.expander("❓ What do these numbers mean?"):
            st.markdown("""
            - **Average Cost**: The overall mean cost across patients matching your criteria.
            - **Median Cost**: The midpoint — half of people paid less, half paid more.
            - **Min Cost**: The least expensive visit in the dataset for this group.
            """)

        with st.expander("📊 What does the gauge show?"):
            st.markdown("""
            The gauge compares **average** to **median** costs:
            - Red delta = higher-than-typical costs.
            - Close to zero = stable cost structure.
            - Use it to spot anomalies or outliers at a glance.
            """)

    # --- INTERPRET BENEFITS ---
    if "interpret_benefits" in results:
        st.subheader("🧬 Interpret Benefits")
        b = results["interpret_benefits"]
        st.markdown(f"**Coverage**: {b.get('coverage', '')}")
        st.markdown(f"**Copay**: {b.get('copay', '')}")
        st.markdown(f"**Summary**: {b.get('summary', '')}")

    # --- DETECT ANOMALIES ---
    if "detect_anomalies" in results:
        st.subheader("⚠️ Detect Anomalies")
        a = results["detect_anomalies"]
        st.success(a.get("message", "No anomalies detected."))

    # --- GENERATE INSIGHTS ---
    if "generate_insights" in results:
        st.subheader("🧠 Insights")
        st.markdown(results["generate_insights"].get("insight", ""))

    # --- EXPORT TO PDF ---
    st.subheader("📄 Export Report")
    pdf_bytes = generate_pdf_report(results)
    if st.download_button("⬇️ Download Report as PDF", data=BytesIO(pdf_bytes), file_name="datasage_report.pdf", mime="application/pdf"):
        pdf_exported = True

    # --- USER ENGAGEMENT SCORE ---
    def compute_engagement_score(selected_tasks, age_min, age_max, results, pdf_exported=False):
        score = 0
        messages = []

        if len(selected_tasks) >= 3:
            score += 2
            messages.append("You explored multiple agents for a deeper analysis.")
        elif len(selected_tasks) == 2:
            score += 1
            messages.append("You're using at least two insights — a solid start!")

        if age_max - age_min <= 10:
            score += 1
            messages.append("You've selected a narrow age range — precise targeting!")

        if results.get("interpret_benefits") or results.get("detect_anomalies"):
            score += 2
            messages.append("You explored specialized agents for benefits or anomaly detection.")

        if pdf_exported:
            score += 2
            messages.append("You downloaded the report — strong engagement!")

        if score >= 6:
            tier = "🔥 High"
        elif score >= 3:
            tier = "✅ Medium"
        else:
            tier = "📊 Low"

        return score, tier, messages

    score, tier, reasons = compute_engagement_score(selected_tasks, age_min, age_max, results, pdf_exported)
    st.subheader("🎯 Engagement Score")
    st.markdown(f"**Level:** {tier} ({score}/8)")

    with st.expander("💡 Why this score?"):
        for msg in reasons:
            st.markdown(f"- {msg}")









