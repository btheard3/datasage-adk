import streamlit as st
import os
import json
from agents.cost_estimator.agent import run_cost_estimator
from agents.benefits_interpreter.agent import run_benefits_interpreter
from agents.anomaly_detector.agent import run_anomaly_detector
from agents.insight_generator.agent import run_insight_generator
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="DataSage", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7f9;
    }
    .main {
        padding: 2rem;
    }
    .st-emotion-cache-1v0mbdj {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💊 DataSage — Healthcare Cost Intelligence")
st.markdown("""
    <div style='background-color: #e8f4f8; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4>Powered by Google Cloud & Agent Development Kit</h4>
        <p>Our multi-agent system analyzes healthcare costs using BigQuery, Vertex AI, and collaborative AI agents.</p>
    </div>
""", unsafe_allow_html=True)

# ---- Filters in a cleaner sidebar ----
with st.sidebar:
    st.header("🎚️ Analysis Parameters")
    st.markdown("---")
    
    with st.expander("📊 Demographics", expanded=True):
        age_min = st.slider("Minimum Age", 0, 100, 25)
        age_max = st.slider("Maximum Age", 0, 100, 60)
        gender = st.selectbox("Gender", ["male", "female", "other"])
    
    with st.expander("📍 Location & Service", expanded=True):
        region = st.selectbox("Region", ["northeast", "southeast", "southwest", "northwest"])
        visit_type = st.selectbox("Visit Type", ["emergency", "routine", "urgent", "preventive"])

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "state": region,
    "visit_type": visit_type
}

col1, col2 = st.columns([2, 1])
with col1:
    run_button = st.button("🔄 Run Analysis", use_container_width=True)
with col2:
    auto_refresh = st.checkbox("Auto-refresh every 5 minutes")

if run_button or (auto_refresh and 'last_refresh' not in st.session_state):
    with st.spinner("🤖 Agents collaborating on analysis..."):
        # Run cost estimation
        estimate = run_cost_estimator(inputs)
        
        if all(v == 0 for v in [estimate.get("avg_cost", 0), estimate.get("median_cost", 0)]):
            st.warning("⚠️ No data available for the selected filters. Please adjust your criteria.")
            st.stop()

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Cost Analysis", "🔍 Insights", "📈 Trends"])

        with tab1:
            # Cost metrics in a grid
            metrics_cols = st.columns(4)
            with metrics_cols[0]:
                st.metric("Average Cost", f"${estimate['avg_cost']:,.2f}")
            with metrics_cols[1]:
                st.metric("Median Cost", f"${estimate['median_cost']:,.2f}")
            with metrics_cols[2]:
                st.metric("Insurance Coverage", f"{estimate['insurance_coverage_ratio']*100:.1f}%")
            with metrics_cols[3]:
                st.metric("Member Burden", f"{estimate['member_burden_ratio']*100:.1f}%")

            # Visualization
            fig = go.Figure()
            
            # Cost distribution gauge
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=estimate['avg_cost'],
                delta={"reference": estimate['median_cost']},
                gauge={
                    "axis": {"range": [0, estimate['max_cost']]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, estimate['median_cost']], "color": "lightgray"},
                        {"range": [estimate['median_cost'], estimate['max_cost']], "color": "rgb(200, 230, 255)"}
                    ]
                },
                title={"text": "Cost Distribution"}
            ))
            
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Run analysis agents
            benefits = run_benefits_interpreter(estimate)
            anomalies = run_anomaly_detector(estimate)
            insights = run_insight_generator(estimate)

            # Display insights in cards
            st.subheader("🎯 Key Findings")
            cols = st.columns(3)
            
            with cols[0]:
                st.markdown("""
                    <div style='background-color: white; padding: 1rem; border-radius: 10px; height: 200px; overflow-y: auto;'>
                        <h4>💡 Benefits Analysis</h4>
                        <p>{}</p>
                    </div>
                """.format(benefits.get("benefit_summary", "No summary available.")), unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown("""
                    <div style='background-color: white; padding: 1rem; border-radius: 10px; height: 200px; overflow-y: auto;'>
                        <h4>🚨 Risk Analysis</h4>
                        <p>{}</p>
                    </div>
                """.format(anomalies.get("explanation", "No anomalies detected.")), unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown("""
                    <div style='background-color: white; padding: 1rem; border-radius: 10px; height: 200px; overflow-y: auto;'>
                        <h4>📈 Cost Insights</h4>
                        <p>{}</p>
                    </div>
                """.format(insights.get("insights", "No insights available.")), unsafe_allow_html=True)

        with tab3:
            st.subheader("📊 Statistical Overview")
            st.markdown(f"""
                - **Sample Size**: {estimate['sample_size']:,} records
                - **Standard Deviation**: ${estimate['std_dev']:,.2f}
                - **Cost Range**: ${estimate['min_cost']:,.2f} - ${estimate['max_cost']:,.2f}
            """)

        # Update last refresh time
        st.session_state['last_refresh'] = True

# Auto-refresh script
if auto_refresh:
    st.markdown("""
        <script>
            setTimeout(function(){
                window.location.reload();
            }, 300000);
        </script>
    """, unsafe_allow_html=True)