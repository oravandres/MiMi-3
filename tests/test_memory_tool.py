"""MemoryTool round‑trip tests."""
from ma_framework.database import init_db, SessionLocal
from ma_framework.crud import create_role, create_agent, create_model, create_project, create_task
from ma_framework.tools.memory import MemoryTool

def test_memory_tool_roundtrip():
    init_db()
    with SessionLocal() as db:
        role = create_role(db, name="MemRole")
        model = create_model(db, name="llama3")
        agent = create_agent(db, name="MemAgent", role=role, models_=[model])
        project = create_project(db, name="MemProject", goal="Testing")
        task = create_task(db, project=project, title="MemTask")

        mem = MemoryTool(db)
        mem.save(agent_id=agent.id, task_id=task.id, content="Hello memory!")
        mem.save(agent_id=agent.id, task_id=task.id, content="Second message")

        recall = mem.recall(agent_id=agent.id, task_id=task.id)
        assert recall[0] == "Second message"
        assert recall[-1] == "Hello memory!"
