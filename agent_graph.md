# Agent Graph — Kasparro FB Ads Analyst

This document explains the agent architecture and data flow of this project.

---

## High-Level Flow

1️⃣ **Planner Agent**
- Input: User query (e.g., "Analyze ROAS drop in last 7 days")
- Output: Structured analysis plan (JSON)
- Responsibilities:
  - Determine metrics to analyze
  - Decide campaign grouping and time ranges
  - Pass instructions to next agents

2️⃣ **Data Agent** (will be separated from Analyst in refactor)
- Input: JSON plan + dataset path
- Output: Aggregated performance metrics
- Responsibilities:
  - Load dataset based on config
  - Summarize ROAS, CTR, CPC by campaign/adset

3️⃣ **Insight Agent**
- Input: Data summaries + plan details
- Output: Insights JSON with confidence scoring
- Responsibilities:
  - Extract high/low performing patterns
  - Rank insights by impact severity

4️⃣ **Evaluator Agent**
- Input: Insights JSON
- Output: QA result (pass/fail) + issues list
- Responsibilities:
  - Check confidence thresholds
  - Validate presence of impactful insights

5️⃣ **Creative Generator Agent**
- Input: Underperforming campaigns + insights
- Output: New creative suggestions (JSON)
- Responsibilities:
  - Recommend improved messaging (WIP)

---

## Agent Flow Diagram (Mermaid)

```mermaid
flowchart LR
    A[User Query] --> P[Planner Agent]
    P --> D[Data Agent]
    D --> I[Insight Agent]
    I --> E[Evaluator Agent]
    E -- pass --> C[Creative Generator]
    E -- fail --> P
    C --> R[Reports]
