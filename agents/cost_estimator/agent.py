import os
from typing import Dict
from google.cloud import bigquery
from dotenv import load_dotenv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(".secrets/datasage-adk-v2-656c3805b9f3.json")


load_dotenv()

class CostEstimatorAgent:
    def __init__(self):
        self.client = bigquery.Client()

    def estimate_cost(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str) -> Dict:
        query = f"""
        SELECT 
            AVG(cost) AS avg_cost,
            APPROX_QUANTILES(cost, 2)[OFFSET(1)] AS median_cost
        FROM `datasage-adk-v2.datasage_health.healthcare_costs`
        WHERE age BETWEEN @age_min AND @age_max
            AND gender = @gender
            AND visit_type = @visit_type
            AND region = @region
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("age_min", "INT64", age_min),
                bigquery.ScalarQueryParameter("age_max", "INT64", age_max),
                bigquery.ScalarQueryParameter("gender", "STRING", gender),
                bigquery.ScalarQueryParameter("visit_type", "STRING", visit_type),
                bigquery.ScalarQueryParameter("region", "STRING", region),
            ]
        )

        query_job = self.client.query(query, job_config=job_config)
        result = query_job.result().to_dataframe().to_dict(orient="records")[0]

        return {
            "avg_cost": round(result["avg_cost"], 2),
            "median_cost": round(result["median_cost"], 2)
        }

if __name__ == "__main__":
    agent = CostEstimatorAgent()
    output = agent.estimate_cost(age_min=30, age_max=40, gender="Male", visit_type="Mental Health", region="South")
    print("Estimated Cost:", output)
