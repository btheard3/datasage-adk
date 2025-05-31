import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run(**kwargs):
    avg = kwargs.get("avg_cost", 0)
    median = kwargs.get("median_cost", 0)
    min_cost = kwargs.get("min_cost", 0)
    max_cost = kwargs.get("max_cost", 0)

    if avg == 0 or max_cost == 0:
        return {
            "benefit_summary": "⚠️ Not enough KPI data to generate a summary."
        }

    prompt = f"""You're a healthcare policy expert. Interpret the following cost KPIs to assess benefit efficiency:
    - Avg Cost: {avg}
    - Median: {median}
    - Min: {min_cost}
    - Max: {max_cost}

    What does this suggest about patient value and efficiency of care? Limit to 2–3 sentences."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "benefit_summary": response.choices[0].message.content.strip()
    }
