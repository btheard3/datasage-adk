from agents.llm_reasoner.agent import LLMReasonerAgent

mock_results = {
    "estimate_cost": {"avg_cost": 2489, "median_cost": 2432},
    "benefits_interpreter": {"summary": "Service is typically covered with low out-of-pocket cost."},
    "generate_insights": {"insight": "Spring sees the highest volume of visits in the West."},
    "detect_anomalies": {"anomaly_flag": False, "message": "No anomalies detected."}
}

agent = LLMReasonerAgent()
summary = agent.summarize_outputs(mock_results)

print("🧠 LLM Summary:\n")
print(summary)


