"""ReviewerAgent specialising in code review."""
from crewai import Task
from .base import MultiModelAgent

class ReviewerAgent(MultiModelAgent):
    """Reviews code artifacts."""

    def review(self, task: Task) -> str:
        return self.run(task)
