# MiMi-3: Multi-Model Multi-Agent Framework

A minimal, opinionated framework for building software-engineering agents.

## Overview

MiMi-3 (Multi-Model, Multi-Agent) is a framework designed to help you build and manage teams of AI agents. Each agent can use one or more language models, and you can organize agents into projects and assign them tasks.

## Features

- Multi-model support: Assign different LLMs to different agents
- Database-backed persistence: Store agent states, tasks, and conversations
- Role-based design: Create specialized agent roles 
- Memory system: Agents can store and recall information
- SQLite support for development, PostgreSQL for production

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MiMi-3.git
cd MiMi-3
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Quick Start

Run the demo to see how the framework works:

```bash
python -m src.mimi3.demo
```

This will:
- Create a SQLite database
- Set up roles (Builder, Reviewer)
- Create agents with different models
- Create a project with tasks
- Demonstrate the memory system

## Running Tests

The project includes tests that verify the functionality of the framework:

```bash
python -m pytest -v
```

## Project Structure

```
MiMi-3/
├── src/
│   └── mimi3/           # Main package
│       ├── agents/             # Agent implementations
│       ├── tools/              # Tools for agents to use
│       ├── models.py           # SQLAlchemy models
│       ├── schemas.py          # Pydantic schemas
│       ├── crud.py             # Database operations
│       ├── database.py         # Database connection
│       └── demo.py             # Demo application
│
├── tests/                      # Test directory
│   ├── test_models.py          # Database model tests
│   ├── test_memory_tool.py     # Memory tool tests
│   └── test_integration.py     # Integration tests
│
├── setup.py                    # Package setup
└── requirements.txt            # Dependencies
```

## Configuration

For production use, create a `.env` file based on these settings:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
OLLAMA_HOST=http://localhost:11434
DEFAULT_LLM=llama3:8b
```

## Development Environment

During development and testing, the framework uses SQLite by default.

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
python -m src.mimi3.cli initdb     # Migrate schema
python -m src.mimi3.sample_project # Run demo workflow
```

## Docker Setup

This project includes Docker support for running both the application and PostgreSQL database.

### Running with Docker Compose

1. Start the services:
```bash
docker-compose up -d
```

2. To run only the PostgreSQL database (for local development):
```bash
docker-compose up -d postgres
```

3. Access PostgreSQL from your local machine:
```bash
psql -h localhost -U postgres -d mimi3
```
(Password: postgres)

4. Stop all services:
```bash
docker-compose down
```

5. To remove all data volumes:
```bash
docker-compose down -v
```

*Generated on 2025-05-16T12:17:40 UTC.*
