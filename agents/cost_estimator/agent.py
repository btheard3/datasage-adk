import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

def run(**kwargs):
    load_dotenv()

    # Load service account credentials
    key_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '.secrets', 'creds.json')
    )
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Extract input parameters
    age_min = kwargs.get("age_min", 0)
    age_max = kwargs.get("age_max", 100)
    gender = kwargs.get("gender", "").lower()
    region = kwargs.get("region", "").lower()
    visit_type = kwargs.get("visit_type", "").lower()

    # Build dynamic WHERE clause
    conditions = [f"age BETWEEN {age_min} AND {age_max}"]
    if gender:
        conditions.append(f"LOWER(gender) = '{gender}'")
    if region:
        conditions.append(f"LOWER(region) = '{region}'")
    if visit_type:
        conditions.append(f"LOWER(visit_type) = '{visit_type}'")

    where_clause = " AND ".join(conditions)

    # Build query string
    query = f"""
        SELECT
            AVG(cost) AS avg_cost,
            APPROX_QUANTILES(cost, 2)[OFFSET(1)] AS median_cost,
            MIN(cost) AS min_cost,
            MAX(cost) AS max_cost
        FROM `datasage-adk-v2.datasage_health.healthcare_costs`
        WHERE {where_clause}
    """

    print("QUERY BEING RUN:\n", query)

    # Execute query
    job_config = bigquery.QueryJobConfig(use_query_cache=True)
    query_job = client.query(query, job_config=job_config)
    rows = list(query_job.result())

    if not rows:
        return {
            "avg_cost": 0.0,
            "median_cost": 0.0,
            "min_cost": 0.0,
            "max_cost": 0.0,
        }

    row = rows[0]
    return {
        "avg_cost": row["avg_cost"] or 0.0,
        "median_cost": row["median_cost"] or 0.0,
        "min_cost": row["min_cost"] or 0.0,
        "max_cost": row["max_cost"] or 0.0,
    }

