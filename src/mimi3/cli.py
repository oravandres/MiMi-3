"""Typer CLI for quick DB operations."""
import typer
from .database import init_db, SessionLocal
from .crud import create_role, create_model, create_tool
from . import models

app = typer.Typer(help="MiMi-3 CLI")

@app.command()
def initdb() -> None:
    """Create DB schema."""
    init_db()
    typer.echo("✅ Database initialized.")

@app.command()
def role(name: str, description: str = "") -> None:
    with SessionLocal() as db:
        role = create_role(db, name=name, description=description or None)
        typer.echo(f"✅ Role {role.id}: {role.name}")

@app.command()
def model(name: str, version: str = "", description: str = "") -> None:
    with SessionLocal() as db:
        model = create_model(db, name=name, version=version or None, description=description or None)
        typer.echo(f"✅ Model {model.id}: {model.name}")

@app.command()
def tool(name: str, type_: str, description: str = "") -> None:
    with SessionLocal() as db:
        tool = create_tool(db, name=name, type_=type_, description=description)
        typer.echo(f"✅ Tool {tool.id}: {tool.name}")

if __name__ == "__main__":
    app()
