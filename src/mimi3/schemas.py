"""Pydantic models for safe I/O."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ModelSchema(BaseModel):
    id: int
    name: str
    version: Optional[str]

    class Config:
        orm_mode = True

class ToolSchema(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True

class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class AgentSchema(BaseModel):
    id: int
    name: str
    role: RoleSchema
    models: List[ModelSchema]
    tools: List[ToolSchema]

    class Config:
        orm_mode = True

class TaskSchema(BaseModel):
    id: int
    title: str
    status: str
    agents: List[AgentSchema]

    class Config:
        orm_mode = True

class ProjectSchema(BaseModel):
    id: int
    name: str
    goal: str
    created_at: datetime
    tasks: List[TaskSchema]

    class Config:
        orm_mode = True
