# agents/cleaner.py

from google.adk.agents import Agent
from pydantic import PrivateAttr
import pandas as pd

class CleanerAgent(Agent):
    _df: pd.DataFrame = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def clean_data(self, records: list) -> list:
        self._df = pd.DataFrame(records)

        # Normalize column names
        self._df.columns = [col.lower().strip() for col in self._df.columns]

        # Drop duplicates
        self._df = self._df.drop_duplicates()

        # Fill NA with placeholder
        self._df = self._df.fillna("unknown")

        # Convert to list of dictionaries
        cleaned_records = self._df.to_dict(orient="records")
        return cleaned_records

    def run(self, task: dict) -> dict:
        records = task.get("records", [])
        if not records:
            raise ValueError("No input records provided to CleanerAgent.")

        cleaned = self.clean_data(records)
        return {
            "status": "success",
            "step": "cleaned",
            "records": cleaned
        }

# Standalone test
if __name__ == "__main__":
    agent = CleanerAgent(name="CleanerAgent")
    test_task = {
        "records": [
            {"Name": "James", "Total": 272793},
            {"Name": "James", "Total": 272793},
            {"Name": "John", "Total": 235139},
            {"Name": "Robert", "Total": None}
        ]
    }
    output = agent.run(test_task)
    print(output)
