from agents.evaluator import EvaluatorAgent


def test_evaluator_basic():
    evaluator = EvaluatorAgent()
    insights = {"best_campaign_by_roas": "X"}
    creatives = [{"creative_type": "UGC"}]
    result = evaluator.evaluate(insights, creatives)
    assert "status" in result
