"""Integration smoke test (DB interactions only)."""
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
        role = create_role(db, name="MultiRole")
        models = [create_model(db, name=f"model{i}") for i in range(llm_count)]
        agent = create_agent(db, name="MultiAgent", role=role, models_=models)

        assert len(agent.models) == llm_count

        project = create_project(db, name="Demo", goal="Test Framework")
        task = create_task(db, project=project, title="DemoTask", agents=[agent])

        assert agent in task.agents
