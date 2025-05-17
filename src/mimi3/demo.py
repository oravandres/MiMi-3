#!/usr/bin/env python3
"""Self-contained demo of the multi-agent framework using SQLite."""
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Set up SQLite database
DB_URL = "sqlite:///./demo.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define models (a simplified version)
Base = declarative_base()

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

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50))
    description = Column(Text)
    agents = relationship("Agent", secondary=agent_model_association, back_populates="models")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    agents = relationship("Agent", back_populates="role")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="agents")
    models = relationship("Model", secondary=agent_model_association, back_populates="agents")
    tasks = relationship("Task", secondary=task_agent_association, back_populates="agents")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")
    result = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")
    agents = relationship("Agent", secondary=task_agent_association, back_populates="tasks")

class Memory(Base):
    """Simple key‑value message log for agents per task."""
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    content = Column(Text, nullable=False)

# CRUD operations
def create_role(db, name, description=None):
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def create_model(db, name, version=None, description=None):
    model = Model(name=name, version=version, description=description)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def create_agent(db, name, role, models_=None, description=None):
    agent = Agent(name=name, role=role, description=description)
    if models_:
        agent.models = models_
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def create_project(db, name, goal):
    project = Project(name=name, goal=goal)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def create_task(db, project, title, description=None, agents=None):
    task = Task(project=project, title=title, description=description)
    if agents:
        task.agents = agents
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Memory tool
class MemoryTool:
    """Store and retrieve per‑task conversation memory."""
    def __init__(self, db):
        self.db = db

    def save(self, *, agent_id, task_id, content):
        entry = Memory(agent_id=agent_id, task_id=task_id, content=content, timestamp=datetime.datetime.now(datetime.UTC))
        self.db.add(entry)
        self.db.commit()

    def recall(self, *, agent_id, task_id, limit=20):
        q = (
            self.db.query(Memory)
            .filter_by(agent_id=agent_id, task_id=task_id)
            .order_by(Memory.timestamp.desc())
            .limit(limit)
        )
        return [m.content for m in q]

def run_demo():
    """Run a simple demonstration."""
    # Initialize the database
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    with SessionLocal() as db:
        # Create roles
        builder_role = create_role(db, name="Builder", description="Writes code")
        reviewer_role = create_role(db, name="Reviewer", description="Reviews code")
        
        # Create models
        llama_model = create_model(db, name="llama3", version="8b")
        phi_model = create_model(db, name="phi", version="3")
        
        # Create agents
        builder = create_agent(
            db, 
            name="CodeWriter", 
            role=builder_role,
            models_=[llama_model]
        )
        
        reviewer = create_agent(
            db, 
            name="CodeReviewer", 
            role=reviewer_role,
            models_=[phi_model]
        )
        
        # Create project and tasks
        project = create_project(
            db,
            name="Demo Project",
            goal="Build a simple Python app"
        )
        
        task1 = create_task(
            db,
            project=project,
            title="Write Hello World",
            description="Create a simple Hello World application",
            agents=[builder]
        )
        
        task2 = create_task(
            db,
            project=project,
            title="Review Hello World",
            description="Review the Hello World application",
            agents=[reviewer]
        )
        
        # Demonstrate memory tool usage
        memory = MemoryTool(db)
        memory.save(agent_id=builder.id, task_id=task1.id, content="Starting to write Hello World")
        memory.save(agent_id=builder.id, task_id=task1.id, content="Completed Hello World application")
        
        # Retrieve memories
        builder_memories = memory.recall(agent_id=builder.id, task_id=task1.id)
        print(f"Builder's memories for task '{task1.title}':")
        for mem in builder_memories:
            print(f"- {mem}")
        
        # Update task status
        task1.status = "completed"
        db.commit()
        
        # Print project summary
        print("\nProject Summary:")
        print(f"Project: {project.name} - {project.goal}")
        print(f"Tasks:")
        for task in project.tasks:
            print(f"- {task.title} ({task.status})")
            print(f"  Assigned to: {', '.join([a.name for a in task.agents])}")

if __name__ == "__main__":
    # Remove existing demo.db to start fresh
    if os.path.exists("demo.db"):
        os.remove("demo.db")
    
    # Run the demo
    run_demo() 