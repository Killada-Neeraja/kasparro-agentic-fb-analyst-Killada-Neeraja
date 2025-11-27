import sys
import json
from pathlib import Path

from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.creative_generator import CreativeGeneratorAgent
from agents.evaluator import EvaluatorAgent


def main():
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Analyse overall ROAS performance"

    print("\n=== Kasparro Agentic FB Analyst ===")
    print("User query:", user_query)

    planner = PlannerAgent()
    data_agent = DataAgent()
    insight_agent = InsightAgent()
    creative_agent = CreativeGeneratorAgent()
    evaluator = EvaluatorAgent()

    plan = planner.plan()
    print("\n[PLAN]")
    for step in plan["steps"]:
        print(" -", step)

    print("\n[DATA AGENT] Loading dataset...")
    df = data_agent.load()
    print(f"Loaded {len(df)} rows.")

    print("\n[INSIGHT AGENT] Generating insights & hypothesis...")
    analysis = insight_agent.generate(df)
    insights = analysis["insights"]
    roas_hypothesis = analysis["roas_hypothesis"]

    print("Insights:", insights)
    print("ROAS hypothesis:", roas_hypothesis)

    print("\n[CREATIVE AGENT] Generating creatives...")
    creatives = creative_agent.generate(insights, roas_hypothesis)

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    with (reports_dir / "insights.json").open("w") as f:
        json.dump(
            {
                "insights": insights,
                "roas_hypothesis": roas_hypothesis,
                "user_query": user_query,
            },
            f,
            indent=4,
        )

    with (reports_dir / "creatives.json").open("w") as f:
        json.dump(creatives, f, indent=4)

    print("\n[EVALUATOR] Evaluating pipeline output...")
    evaluation = evaluator.evaluate(insights, creatives)
    with (reports_dir / "evaluation.json").open("w") as f:
        json.dump(evaluation, f, indent=4)
    print("Evaluation:", evaluation)

    # Optional: simple trace log
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    with (logs_dir / "pipeline_trace.json").open("w") as f:
        json.dump(
            {
                "query": user_query,
                "plan": plan,
                "evaluation": evaluation,
            },
            f,
            indent=4,
        )

    print("\n✅ Pipeline completed. Outputs in /reports and /logs.")


if __name__ == "__main__":
    main()
