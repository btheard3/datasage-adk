import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMReasonerAgent:
    def __init__(self, model="gpt-4"):
        self.model = model

    def summarize(self, results: dict) -> str:
        content = "Here are the outputs from multiple agents analyzing healthcare cost data:\n"
        for task, output in results.items():
            content += f"\n---\n{task.upper()}:\n{output}\n"

        messages = [
            {"role": "system", "content": "You are a helpful medical AI analyst assistant."},
            {"role": "user", "content": content + "\n\nCan you summarize the key findings in simple terms and offer any recommendations?"}
        ]

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"LLM Error: {e}"
