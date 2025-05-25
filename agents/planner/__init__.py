from agents.cost_estimator import estimate_cost
from agents.benefits_interpreter import interpret_benefits
from agents.anomaly_detector import detect_anomalies
from agents.insight_generator import generate_insights
from agents.llm_reasoner import llm_summary

def execute_agents(input_data: dict, selected_tasks: list) -> dict:
    results = {}
    
    if "estimate_cost" in selected_tasks:
        results["estimate_cost"] = estimate_cost(input_data)

    if "generate_insights" in selected_tasks:
        results["generate_insights"] = generate_insights(input_data, results)

    if "interpret_benefits" in selected_tasks:
        results["interpret_benefits"] = interpret_benefits(input_data)

    if "detect_anomalies" in selected_tasks:
        results["detect_anomalies"] = detect_anomalies(input_data)

    if "llm_summary" in selected_tasks:
        results["llm_summary"] = llm_summary(input_data, results)

    return results


