# tests/test_agents.py

from agents.planner.controller import PlannerAgent

planner = PlannerAgent()

output1 = planner.run("estimate_cost", {
    "age_min": 30,
    "age_max": 40,
    "gender": "Male",
    "visit_type": "Primary Care",
    "region": "West"
})

output2 = planner.run("interpret_benefits", {
    "age_min": 30,
    "age_max": 40,
    "gender": "Male",
    "visit_type": "Primary Care",
    "region": "West"
})

print("Cost Estimate:", output1)
print("Benefit Summary:", output2)

