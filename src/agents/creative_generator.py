import json

class CreativeGenerator:
    def __init__(self, llm_client, prompts_dir, config):
        self.llm_client = llm_client
        self.prompts_dir = prompts_dir
        self.config = config

    def generate_creatives(self, underperforming_ads, insights):
        """
        underperforming_ads: list of dicts with campaign/ad names and metrics
        insights: dict from InsightAgent.generate_insights
        """
        prompt = self._load_prompt("creative_prompt.md")

        payload = json.dumps({
            "underperforming_ads": underperforming_ads,
            "insights": insights.get("insights", [])
        })

        full_prompt = f"{prompt}\n\nDATA:\n{payload}"

        response = self.llm_client.generate(full_prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "ideas": [],
                "error": "Invalid JSON from LLM"
            }

        return result

    def _load_prompt(self, filename):
        with open(f"{self.prompts_dir}/{filename}", "r", encoding="utf-8") as f:
            return f.read()
