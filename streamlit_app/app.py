import streamlit as st
import plotly.graph_objects as go
from agents.planner import execute_agents

# === UI ===
st.set_page_config(page_title="DataSage Multi-Agent System", layout="wide")
st.title("🧠 DataSage Multi-Agent System")
st.caption("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# === Sidebar Inputs ===
st.sidebar.header("User Profile")
min_age = st.sidebar.slider("Minimum Age", 0, 100, 30)
max_age = st.sidebar.slider("Maximum Age", min_age, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Specialist", "Emergency"])
region = st.sidebar.selectbox("Region", ["West", "South", "Northeast", "Midwest"])

st.sidebar.header("Select Agent Tasks")
selected_tasks = st.sidebar.multiselect(
    "Choose one or more agents to run:",
    options=["estimate_cost", "generate_insights", "interpret_benefits", "detect_anomalies", "llm_summary"],
    default=["estimate_cost"]
)

# === Default placeholders ===
estimate_result = {}
insights_result = {}
benefits_result = {}
anomaly_result = {}
llm_result = {}

# === Run Button ===
if st.sidebar.button("🚀 Run Agents"):
    input_data = {
        "min_age": min_age,
        "max_age": max_age,
        "gender": gender,
        "visit_type": visit_type,
        "region": region
    }

    results = execute_agents(input_data, selected_tasks)

    estimate_result = results.get("estimate_cost", {})
    insights_result = results.get("generate_insights", {})
    benefits_result = results.get("interpret_benefits", {})
    anomaly_result = results.get("detect_anomalies", {})
    llm_result = results.get("llm_summary", {})

# === KPI Display ===
def display_kpi_metrics(cost_data):
    st.subheader("📊 Key Cost Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Cost", f"${cost_data.get('avg_cost', 0):,.2f}")
    col2.metric("Median Cost", f"${cost_data.get('median_cost', 0):,.2f}")
    col3.metric("Min Cost", f"${cost_data.get('min_cost', 0):,.2f}")
    col4.metric("Max Cost", f"${cost_data.get('max_cost', 0):,.2f}")

    with st.expander("ℹ️ What these KPIs mean"):
        st.markdown("""
        - **Avg Cost**: The average cost of care based on selected filters.
        - **Median Cost**: The midpoint cost value—less sensitive to outliers.
        - **Min/Max Cost**: The lowest and highest recorded costs in this cohort.
        - **Gauge Chart**: Visualizes whether the average is below or above the median—useful for detecting skewness in data.
        """)

# === Plotly Chart ===
def plot_cost_distribution(cost_data):
    st.subheader("📈 Cost Distribution")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=cost_data.get("avg_cost", 0),
        delta={"reference": cost_data.get("median_cost", 0)},
        gauge={
            "axis": {"range": [cost_data.get("min_cost", 0), cost_data.get("max_cost", 5000)]},
            "bar": {"color": "green"},
            "steps": [
                {"range": [cost_data.get("min_cost", 0), cost_data.get("avg_cost", 0)], "color": "lightgreen"},
                {"range": [cost_data.get("avg_cost", 0), cost_data.get("max_cost", 5000)], "color": "lightgray"},
            ],
        },
        title={"text": "Average Cost Comparison"}
    ))
    st.plotly_chart(fig, use_container_width=True)

# === Render Outputs ===
if estimate_result:
    st.markdown("## 🧾 Estimate Cost")
    display_kpi_metrics({
        "avg_cost": estimate_result.get("avg_cost", 0),
        "median_cost": estimate_result.get("median_cost", 0),
        "min_cost": insights_result.get("min_cost", 0),
        "max_cost": insights_result.get("max_cost", 0),
    })
    plot_cost_distribution({
        "avg_cost": estimate_result.get("avg_cost", 0),
        "median_cost": estimate_result.get("median_cost", 0),
        "min_cost": insights_result.get("min_cost", 0),
        "max_cost": insights_result.get("max_cost", 0),
    })

if insights_result:
    st.markdown("## 🔍 Generate Insights")
    st.success(insights_result.get("insight", "No insight found."))

if benefits_result:
    st.markdown("## 🩺 Interpret Benefits")
    st.info(f"**Summary:** {benefits_result.get('summary', '')}")
    st.info(f"**Coverage:** {benefits_result.get('coverage', '')}")
    st.info(f"**Copay:** {benefits_result.get('copay', '')}")

if anomaly_result:
    st.markdown("## 🚨 Detect Anomalies")
    st.warning(anomaly_result.get("message", "No anomalies detected."))

if llm_result:
    st.markdown("## 🧠 Summary")
    st.markdown(llm_result.get("summary", ""), unsafe_allow_html=True)


