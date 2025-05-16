"""CrewAI wrapper with multi‑model support."""
from typing import Sequence, Any
from crewai import Agent, Task
from ollama import Client as OllamaClient  # type: ignore
from ..settings import settings

_ollama = OllamaClient(host=settings.ollama_host)

class MultiModelAgent(Agent):
    """CrewAI Agent that can swap between multiple LLM backends."""

    def __init__(self, *args, models: Sequence[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.models = list(models or [settings.default_llm])

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _call_llm(self, prompt: str, model_name: str) -> str:
        """Call Ollama model and return completion text."""
        response = _ollama.generate(model=model_name, prompt=prompt, stream=False)
        return response["response"]

    def run(self, task: Task, *args: Any, **kwargs: Any) -> str:  # noqa: D401
        """Override Agent.run with first‑fit LLM execution."""
        prompt = task.compile_prompt(*args, **kwargs)
        for model_name in self.models:
            try:
                return self._call_llm(prompt, model_name=model_name)
            except Exception as exc:  # pragma: no cover
                # fallback to next model
                print(f"[{self.name}] ⚠️  Model {model_name} failed: {exc}")
                continue
        raise RuntimeError(f"No available models succeeded for {self.name}")
