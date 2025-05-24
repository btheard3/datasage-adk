from google.cloud import bigquery

class InsightGeneratorAgent:
    def __init__(self):
        self.client = bigquery.Client()

    def generate(self, age_min: int, age_max: int, gender: str, visit_type: str, region: str) -> dict:
        query = """
        SELECT
            visit_type,
            region,
            gender,
            COUNT(*) AS visit_count,
            ROUND(AVG(cost), 2) AS avg_cost,
            ROUND(MIN(cost), 2) AS min_cost,
            ROUND(MAX(cost), 2) AS max_cost
        FROM `datasage-adk-v2.datasage_health.healthcare_costs`
        WHERE age BETWEEN @age_min AND @age_max
            AND gender = @gender
            AND visit_type = @visit_type
            AND region = @region
        GROUP BY visit_type, region, gender
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
            return {"message": "No matching insights found."}

        row = results[0]
        return {
            "avg_cost": row["avg_cost"],
            "min_cost": row["min_cost"],
            "max_cost": row["max_cost"],
            "visit_count": row["visit_count"],
            "insight": (
                f"For {gender}s aged {age_min}-{age_max} in {region} visiting for {visit_type}, "
                f"there were {row['visit_count']} visits. "
                f"Avg cost: ${row['avg_cost']}, Min: ${row['min_cost']}, Max: ${row['max_cost']}."
            )
        }

