import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_anomaly_detector(inputs):
    avg = inputs.get("avg_cost", 0)
    median = inputs.get("median_cost", 0)
    min_cost = inputs.get("min_cost", 0)
    max_cost = inputs.get("max_cost", 0)

    flags = []
    if min_cost == 0 or max_cost == 0:
        flags.append("zero_extremes")
    elif avg == 0:
        flags.append("zero_average")

    prompt = f"""
    Based on the following healthcare cost KPIs, write a 2-sentence analysis of any data quality anomalies or red flags:
    - Average Cost: {avg}
    - Median Cost: {median}
    - Min Cost: {min_cost}
    - Max Cost: {max_cost}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    explanation = response.choices[0].message["content"]
    return {"anomaly_flags": flags, "explanation": explanation}

