from .agent import AnomalyDetectorAgent

def run(input_data):
    agent = AnomalyDetectorAgent()
    return agent.detect(
        age_min=input_data["min_age"],
        age_max=input_data["max_age"],
        gender=input_data["gender"],
        visit_type=input_data["visit_type"],
        region=input_data["region"]
    )
