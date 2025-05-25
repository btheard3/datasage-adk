from .agent import AnomalyDetectorAgent

def detect_anomalies(input_data: dict) -> dict:
    agent = AnomalyDetectorAgent()
    return agent.detect(
        age_min=input_data["age_min"],
        age_max=input_data["age_max"],
        gender=input_data["gender"],
        visit_type=input_data["visit_type"],
        region=input_data["region"]
    )
