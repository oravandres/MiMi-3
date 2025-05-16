# Multi‑Agent / Multi‑Model Framework

A minimal, opinionated boilerplate for building **software‑engineering agents** powered by
**CrewAI**, **Ollama** LLMs, and backed by **PostgreSQL**.

## Entities

| Entity  | Purpose |
|---------|---------|
| **Model**  | LLM or specialist model (e.g., `llama3`, `qwen:72b`). |
| **Role**   | Defines responsibility (Builder, Reviewer…). |
| **Agent**  | Runtime actor – can leverage _multiple_ models and tools. |
| **Tool**   | Extend agents with capabilities (e.g., persistent memory). |
| **Project**| High‑level goal and collection of tasks. |
| **Task**   | Unit of work that can be solved by _one or more_ agents. |

## Quick‑Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                  # Adjust DATABASE_URL
python -m ma_framework.cli initdb     # Migrate schema
python -m ma_framework.sample_project # Run demo workflow
```

*Generated on 2025-05-16T12:17:40 UTC.*
