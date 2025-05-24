import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
class LLMReasonerAgent:
    def __init__(self):
        # Setup for OpenAI or other LLM client
        import openai
        import os
        from dotenv import load_dotenv
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def reason(self, input_data: dict, results: dict) -> dict:
        # Construct context from previous agents
        context_parts = []
        if "estimate_cost" in results:
            context_parts.append(f"Estimated Cost: {results['estimate_cost']}")
        if "generate_insights" in results:
            context_parts.append(f"Insights: {results['generate_insights']}")
        if "interpret_benefits" in results:
            context_parts.append(f"Benefits: {results['interpret_benefits']}")
        if "detect_anomalies" in results:
            context_parts.append(f"Anomalies: {results['detect_anomalies']}")

        full_context = "\n".join(context_parts)

        prompt = f"""You are a healthcare analyst. Based on the following data, generate a brief summary with 3 main points and one recommendation:\n\n{full_context}"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return {"summary": response['choices'][0]['message']['content']}

