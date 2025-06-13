"""BuilderAgent specializing in code generation."""
from crewai import Task
from .base import MultiModelAgent

class BuilderAgent(MultiModelAgent):
    """Builds code artifacts."""

    def build(self, task: Task) -> str:
        return self.run(task)
