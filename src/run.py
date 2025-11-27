from agents.planner import PlannerAgent
from agents.analyst import AnalystAgent
from agents.evaluator import EvaluatorAgent


def main():
    planner = PlannerAgent()
    analyst = AnalystAgent()
    evaluator = EvaluatorAgent()

    # 1) Agent planning
    plan = planner.plan()
    print("📌 PLAN:")
    for i, step in enumerate(plan["steps"], start=1):
        print(f"{i}. {step}")

    # 2) Run analysis (creates insights & creatives)
    result = analyst.run()
    insights = result["insights"]
    creatives = result["creatives"]

    print("\n📊 INSIGHTS:")
    print(insights)

    print("\n🎨 CREATIVES:")
    for c in creatives:
        print("-", c.get("example_copy", ""))

    # 3) Evaluate final output
    evaluation = evaluator.evaluate(insights, creatives)
    print("\n📈 EVALUATION:")
    print(evaluation)


if __name__ == "__main__":
    main()
