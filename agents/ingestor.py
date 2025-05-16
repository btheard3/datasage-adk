from google.cloud import bigquery
from google.adk.agents import Agent
from pydantic import PrivateAttr
from dotenv import load_dotenv
import os

load_dotenv()

class IngestorAgent(Agent):
    _client: bigquery.Client = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = bigquery.Client()

    def ingest_from_bigquery(self, query: str) -> list:
        print(f"[{self.name}] Executing query: {query}")
        query_job = self._client.query(query)
        results = query_job.result()
        data = [dict(row) for row in results]
        print(f"[{self.name}] Retrieved {len(data)} records.")
        return data

    def run(self, task: dict) -> dict:
        query = task.get("query", "")
        if not query:
            raise ValueError("No BigQuery SQL query provided in task input.")
        
        data = self.ingest_from_bigquery(query)
        return {
            "status": "success",
            "source": "bigquery",
            "records": data
        }

# Standalone test
if __name__ == "__main__":
    agent = IngestorAgent(name="IngestorAgent")
    test_task = {
        "query": """
            SELECT name, SUM(number) as total
            FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE state = 'TX'
            GROUP BY name
            ORDER BY total DESC
            LIMIT 5
        """
    }
    output = agent.run(test_task)
    print(output)
