from agents.cost_estimator.agent import CostEstimatorAgent
from agents.benefits_interpreter.agent import BenefitsInterpreterAgent
from agents.insight_generator.agent import InsightGeneratorAgent
from agents.anomaly_detector.agent import AnomalyDetectorAgent
from agents.llm_reasoner.agent import LLMReasonerAgent  # NEW

class PlannerAgent:
    def __init__(self):
        self.cost_estimator = CostEstimatorAgent()
        self.benefits_interpreter = BenefitsInterpreterAgent()
        self.insight_generator = InsightGeneratorAgent()
        self.anomaly_detector = AnomalyDetectorAgent()
        self.llm_reasoner = LLMReasonerAgent()  # NEW

    def run(self, task: str, params: dict):
        if task == "estimate_cost":
            return self.cost_estimator.estimate_cost(**params)

        elif task == "interpret_benefits":
            return self.benefits_interpreter.interpret(**params)

        elif task == "generate_insights":
            return self.insight_generator.generate(**params)

        elif task == "detect_anomalies":
            return self.anomaly_detector.detect(**params)

        elif task == "llm_summary":
            return self.llm_reasoner.summarize(params["results"])

        else:
            return {"error": f"Unknown task: {task}"}


