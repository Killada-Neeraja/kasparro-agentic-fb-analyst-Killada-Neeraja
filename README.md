# Kasparro — Agentic Facebook Performance Analyst

## Quick Start
```bash
python -V  # ensure Python >= 3.10
pip install pandas
python src/run.py

## Data


## Config
Edit `config/config.yaml`:

```yaml
python: "3.10"
random_seed: 42
confidence_min: 0.6
use_sample_data: false
sample_fraction: 0.3




## Repo Map
src/
 ├─ run.py                  → Runs the full pipeline
 └─ agents/
     ├─ planner.py         → Defines the task plan/steps
     ├─ analyst.py         → Loads CSV, generates insights & creatives
     ├─ evaluator.py       → Validates outputs & saves evaluation results

data/
 └─ synthetic_fb_ads_undergarments.csv  → Input dataset
reports/
 ├─ insights.json          → Best campaign/platform/country/creative type
 ├─ creatives.json         → Recommended messaging for ads
 └─ report.md              → Final human-readable summary
logs/                      → Placeholder for future logging
tests/                     → Placeholder for future tests
prompts/                   → Placeholder for LLM prompts

## Run
python src/run.py

## Outputs
The agent pipeline generates three files:
reports/insights.json
reports/creatives.json
reports/report.md

## Observability
- A JSON trace of each run is written to `logs/pipeline_trace.json`.
- Langfuse is not integrated in this version, but the logs structure can be extended to external tools.


## Release
Version: v1.0 — Final Assignment Submission
Core features implemented
Automatic pipeline generation complete


## Self-Review
- Verified that the agent pipeline (Planner → Analyst → Evaluator) runs end-to-end.
- Confirmed that `reports/insights.json`, `reports/creatives.json` and `reports/evaluation.json` are generated.
- Ensured the structure matches the provided template (src/, data/, config/, logs/, reports/, prompts/, tests/).
- Identified future improvements: deeper config usage, real LLM prompts, Langfuse integration and unit tests.

