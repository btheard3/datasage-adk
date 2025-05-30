import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class BenefitsInterpreterAgent:
    def interpret(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str):
        prompt = f"""
        You are a healthcare benefits advisor.

        Based on the following patient context:
        - Age range: {age_min} to {age_max}
        - Gender: {gender}
        - Visit type: {visit_type}
        - Region: {region}

        Provide a short summary of expected insurance coverage, potential copays, or if prior authorization is likely.
        Do not mention cost data. Return only 3 bullet points.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare benefits advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {"ai_benefits_summary": response["choices"][0]["message"]["content"]}
        except Exception as e:
            return {"ai_benefits_summary": f"⚠️ AI interpretation failed: {str(e)}"}


