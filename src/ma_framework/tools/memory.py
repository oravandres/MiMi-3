"""Simple persistent memory tool for agents."""
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models

class MemoryTool:
    """Store and retrieve per‑task conversation memory."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def save(self, *, agent_id: int, task_id: int, content: str) -> None:
        entry = models.Memory(agent_id=agent_id, task_id=task_id, content=content, timestamp=datetime.utcnow())
        self.db.add(entry)
        self.db.commit()

    def recall(self, *, agent_id: int, task_id: int, limit: int = 20) -> list[str]:
        q = (
            self.db.query(models.Memory)
            .filter_by(agent_id=agent_id, task_id=task_id)
            .order_by(models.Memory.timestamp.desc())
            .limit(limit)
        )
        return [m.content for m in q]
