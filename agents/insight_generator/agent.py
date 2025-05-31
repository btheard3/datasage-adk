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

    if avg == 0:
        return {
            "insights": "⚠️ Missing cost KPIs: unable to generate insights."
        }

    prompt = f"""You're a business intelligence analyst. Given the following healthcare cost KPIs:
    - Average Cost: {avg}
    - Median Cost: {median}
    - Min Cost: {min_cost}
    - Max Cost: {max_cost}

    Derive 2–3 actionable insights or trends. Think like someone advising hospital executives on cost control."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "insights": response.choices[0].message.content.strip()
    }
