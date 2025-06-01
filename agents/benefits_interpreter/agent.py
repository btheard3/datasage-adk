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
You are a healthcare benefits specialist. Your role is to interpret cost KPIs from a policy and plan design perspective.
Explain what the following numbers could mean in terms of member coverage, plan utilization, access, and affordability:

- Average Cost: {avg}
- Median Cost: {median}
- Minimum Cost: {min_cost}
- Maximum Cost: {max_cost}

Focus on:
1. What this tells us about how members are using their benefits.
2. Whether these numbers suggest equitable or skewed access.
3. How this could guide benefit redesign or communication strategy.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a healthcare benefits interpretation expert."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content.strip()
    return {"benefit_summary": summary}

