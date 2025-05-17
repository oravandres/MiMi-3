"""Script that sets up a demo multi‑agent project and executes it."""
import typer
from crewai import Task as CrewTask, Crew
from sqlalchemy.orm import Session
from .database import init_db, SessionLocal
from .crud import (
    create_role,
    create_model,
    create_agent,
    create_project,
    create_task,
    create_tool,
)
from .agents.builder_agent import BuilderAgent
from .agents.reviewer_agent import ReviewerAgent
from .tools.memory import MemoryTool

cli = typer.Typer(help="Run demo project")

@cli.command()
def run() -> None:
    # ---------------------------------------------------------------------
    # Bootstrap DB + demo data
    # ---------------------------------------------------------------------
    init_db()
    with SessionLocal() as db:
        builder_role = create_role(db, name="Builder", description="Writes code")
        reviewer_role = create_role(db, name="Reviewer", description="Reviews code")

        llama = create_model(db, name="llama3", version="8b")
        qwen = create_model(db, name="qwen", version="72b")

        mem_tool = create_tool(db, name="Memory", type_="memory", description="Persistent memory tool")

        # Agents with multiple models & tool
        builder = create_agent(
            db,
            name="BuilderBot",
            role=builder_role,
            models_=[llama, qwen],
            tools=[mem_tool],
        )
        reviewer = create_agent(
            db,
            name="ReviewerBot",
            role=reviewer_role,
            models_=[qwen],
            tools=[mem_tool],
        )

        project = create_project(db, name="HelloWorld", goal="Generate and review Hello World code")

        task_build = create_task(
            db,
            project=project,
            title="Write hello world program",
            description="Create a hello world in Python and Rust",
            agents=[builder, reviewer],  # multiple agents
        )

        task_review = create_task(
            db,
            project=project,
            title="Review hello world program",
            description="Review for best practices and style",
            agents=[reviewer, builder],  # both agents can chime in
        )

        # -----------------------------------------------------------------
        # CrewAI Execution
        # -----------------------------------------------------------------
        # Convert DB tasks to CrewAI tasks
        crew_task_build = CrewTask(task_build.description, expected_output="hello_world.py and hello_world.rs")
        crew_task_review = CrewTask(task_review.description, expected_output="review.md")

        # Init runtime agents
        rt_builder = BuilderAgent(
            name="BuilderBot",
            role="software engineer",
            goal="Generate code",
            models=["llama3:8b", "qwen:72b"],
        )
        rt_reviewer = ReviewerAgent(
            name="ReviewerBot",
            role="software reviewer",
            goal="Review code",
            models=["qwen:72b"],
        )

        c = Crew(
            agents=[rt_builder, rt_reviewer],
            tasks=[crew_task_build, crew_task_review],
        )
        results = c.kickoff()
        print("=== RESULTS ===")
        for t, res in zip([task_build, task_review], results):
            print(f"{t.title}:\n{res}\n")

if __name__ == "__main__":
    cli()
