import streamlit as st
from agents.planner.controller import PlannerAgent

st.set_page_config(page_title="DataSage Multi-Agent System", layout="wide")
st.title("🧠 DataSage Multi-Agent System")
st.markdown("Explore healthcare cost estimates and benefit summaries with AI agents powered by BigQuery.")

# Sidebar input
st.sidebar.header("User Profile")
age_min = st.sidebar.slider("Minimum Age", 0, 100, 30)
age_max = st.sidebar.slider("Maximum Age", age_min, 100, 40)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
visit_type = st.sidebar.selectbox("Visit Type", ["Primary Care", "Specialist", "Emergency"])
region = st.sidebar.selectbox("Region", ["West", "Northeast", "South", "Midwest"])

st.sidebar.header("Select Agent Tasks")
task_options = [
    "estimate_cost",
    "interpret_benefits",
    "generate_insights",
    "detect_anomalies",
    "llm_summary"
]
selected_tasks = st.sidebar.multiselect("Choose one or more agents to run:", task_options, default=["estimate_cost"])

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "visit_type": visit_type,
    "region": region
}

if st.button("Run Agents"):
    with st.spinner("Running agents..."):
        planner = PlannerAgent()
        results = {}

        for task in selected_tasks:
            if task == "llm_summary":
                results[task] = planner.run(task, {"results": results})
            else:
                results[task] = planner.run(task, inputs)

        st.markdown("## 📊 Results")

        # Display LLM summary cleanly
        if "llm_summary" in selected_tasks and isinstance(results.get("llm_summary"), str):
            st.subheader("🧠 LLM Summary")
            st.write(results["llm_summary"])

        # Display all other agent results as JSON
        for task in selected_tasks:
            if task == "llm_summary":
                continue  # already shown above
            output = results.get(task)
            if output:
                st.subheader(f"🔹 {task.replace('_', ' ').title()}")
                st.json(output)

