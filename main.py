# main.py

from agents.ingestor import IngestorAgent
from agents.cleaner import CleanerAgent
from agents.analyst import AnalystAgent
from agents.insight import InsightAgent
from agents.presenter import PresenterAgent

# Initialize all agents
ingestor = IngestorAgent(name="IngestorAgent")
cleaner = CleanerAgent(name="CleanerAgent")
analyst = AnalystAgent(name="AnalystAgent")
insight = InsightAgent(name="InsightAgent")
presenter = PresenterAgent(name="PresenterAgent")

# Step 1: Ingest data from BigQuery
print("\n🟢 Step 1: Ingesting data from BigQuery...\n")
ingest_result = ingestor.run({
    "query": """
        SELECT name, SUM(number) as total
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state = 'TX'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 5
    """
})
records = ingest_result["records"]

# Step 2: Clean data
print("\n🟢 Step 2: Cleaning data...\n")
clean_result = cleaner.run({"records": records})
cleaned_records = clean_result["records"]

# Step 3: Analyze cleaned data
print("\n🟢 Step 3: Analyzing data...\n")
analysis_result = analyst.run({"records": cleaned_records})
insights = analysis_result["insights"]

# Step 4: Generate insight summary
print("\n🟢 Step 4: Generating summary...\n")
summary_result = insight.run({"insights": insights})
summary = summary_result["summary"]

# Step 5: Present final report
print("\n🟢 Step 5: Building final report...\n")
report_result = presenter.run({
    "records": cleaned_records,
    "summary": summary
})

print("\n✅ Final Multi-Agent Report:\n")
print(report_result["report"])
