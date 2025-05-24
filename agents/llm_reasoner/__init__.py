from .agent import LLMReasonerAgent

def run(input_data, results):
    agent = LLMReasonerAgent()
    return agent.reason(input_data, results)

