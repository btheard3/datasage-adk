import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_benefits_interpreter(inputs):
    avg = inputs.get("avg_cost", 0)
    median = inputs.get("median_cost", 0)
    min_cost = inputs.get("min_cost", 0)
    max_cost = inputs.get("max_cost", 0)

    if avg == 0 or max_cost == 0:
        return {"benefit_summary": "⚠️ Not enough KPI data to generate a summary."}

    prompt = f"""
    You are a healthcare analyst. Based on these healthcare cost KPIs, write a short 3-sentence summary of what this might mean from a benefits perspective:
    - Average Cost: {avg}
    - Median Cost: {median}
    - Min Cost: {min_cost}
    - Max Cost: {max_cost}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message["content"]
    return {"benefit_summary": summary}
