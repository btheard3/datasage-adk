import os
from typing import Dict
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

class CostEstimatorAgent:
    def __init__(self):
        key_path = os.path.join(
            os.path.dirname(__file__), "..", "..", ".secrets", "datasage-adk-v2-656c3805b9f3.json"
        )
        credentials = service_account.Credentials.from_service_account_file(key_path)
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    def run(self, inputs: Dict) -> Dict:
        query = f"""
            SELECT
                AVG(cost) AS avg_cost,
                APPROX_QUANTILES(cost, 2)[OFFSET(1)] AS median_cost,
                MIN(cost) AS min_cost,
                MAX(cost) AS max_cost
            FROM `datasage-adk-v2.datasage_health.healthcare_costs`
            WHERE
                age BETWEEN @age_min AND @age_max
                AND gender = @gender
                AND visit_type = @visit_type
                AND region = @region
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("age_min", "INT64", inputs["age_min"]),
                bigquery.ScalarQueryParameter("age_max", "INT64", inputs["age_max"]),
                bigquery.ScalarQueryParameter("gender", "STRING", inputs["gender"]),
                bigquery.ScalarQueryParameter("visit_type", "STRING", inputs["visit_type"]),
                bigquery.ScalarQueryParameter("region", "STRING", inputs["region"]),
            ]
        )

        try:
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result().to_dataframe().to_dict(orient="records")
            if not results or results[0]["avg_cost"] is None:
                return {k: 0 for k in ["avg_cost", "median_cost", "min_cost", "max_cost"]}
            result = results[0]
            return {
                "avg_cost": float(result["avg_cost"]),
                "median_cost": float(result["median_cost"]),
                "min_cost": float(result["min_cost"]),
                "max_cost": float(result["max_cost"]),
            }
        except Exception as e:
            return {"avg_cost": 0, "median_cost": 0, "min_cost": 0, "max_cost": 0, "error": str(e)}



