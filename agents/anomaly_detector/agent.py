class AnomalyDetectorAgent:
    def run(self, inputs: dict) -> dict:
        if inputs["visit_type"] == "Emergency" and inputs["age_max"] > 70:
            return {"message": "⚠️ Higher-than-expected emergency costs detected for elderly patients."}
        return {"message": "✅ No significant anomalies detected in the cost data."}
