import streamlit as st
import os
import json
from agents.cost_estimator.agent import run_cost_estimator
from agents.benefits_interpreter.agent import run_benefits_interpreter
from agents.anomaly_detector.agent import run_anomaly_detector
from agents.insight_generator.agent import run_insight_generator
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="DataSage ADK", layout="wide")

# Enhanced UI with modern styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .insight-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header with ADK branding
st.title("🤖 DataSage ADK — Healthcare Intelligence Platform")
st.markdown("""
    <div style='background-color: #e8f5e9; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4>🏆 Google Cloud & Agent Development Kit Showcase</h4>
        <p>Advanced healthcare analytics powered by collaborative AI agents using Google Cloud's BigQuery, Vertex AI, and ADK.</p>
    </div>
""", unsafe_allow_html=True)

# Enhanced sidebar with agent status
with st.sidebar:
    st.header("🎛️ Analysis Configuration")
    st.markdown("---")
    
    with st.expander("👥 Patient Demographics", expanded=True):
        age_min = st.slider("Minimum Age", 0, 100, 25)
        age_max = st.slider("Maximum Age", 0, 100, 60)
        gender = st.selectbox("Gender", ["male", "female", "other"])
    
    with st.expander("📍 Location & Service", expanded=True):
        region = st.selectbox("Region", ["northeast", "southeast", "southwest", "northwest"])
        visit_type = st.selectbox("Visit Type", ["emergency", "routine", "urgent", "preventive"])
    
    st.markdown("---")
    st.subheader("🤖 Active Agents")
    agent_statuses = {
        "Cost Estimator": "Connected to BigQuery",
        "Benefits Interpreter": "GPT-4 Ready",
        "Anomaly Detector": "Active",
        "Insight Generator": "Processing"
    }
    for agent, status in agent_statuses.items():
        st.markdown(f"""
            <div class='agent-status' style='background-color: #e8f5e9;'>
                ✅ {agent}<br/>
                <small style='color: #666;'>{status}</small>
            </div>
        """, unsafe_allow_html=True)

inputs = {
    "age_min": age_min,
    "age_max": age_max,
    "gender": gender,
    "state": region,
    "visit_type": visit_type
}

col1, col2 = st.columns([2, 1])
with col1:
    run_button = st.button("🔄 Execute Agent Workflow", use_container_width=True)
with col2:
    auto_refresh = st.checkbox("Enable Auto-refresh (5min)")

if run_button or (auto_refresh and 'last_refresh' not in st.session_state):
    with st.spinner("🤖 Multi-Agent System Processing..."):
        # Cost estimation agent
        estimate = run_cost_estimator(inputs)
        
        if all(v == 0 for v in [estimate.get("avg_cost", 0), estimate.get("median_cost", 0)]):
            st.warning("⚠️ Insufficient data for selected criteria. Please adjust filters.")
            st.stop()

        # Create enhanced tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Cost Analysis", "🔍 Agent Insights", "📈 Trends", "🤖 Agent Collaboration"])

        with tab1:
            # Enhanced metrics display
            st.subheader("💰 Cost Metrics")
            metrics_cols = st.columns(4)
            with metrics_cols[0]:
                st.metric("Average Cost", f"${estimate['avg_cost']:,.2f}", 
                         delta=f"{((estimate['avg_cost']-estimate['median_cost'])/estimate['median_cost']*100):,.1f}%")
            with metrics_cols[1]:
                st.metric("Median Cost", f"${estimate['median_cost']:,.2f}")
            with metrics_cols[2]:
                st.metric("Insurance Coverage", f"{estimate['insurance_coverage_ratio']*100:.1f}%")
            with metrics_cols[3]:
                st.metric("Member Burden", f"{estimate['member_burden_ratio']*100:.1f}%")

            # Enhanced visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Cost distribution gauge
                fig_gauge = go.Figure()
                fig_gauge.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=estimate['avg_cost'],
                    delta={"reference": estimate['median_cost']},
                    gauge={
                        "axis": {"range": [0, estimate['max_cost']]},
                        "bar": {"color": "#1976D2"},
                        "steps": [
                            {"range": [0, estimate['median_cost']], "color": "#E3F2FD"},
                            {"range": [estimate['median_cost'], estimate['max_cost']], "color": "#BBDEFB"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": estimate['avg_cost']
                        }
                    },
                    title={"text": "Cost Distribution Analysis"}
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                # Cost breakdown
                fig_breakdown = go.Figure()
                fig_breakdown.add_trace(go.Bar(
                    x=['Member Paid', 'Insurance Paid'],
                    y=[estimate['member_burden_ratio']*100, estimate['insurance_coverage_ratio']*100],
                    marker_color=['#FFA726', '#42A5F5']
                ))
                fig_breakdown.update_layout(
                    title="Cost Share Analysis",
                    yaxis_title="Percentage (%)",
                    showlegend=False
                )
                st.plotly_chart(fig_breakdown, use_container_width=True)

        with tab2:
            # Run analysis agents
            benefits = run_benefits_interpreter(estimate)
            anomalies = run_anomaly_detector(estimate)
            insights = run_insight_generator(estimate)

            st.subheader("🎯 Multi-Agent Analysis")
            cols = st.columns(3)
            
            with cols[0]:
                st.markdown("""
                    <div class='insight-card'>
                        <h4>💡 Benefits Analysis</h4>
                        <p style='color: #1976D2;'>{}</p>
                    </div>
                """.format(benefits.get("benefit_summary", "Analysis pending...")), unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown("""
                    <div class='insight-card'>
                        <h4>🚨 Risk Analysis</h4>
                        <p style='color: #D32F2F;'>{}</p>
                    </div>
                """.format(anomalies.get("explanation", "No anomalies detected.")), unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown("""
                    <div class='insight-card'>
                        <h4>📈 Cost Insights</h4>
                        <p style='color: #388E3C;'>{}</p>
                    </div>
                """.format(insights.get("insights", "Processing insights...")), unsafe_allow_html=True)

        with tab3:
            st.subheader("📊 Statistical Analysis")
            
            # Enhanced stats display
            stats_cols = st.columns(3)
            with stats_cols[0]:
                st.markdown("""
                    <div class='metric-card'>
                        <h3>Sample Size</h3>
                        <h2>{:,}</h2>
                        <p>Total records analyzed</p>
                    </div>
                """.format(estimate['sample_size']), unsafe_allow_html=True)
            
            with stats_cols[1]:
                st.markdown("""
                    <div class='metric-card'>
                        <h3>Cost Variance</h3>
                        <h2>${:,.2f}</h2>
                        <p>Standard deviation</p>
                    </div>
                """.format(estimate['std_dev']), unsafe_allow_html=True)
            
            with stats_cols[2]:
                st.markdown("""
                    <div class='metric-card'>
                        <h3>Cost Range</h3>
                        <h2>${:,.2f} - ${:,.2f}</h2>
                        <p>Min to Max spread</p>
                    </div>
                """.format(estimate['min_cost'], estimate['max_cost']), unsafe_allow_html=True)

        with tab4:
            st.subheader("🤖 Agent Collaboration Workflow")
            
            # Agent collaboration diagram
            st.graphviz_chart("""
                digraph G {
                    rankdir=LR;
                    node [shape=box, style=rounded, fontname="Arial"];
                    edge [fontname="Arial"];
                    
                    BigQuery [shape=cylinder, label="BigQuery\nHealthcare Data"];
                    CostEstimator [label="Cost Estimator\nAgent"];
                    BenefitsInterpreter [label="Benefits Interpreter\nAgent"];
                    AnomalyDetector [label="Anomaly Detector\nAgent"];
                    InsightGenerator [label="Insight Generator\nAgent"];
                    
                    BigQuery -> CostEstimator [label="Raw Data"];
                    CostEstimator -> BenefitsInterpreter [label="Cost Metrics"];
                    CostEstimator -> AnomalyDetector [label="Cost Patterns"];
                    BenefitsInterpreter -> InsightGenerator [label="Benefits Analysis"];
                    AnomalyDetector -> InsightGenerator [label="Risk Patterns"];
                }
            """)
            
            # Agent execution timeline
            st.markdown("""
                <div style='background-color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h4>🔄 Agent Execution Timeline</h4>
                    <ol>
                        <li>Cost Estimator queries BigQuery for healthcare cost data</li>
                        <li>Benefits Interpreter analyzes coverage patterns using GPT-4</li>
                        <li>Anomaly Detector identifies unusual cost patterns</li>
                        <li>Insight Generator synthesizes findings from all agents</li>
                    </ol>
                </div>
            """, unsafe_allow_html=True)

        # Update refresh state
        st.session_state['last_refresh'] = True

# Auto-refresh functionality
if auto_refresh:
    st.markdown("""
        <script>
            setTimeout(function(){
                window.location.reload();
            }, 300000);
        </script>
    """, unsafe_allow_html=True)