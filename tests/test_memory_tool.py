"""MemoryTool round‑trip tests."""
import uuid
from ma_framework.database import init_db, SessionLocal
from ma_framework.crud import create_role, create_agent, create_model, create_project, create_task
from ma_framework.tools.memory import MemoryTool

def test_memory_tool_roundtrip():
    init_db()
    with SessionLocal() as db:
        unique_id = str(uuid.uuid4())[:8]
        role = create_role(db, name=f"MemRole-{unique_id}")
        model = create_model(db, name=f"llama3-{unique_id}")
        agent = create_agent(db, name=f"MemAgent-{unique_id}", role=role, models_=[model])
        project = create_project(db, name=f"MemProject-{unique_id}", goal="Testing")
        task = create_task(db, project=project, title=f"MemTask-{unique_id}")

        mem = MemoryTool(db)
        mem.save(agent_id=agent.id, task_id=task.id, content="Hello memory!")
        mem.save(agent_id=agent.id, task_id=task.id, content="Second message")

        recall = mem.recall(agent_id=agent.id, task_id=task.id)
        assert recall[0] == "Second message"
        assert recall[-1] == "Hello memory!"
