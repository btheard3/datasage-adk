# agents/analyst.py

from google.adk.agents import Agent
from pydantic import PrivateAttr
import pandas as pd
import numpy as np

class AnalystAgent(Agent):
    _df: pd.DataFrame = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def analyze_data(self, records: list) -> dict:
        self._df = pd.DataFrame(records)

        numeric_cols = self._df.select_dtypes(include=np.number).columns.tolist()
        stats = {}

        for col in numeric_cols:
            stats[col] = {
                "mean": self._df[col].mean(),
                "min": self._df[col].min(),
                "max": self._df[col].max(),
                "std": self._df[col].std(),
                "top_5": self._df[col].value_counts().head(5).to_dict()
            }

        return stats

    def run(self, task: dict) -> dict:
        records = task.get("records", [])
        if not records:
            raise ValueError("No records provided to AnalystAgent.")

        insights = self.analyze_data(records)
        return {
            "status": "success",
            "step": "analysis",
            "insights": insights
        }

# Standalone test
if __name__ == "__main__":
    agent = AnalystAgent(name="AnalystAgent")
    test_task = {
        "records": [
            {"name": "James", "total": 272793},
            {"name": "John", "total": 235139},
            {"name": "Michael", "total": 225320},
            {"name": "Robert", "total": 220399},
            {"name": "David", "total": 219028}
        ]
    }
    output = agent.run(test_task)
    print(output)
