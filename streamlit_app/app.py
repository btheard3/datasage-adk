import streamlit as st
from agents.planner.controller import PlannerAgent

# Initialize planner
planner = PlannerAgent()

st.set_page_config(page_title="DataSage Agent Hub", layout="centered")
st.title("🧠 DataSage Multi-Agent System")
st.markdown("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# --- Sidebar: Input parameters ---
st.sidebar.header("User Profile")
age_min = st.sidebar.slider("Minimum Age", 0, 100, 30)
age_max = st.sidebar.slider("Maximum Age", age_min, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Specialist Visit", "Emergency"])
region = st.sidebar.selectbox("Region", ["Northeast", "South", "Midwest", "West"])

params = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "visit_type": visit_type,
    "region": region
}

# --- Agent Selection ---
st.sidebar.header("Select Agent Tasks")
selected_tasks = st.sidebar.multiselect(
    "Choose one or more agents to run:",
    ["estimate_cost", "interpret_benefits"],
    default=["estimate_cost"]
)

# --- Run Agents ---
if st.button("Run Agents"):
    for task in selected_tasks:
        with st.spinner(f"Running {task.replace('_', ' ').title()}..."):
            result = planner.run(task, params)
            st.subheader(f"🔍 Result from `{task}`")
            st.json(result)

