from config.agent_executor import AgentExecutor
import json

if __name__ == "__main__":
    # Example input payload
    input_data = {
    "age_min": 0,
    "age_max": 100,
    "gender": "",
    "region": "",
    "visit_type": ""
}




    executor = AgentExecutor("task.yaml")
    results = executor.run(input_data)

    # Print results
    print("\n✅ Final Output from Multi-Agent System:\n")
    print(json.dumps(results, indent=2))
