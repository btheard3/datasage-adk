# agents/presenter.py

from google.adk.agents import Agent
from pydantic import PrivateAttr
import pandas as pd
from tabulate import tabulate

class PresenterAgent(Agent):
    _df: pd.DataFrame = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_report(self, records: list, summary: str) -> str:
        self._df = pd.DataFrame(records)

        table = tabulate(self._df.head(10), headers="keys", tablefmt="github")
        report = f"""# 📊 Final Report

## 🔍 Summary
{summary}

## 🧾 Sample of Cleaned Data (Top 10 Rows)
{table}
"""
        return report

    def run(self, task: dict) -> dict:
        records = task.get("records", [])
        summary = task.get("summary", "")

        if not records:
            raise ValueError("No records provided to PresenterAgent.")
        if not summary:
            raise ValueError("No summary provided to PresenterAgent.")

        report = self.build_report(records, summary)
        return {
            "status": "success",
            "step": "present",
            "report": report
        }

# Standalone test
if __name__ == "__main__":
    agent = PresenterAgent(name="PresenterAgent")
    test_task = {
        "summary": "The average total is 234535.80, ranging from 219028 to 272793.",
        "records": [
            {"name": "James", "total": 272793},
            {"name": "John", "total": 235139},
            {"name": "Michael", "total": 225320},
            {"name": "Robert", "total": 220399},
            {"name": "David", "total": 219028}
        ]
    }
    output = agent.run(test_task)
    print(output["report"])
