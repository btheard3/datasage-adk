# agents/insight_generator/agent.py

class InsightGeneratorAgent:
    def generate(self, **kwargs):
        return {
            "insight": "Visits peak in spring due to allergies. Consider staffing accordingly.",
            "input_params": kwargs
        }
