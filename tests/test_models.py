"""Unit tests for SQLAlchemy models integrity."""
import uuid
from mimi3 import models
from mimi3.database import init_db, SessionLocal

def test_create_role_and_agent():
    init_db()
    with SessionLocal() as db:
        unique_id = str(uuid.uuid4())[:8]
        role = models.Role(name=f"Tester-{unique_id}")
        db.add(role)
        db.commit()
        db.refresh(role)

        agent = models.Agent(name=f"TestAgent-{unique_id}", role=role)
        db.add(agent)
        db.commit()
        db.refresh(agent)

        assert agent.role_id == role.id
        assert agent in role.agents
