import os
from typing import Dict
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

class CostEstimatorAgent:
    def __init__(self):
        key_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '.secrets', 'datasage-adk-v2-656c3805b9f3.json'
        )
        credentials = service_account.Credentials.from_service_account_file(
            key_path
        )
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    def estimate_cost(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str) -> Dict:
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
                bigquery.ScalarQueryParameter("age_min", "INT64", age_min),
                bigquery.ScalarQueryParameter("age_max", "INT64", age_max),
                bigquery.ScalarQueryParameter("gender", "STRING", gender),
                bigquery.ScalarQueryParameter("visit_type", "STRING", visit_type),
                bigquery.ScalarQueryParameter("region", "STRING", region),
            ]
        )

        query_job = self.client.query(query, job_config=job_config)
        result = query_job.result().to_dataframe().to_dict(orient="records")[0]
        return result


