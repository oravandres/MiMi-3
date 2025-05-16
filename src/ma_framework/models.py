"""SQLAlchemy domain models (v2 declarative)."""
from __future__ import annotations
import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association tables ------------------------------------------------------

agent_model_association = Table(
    "agent_model_association",
    Base.metadata,
    Column("agent_id", ForeignKey("agents.id"), primary_key=True),
    Column("model_id", ForeignKey("models.id"), primary_key=True),
)

task_agent_association = Table(
    "task_agent_association",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("agent_id", ForeignKey("agents.id"), primary_key=True),
)

agent_tool_association = Table(
    "agent_tool_association",
    Base.metadata,
    Column("agent_id", ForeignKey("agents.id"), primary_key=True),
    Column("tool_id", ForeignKey("tools.id"), primary_key=True),
)

# Core tables -------------------------------------------------------------

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50))
    description = Column(Text)

    agents = relationship("Agent", secondary=agent_model_association, back_populates="models")

    def __repr__(self) -> str:  # pragma: no cover
        v = f":{self.version}" if self.version else ""
        return f"<Model {self.name}{v}>"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    agents = relationship("Agent", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Role {self.name}>"

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text)
    config = Column(Text)

    agents = relationship("Agent", secondary=agent_tool_association, back_populates="tools")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Tool {self.name}>"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="agents")
    models = relationship("Model", secondary=agent_model_association, back_populates="agents")
    tools = relationship("Tool", secondary=agent_tool_association, back_populates="agents")
    tasks = relationship("Task", secondary=task_agent_association, back_populates="agents")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Agent {self.name}>"

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Project {self.name}>"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")

    agents = relationship("Agent", secondary=task_agent_association, back_populates="tasks")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Task {self.title} ({self.status})>"

class Memory(Base):
    """Simple key‑value message log for agents per task."""
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text, nullable=False)
