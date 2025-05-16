# agents/insight.py

from google.adk.agents import Agent
from pydantic import PrivateAttr
import json

# Force fallback mode (no Vertex AI)
VERTEX_ENABLED = False

class InsightAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_summary(self, insights: dict) -> str:
        # Fallback summary logic
        total = insights.get("total", {})
        mean = total.get("mean", "N/A")
        min_val = total.get("min", "N/A")
        max_val = total.get("max", "N/A")
        top_n = len(total.get("top_5", {}))

        return (
            f"The dataset contains {top_n} top values. "
            f"The average total is {mean:.2f}, "
            f"ranging from {min_val} to {max_val}."
        )

    def run(self, task: dict) -> dict:
        insights = task.get("insights", {})
        if not insights:
            raise ValueError("No insights provided to InsightAgent.")

        summary = self.generate_summary(insights)
        return {
            "status": "success",
            "step": "insight",
            "summary": summary
        }

# Standalone test
if __name__ == "__main__":
    agent = InsightAgent(name="InsightAgent")
    test_insights = {
        "total": {
            "mean": 234535.8,
            "min": 219028,
            "max": 272793,
            "std": 22300.5,
            "top_5": {272793: 1, 235139: 1, 225320: 1, 220399: 1, 219028: 1}
        }
    }
    result = agent.run({"insights": test_insights})
    print(result)

