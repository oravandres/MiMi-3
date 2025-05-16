"""CRUD helpers. Feel free to extend with advanced queries."""
from sqlalchemy.orm import Session
from . import models

# ---------- Role ---------------------------------------------------------

def create_role(db: Session, *, name: str, description: str | None = None) -> models.Role:
    role = models.Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

# ---------- Model --------------------------------------------------------

def create_model(db: Session, *, name: str, version: str | None = None, description: str | None = None) -> models.Model:
    model = models.Model(name=name, version=version, description=description)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

# ---------- Tool ---------------------------------------------------------

def create_tool(db: Session, *, name: str, type_: str, description: str = "", config: str | None = None) -> models.Tool:
    tool = models.Tool(name=name, type=type_, description=description, config=config)
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool

# ---------- Agent --------------------------------------------------------

def create_agent(
    db: Session,
    *,
    name: str,
    role: models.Role,
    models_: list[models.Model],
    tools: list[models.Tool] | None = None,
    description: str | None = None,
) -> models.Agent:
    agent = models.Agent(name=name, role=role, description=description)
    agent.models.extend(models_)
    if tools:
        agent.tools.extend(tools)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

# ---------- Project & Task ----------------------------------------------

def create_project(db: Session, *, name: str, goal: str) -> models.Project:
    project = models.Project(name=name, goal=goal)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def create_task(
    db: Session,
    *,
    project: models.Project,
    title: str,
    description: str | None = None,
    agents: list[models.Agent] | None = None,
) -> models.Task:
    task = models.Task(title=title, description=description, project=project)
    if agents:
        task.agents.extend(agents)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
