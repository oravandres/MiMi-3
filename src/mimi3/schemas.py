"""Pydantic models for safe I/O."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ModelSchema(BaseModel):
    id: int
    name: str
    version: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ToolSchema(BaseModel):
    id: int
    name: str
    type: str

    model_config = ConfigDict(from_attributes=True)

class RoleSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class AgentSchema(BaseModel):
    id: int
    name: str
    role: RoleSchema
    models: List[ModelSchema]
    tools: List[ToolSchema]

    model_config = ConfigDict(from_attributes=True)

class TaskSchema(BaseModel):
    id: int
    title: str
    status: str
    agents: List[AgentSchema]

    model_config = ConfigDict(from_attributes=True)

class ProjectSchema(BaseModel):
    id: int
    name: str
    goal: str
    created_at: datetime
    tasks: List[TaskSchema]

    model_config = ConfigDict(from_attributes=True)
