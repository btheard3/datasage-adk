from google.cloud import bigquery

class AnomalyDetectorAgent:
    def __init__(self):
        self.client = bigquery.Client()

    def detect(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str):
        query = """
        SELECT
            cost,
            visit_type,
            region,
            age,
            gender,
            ABS(cost - AVG(cost) OVER()) / STDDEV(cost) OVER() AS z_score
        FROM `datasage-adk-v2.datasage_health.healthcare_costs`
        WHERE age BETWEEN @age_min AND @age_max
          AND gender = @gender
          AND visit_type = @visit_type
          AND region = @region
        QUALIFY z_score > 2
        LIMIT 5
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
        results = list(query_job.result())

        if not results:
            return {"message": "No anomalies detected."}

        return {
            "anomalies": [
                {
                    "cost": row["cost"],
                    "z_score": round(row["z_score"], 2),
                    "age": row["age"]
                }
                for row in results
            ]
        }
