from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AIAgent(ABC):
    @abstractmethod
    def prompt_model(self, prompt: str, model: str) -> str:
        """Send a prompt to the LLM and return the generated text."""
        pass

    @abstractmethod
    def get_recommendations(self, prompt: str, model: str) -> List[Dict[str, str]]:
        """Process the model's response and return structured recommendations."""
        pass

    @abstractmethod
    def summarize_market_headlines(self, headlines: List[str], model: str = "default") -> str:
        """Summarize market headlines using the LLM."""
        pass
