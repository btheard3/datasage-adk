from .agent import BenefitsInterpreterAgent

def run(input_data):
    agent = BenefitsInterpreterAgent()
    return agent.interpret(
        age_min=input_data["min_age"],
        age_max=input_data["max_age"],
        gender=input_data["gender"],
        visit_type=input_data["visit_type"],
        region=input_data["region"]
    )

