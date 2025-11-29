# Kasparro — Agentic Facebook Performance Analyst

This repository implements a modular agent-based system that analyzes Meta Ads performance for an undergarments brand. It generates insights, creative recommendations, and a validation trace.

---

## Quick Start
```bash
python -V  # should be >= 3.10
python -m venv .venv
.venv\Scripts\activate        # Windows
# or
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python src/run.py "Analyze ROAS drop in last 7 days"
```

---

## Data
Dataset used: `data/synthetic_fb_ads_undergarments.csv`  
Sample dataset for faster execution: `data/sample_fb_ads.csv`

Contains campaign details including:
- impressions
- clicks
- spend
- revenue
- ROAS
- CTR
- platform
- creative type
- audience type
- country

Insights are generated directly from this dataset.

---

## Config
Config settings in `config/config.yaml`:
```yaml
python: "3.10"
random_seed: 42
confidence_min: 0.6
use_sample_data: false
sample_fraction: 0.3
data_path_full: "data/synthetic_fb_ads_undergarments.csv"
data_path_sample: "data/sample_fb_ads.csv"
```

---

## Repo Map
```
├── config/
├── data/
│   ├── synthetic_fb_ads_undergarments.csv
│   ├── sample_fb_ads.csv
├── logs/
│   ├── pipeline_trace.json
├── reports/
│   ├── report.md
│   ├── insights.json
│   ├── creatives.json
├── src/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── analyst.py
│   │   ├── evaluator.py
│   ├── run.py
├── tests/
│   ├── test_evaluator.py
├── agent_graph.md
```

---

## Run
```bash
python src/run.py "Analyze ROAS drop"
python src/run.py "Suggest creatives for low CTR"
```

---

## Outputs
The agent pipeline generates three files:
- `reports/insights.json`
- `reports/creatives.json`
- `reports/report.md`

Example insight structure:
```json
{"metric": "roas", "change": "decrease", "reason": "CTR dropped; CPC rising"}
```

---

## Observability
A structured JSON trace is created at:
- `logs/pipeline_trace.json`

Trace includes:
- user query
- loaded config
- evaluation verdict

Framework easily extends to agent-level monitoring.

---

## Release
Assignment submission build: `v1.0`  
Repo link: https://github.com/Killada-Neeraja/kasparro-agentic-fb-analyst-neeraja

---

## Self-Review
Included inside the Pull Request:
- Design choices
- Trade-offs
- Suggested improvements
