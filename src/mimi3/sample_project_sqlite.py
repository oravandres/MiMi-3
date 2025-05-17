#!/usr/bin/env python3
"""Sample MiMi-3 project demonstrating the multi-agent framework.

This version uses SQLite instead of PostgreSQL for demonstration.
"""
import os
from sqlalchemy.orm import Session
from . import models
from .database import init_db, SessionLocal
from .crud import (
    create_role,
    create_model,
    create_agent,
    create_project,
    create_task,
)
from .tools.memory import MemoryTool

def run():
    """Set up a sample project with agents and run a simple sequence."""
    # Use SQLite for testing
    os.environ["TESTING"] = "True"
    
    # ---------------------------------------------------------------------
    # Bootstrap DB + demo data
    # ---------------------------------------------------------------------
    init_db()
    with SessionLocal() as db:
        builder_role = create_role(db, name="Builder", description="Writes code")
        reviewer_role = create_role(db, name="Reviewer", description="Reviews code")
        
        llama_model = create_model(db, name="llama3", version="8b")
        phi_model = create_model(db, name="phi", version="3")
        
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
    run() 