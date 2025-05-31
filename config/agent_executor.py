import yaml

class AgentExecutor:
    def __init__(self, task_config_path: str):
        with open(task_config_path, "r") as f:
            self.task_config = yaml.safe_load(f)

    def run(self, inputs: dict) -> dict:
        results = {}
        for step in self.task_config["steps"]:
            name = step["id"]
            module_path = step["module"]
            function_name = step["function"]
            uses = step.get("uses", [])

            # Load function dynamically
            parts = module_path.split(".")
            module = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
            agent_module = getattr(module, parts[-1])
            func = getattr(agent_module, function_name)

            # Prepare input
            kwargs = inputs.copy()
            for use in uses:
                kwargs[use] = results.get(use)

            results[name] = func(**kwargs)

        return results
