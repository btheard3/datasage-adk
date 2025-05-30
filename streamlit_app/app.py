import streamlit as st
import os
from dotenv import load_dotenv
from agents.cost_estimator.agent import CostEstimatorAgent
from agents.insight_generator.agent import InsightGeneratorAgent
from agents.benefits_interpreter.agent import BenefitsInterpreterAgent
from agents.anomaly_detector.agent import AnomalyDetectorAgent
from streamlit_app.pdf_export import generate_pdf_report
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(page_title="DataSage Multi-Agent System", layout="wide")
st.title("🧠 DataSage Multi-Agent System")
st.caption("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# Sidebar inputs
st.sidebar.header("⚙️ Configure Inputs")
age_min = st.sidebar.slider("Minimum Age", 0, 100, 25)
age_max = st.sidebar.slider("Maximum Age", age_min, 100, 65)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
region = st.sidebar.selectbox("Region", ["Northeast", "Midwest", "South", "West"])
visit_type = st.sidebar.selectbox("Visit Type", ["Emergency", "Primary Care", "Inpatient", "Outpatient"])

selected_agents = st.sidebar.multiselect(
    "🧠 Select Agents to Run",
    options=["estimate_cost", "generate_insights", "interpret_benefits", "detect_anomalies"],
    default=[]
)

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "region": region,
    "visit_type": visit_type,
}

results = {}
pdf_bytes = None  # Persisted outside export buttons

# Run agents
if st.sidebar.button("▶️ Run Agents"):
    if "estimate_cost" in selected_agents:
        results["estimate_cost"] = CostEstimatorAgent().run(inputs)

    if "generate_insights" in selected_agents:
        results["generate_insights"] = InsightGeneratorAgent().run(inputs, results)

    if "interpret_benefits" in selected_agents:
        results["interpret_benefits"] = BenefitsInterpreterAgent().interpret(**inputs)

    if "detect_anomalies" in selected_agents:
        results["detect_anomalies"] = AnomalyDetectorAgent().run(inputs)

# Only show content once agents have run
if results:

    # 📊 Cost KPIs
    if "estimate_cost" in results:
        st.subheader("💲 Estimate Cost Summary")
        cost_data = results["estimate_cost"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Avg Cost", f"${cost_data.get('avg_cost', 0):,.2f}")
        col2.metric("🧮 Median Cost", f"${cost_data.get('median_cost', 0):,.2f}")
        col3.metric("🔻 Min Cost", f"${cost_data.get('min_cost', 0):,.2f}")
        col4.metric("🔺 Max Cost", f"${cost_data.get('max_cost', 0):,.2f}")

        with st.expander("📊 What do these cost KPIs mean?"):
            st.markdown("""
            - **Avg Cost**: The average cost across all qualifying visits.
            - **Median Cost**: The midpoint — 50% of visits cost more, 50% less.
            - **Min/Max Cost**: The extremes observed under the filters you selected.
            """)

    # 📈 Cost Gauge
    if "estimate_cost" in results:
        st.subheader("📈 Cost Distribution Gauge")
        avg = results["estimate_cost"]["avg_cost"]
        median = results["estimate_cost"]["median_cost"]

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg,
            delta={'reference': median, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={'axis': {'range': [0, max(avg, median) * 1.5]}},
            title={"text": "Avg vs Median Cost"},
        ))

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("ℹ️ What does the gauge show?"):
            st.write("This gauge compares the average cost to the median to indicate possible cost skew or outliers.")

    # 🧬 Interpret Benefits
    if "interpret_benefits" in results:
        st.subheader("🧬 Interpret Benefits")
        benefits = results["interpret_benefits"]
        if "ai_benefits_summary" in benefits:
            st.markdown(benefits["ai_benefits_summary"])
        else:
            st.write(f"**Coverage:** {benefits.get('coverage', 'N/A')}")
            st.write(f"**Copay:** {benefits.get('copay', 'N/A')}")
            st.write(f"**Summary:** {benefits.get('summary', 'N/A')}")

    # ⚠️ Anomaly Detection
    if "detect_anomalies" in results:
        st.subheader("⚠️ Detect Anomalies")
        anomaly_result = results["detect_anomalies"].get("message", "")
        if "No significant" in anomaly_result:
            st.success(anomaly_result)
        else:
            st.warning(anomaly_result)

    # 📌 Insights
    if "generate_insights" in results:
        st.subheader("📌 Generate Insights")
        st.markdown(results["generate_insights"].get("insight", "No insights returned."))

    # 📤 PDF Export (with 2-step pattern)
    st.subheader("📤 Export Results")

    if st.button("📝 Generate PDF"):
        try:
            pdf_bytes = generate_pdf_report(results)
            st.success("✅ PDF generated successfully!")
        except Exception as e:
            st.error(f"❌ Failed to generate PDF: {e}")

    if pdf_bytes:
        st.download_button("📄 Download PDF", data=pdf_bytes, file_name="report.pdf", mime="application/pdf")











