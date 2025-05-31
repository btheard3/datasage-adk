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

    flags = []
    explanation = ""

    if min_cost == 0 or max_cost == 0:
        flags.append("zero_extremes")
        explanation = "⚠️ Min or max cost is zero, which may indicate missing or anomalous data."
    elif avg == 0:
        flags.append("zero_average")
        explanation = "⚠️ Average cost is zero, which could indicate a data pipeline issue."
    else:
        prompt = f"""You're a healthcare analyst. Analyze this cost KPI for anomalies:
        - Average Cost: {avg}
        - Median Cost: {median}
        - Min Cost: {min_cost}
        - Max Cost: {max_cost}

        Are there any statistical outliers or signs of data quality issues? Summarize in 1–2 sentences."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        explanation = response.choices[0].message.content.strip()

    return {
        "anomaly_flags": flags,
        "explanation": explanation
    }
