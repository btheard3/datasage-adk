from agents.planner.controller import PlannerAgent

planner = PlannerAgent()

params = {
    "age_min": 30,
    "age_max": 40,
    "gender": "Male",
    "visit_type": "Primary Care",
    "region": "West"
}

output1 = planner.run("estimate_cost", params)
output2 = planner.run("interpret_benefits", params)
output3 = planner.run("generate_insights", params)
output4 = planner.run("detect_anomalies", params)

print("Cost Estimate:", output1)
print("Benefit Summary:", output2)
print("Insights:", output3)
print("Anomalies:", output4)


