import os
from typing import Dict
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Helper function to initialize BigQuery client with service account
def get_bq_client():
    key_path = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '.secrets', 'datasage-adk-v2-656c3805b9f3.json'
    )
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return bigquery.Client(credentials=credentials, project=credentials.project_id)


class AnomalyDetectorAgent:
    def __init__(self):
        self.client = get_bq_client()

    def detect_anomalies(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str) -> Dict:
        query = f"""
            SELECT
              COUNT(*) AS total_records,
              COUNTIF(cost > 5000) AS high_cost_cases
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

        total = result.get("total_records", 0)
        high = result.get("high_cost_cases", 0)

        if total == 0:
            return {
                "message": "⚠️ No records found for the selected criteria. Try adjusting the filters."
            }

        percentage = (high / total) * 100

        if percentage > 10:
            return {
                "message": f"🚨 Anomaly detected: {percentage:.1f}% of visits had unusually high costs."
            }
        else:
            return {
                "message": "✅ No significant anomalies detected in the cost data."
            }
