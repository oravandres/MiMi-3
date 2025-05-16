"""Unit tests for SQLAlchemy models integrity."""
from ma_framework import models
from ma_framework.database import init_db, SessionLocal

def test_create_role_and_agent():
    init_db()
    with SessionLocal() as db:
        role = models.Role(name="Tester")
        db.add(role)
        db.commit()
        db.refresh(role)

        agent = models.Agent(name="TestAgent", role=role)
        db.add(agent)
        db.commit()
        db.refresh(agent)

        assert agent.role_id == role.id
        assert agent in role.agents
