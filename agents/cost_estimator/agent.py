import os
from google.cloud import bigquery
from google.cloud import aiplatform
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

    # Enhanced query with more sophisticated analytics
    query = f"""
        WITH cost_stats AS (
            SELECT
                AVG(cost) AS avg_cost,
                APPROX_QUANTILES(cost, 2)[OFFSET(1)] AS median_cost,
                MIN(cost) AS min_cost,
                MAX(cost) AS max_cost,
                STDDEV(cost) AS std_dev,
                COUNT(*) as sample_size,
                AVG(insurance_paid) as avg_insurance_paid,
                AVG(member_paid) as avg_member_paid
            FROM `datasage-adk-v2.datasage_health.healthcare_costs`
            WHERE age BETWEEN {age_min} AND {age_max}
            AND LOWER(gender) = '{gender.lower()}'
            AND LOWER(region) = '{region.lower()}'
            AND LOWER(visit_type) = '{visit_type.lower()}'
        )
        SELECT 
            *,
            avg_insurance_paid / NULLIF(avg_cost, 0) as insurance_coverage_ratio,
            avg_member_paid / NULLIF(avg_cost, 0) as member_burden_ratio
        FROM cost_stats
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
        "max_cost": row.max_cost,
        "std_dev": row.std_dev,
        "sample_size": row.sample_size,
        "insurance_coverage_ratio": row.insurance_coverage_ratio,
        "member_burden_ratio": row.member_burden_ratio
    }