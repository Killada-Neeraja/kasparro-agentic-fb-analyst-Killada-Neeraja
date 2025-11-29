import sys
import json
from pathlib import Path

import yaml

from agents.planner import PlannerAgent
from agents.analyst import AnalystAgent
from agents.evaluator import EvaluatorAgent


CONFIG_PATH = Path("config/config.yaml")


def load_config():
    # Default values if config file is missing
    config = {
        "python": "3.10",
        "random_seed": 42,
        "confidence_min": 0.6,
        "use_sample_data": False,
        "sample_fraction": 0.3,
    }
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open() as f:
            loaded = yaml.safe_load(f) or {}
            config.update(loaded)
    return config


def main():
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Analyze overall performance"

    config = load_config()

    print("\n=== Kasparro Agentic FB Analyst ===")
    print("User query:", user_query)
    print("Config:", config)

    planner = PlannerAgent()
    analyst = AnalystAgent()
    evaluator = EvaluatorAgent(config=config)


    print("\n[PLAN]")
    for step in planner.plan()["steps"]:
        print(" -", step)

    print("\n[ANALYST] Running analysis...")
    result = analyst.run()
    insights = result["insights"]
    creatives = result["creatives"]

    print("\nINSIGHTS:")
    print(insights)

    print("\nCREATIVES:")
    for c in creatives:
        print("-", c.get("example_copy", ""))

    print("\n[EVALUATOR] Evaluating with confidence_min =", config["confidence_min"])
    evaluation = evaluator.evaluate(insights)
    print("Evaluation:", evaluation)

    # Simple observability trace
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    with (logs_dir / "pipeline_trace.json").open("w") as f:
        json.dump(
            {
                "query": user_query,
                "config": config,
                "evaluation": evaluation,
            },
            f,
            indent=4,
        )

    print("\n✅ Pipeline completed. Outputs in /reports and /logs.")


if __name__ == "__main__":
    main()
