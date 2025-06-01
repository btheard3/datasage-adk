import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def run_cost_estimator(inputs):
    key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.secrets', 'creds.json'))
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    age_min = inputs.get("age_min", 0)
    age_max = inputs.get("age_max", 100)
    gender = inputs.get("gender", "")
    region = inputs.get("state", "")
    visit_type = inputs.get("visit_type", "")

    query = f"""
        SELECT
            AVG(cost) AS avg_cost,
            APPROX_QUANTILES(cost, 2)[OFFSET(1)] AS median_cost,
            MIN(cost) AS min_cost,
            MAX(cost) AS max_cost
        FROM `datasage-adk-v2.datasage_health.healthcare_costs`
        WHERE age BETWEEN {age_min} AND {age_max}
        AND LOWER(gender) = '{gender.lower()}'
        AND LOWER(region) = '{region.lower()}'
        AND LOWER(visit_type) = '{visit_type.lower()}'
    """

    job = client.query(query)
    rows = list(job.result())
    if not rows or rows[0].avg_cost is None:
        return {"avg_cost": 0, "median_cost": 0, "min_cost": 0, "max_cost": 0}

    row = rows[0]
    return {
        "avg_cost": row.avg_cost,
        "median_cost": row.median_cost,
        "min_cost": row.min_cost,
        "max_cost": row.max_cost
    }
