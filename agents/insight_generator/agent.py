import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class InsightGeneratorAgent:
    def run(self, input_data: dict, results: dict = None) -> dict:
        context = []

        if results and "estimate_cost" in results:
            cost = results["estimate_cost"]
            context.append(
                f"Estimated healthcare cost: Avg = ${cost.get('avg_cost')}, Median = ${cost.get('median_cost')}."
            )

        if results and "interpret_benefits" in results:
            benefits = results["interpret_benefits"]
            context.append(
                f"Benefits: {benefits.get('summary')} Coverage: {benefits.get('coverage')}, Copay: {benefits.get('copay')}."
            )

        if results and "detect_anomalies" in results:
            anomaly = results["detect_anomalies"]
            context.append(f"Anomaly check: {anomaly.get('message')}")

        user_profile = (
            f"User profile: {input_data.get('gender')} aged {input_data.get('age_min')}–{input_data.get('age_max')}, "
            f"Region: {input_data.get('region')}, Visit type: {input_data.get('visit_type')}."
        )

        prompt = (
            f"{user_profile}\n\n"
            f"{chr(10).join(context)}\n\n"
            "Please generate a 3-bullet insight summary and one personalized recommendation based on the data above."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare data analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            insight = response["choices"][0]["message"]["content"]
        except Exception as e:
            insight = f"⚠️ OpenAI error: {str(e)}"

        return {"insight": insight}








