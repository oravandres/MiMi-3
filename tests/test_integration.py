"""Integration smoke test (DB interactions only)."""
import uuid
import pytest
from ma_framework.database import init_db, SessionLocal
from ma_framework.crud import (
    create_role,
    create_model,
    create_agent,
    create_project,
    create_task,
)

@pytest.mark.parametrize("llm_count", [1, 2])
def test_agent_multimodel(llm_count):
    init_db()
    with SessionLocal() as db:
        # Use unique ID for each test run
        unique_id = str(uuid.uuid4())[:8]
        role = create_role(db, name=f"MultiRole-{llm_count}-{unique_id}")
        models = [create_model(db, name=f"model{i}-{unique_id}") for i in range(llm_count)]
        agent = create_agent(db, name=f"MultiAgent-{llm_count}-{unique_id}", role=role, models_=models)

        assert len(agent.models) == llm_count

        project = create_project(db, name=f"Demo-{llm_count}-{unique_id}", goal="Test Framework")
        task = create_task(db, project=project, title=f"DemoTask-{llm_count}-{unique_id}", agents=[agent])

        assert agent in task.agents
