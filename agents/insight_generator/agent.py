import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_insight_generator(inputs):
    avg = inputs.get("avg_cost", 0)
    median = inputs.get("median_cost", 0)
    min_cost = inputs.get("min_cost", 0)
    max_cost = inputs.get("max_cost", 0)

    if avg == 0:
        return {"insights": "⚠️ Missing cost KPIs: unable to generate insights."}

    prompt = f"""
    You are a business intelligence analyst. Based on these healthcare cost metrics, generate non-obvious insights, trends, or recommendations:

    - Average Cost: {avg}
    - Median Cost: {median}
    - Min Cost: {min_cost}
    - Max Cost: {max_cost}

    Provide one insight that would help improve healthcare cost efficiency or identify unusual patterns.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"insights": response.choices[0].message["content"]}
