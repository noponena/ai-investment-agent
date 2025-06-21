from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MarketDataAPI(ABC):
    def __init__(self, api_key: str, demo_mode: bool = False):
        self.api_key = api_key
        self.demo_mode = demo_mode
        if not self.api_key:
            raise ValueError("api key not set")

    def get_news(self, **kwargs) -> Any:
        news = self._do_get_news(**kwargs)
        return self._format_response(news)

    @abstractmethod
    def _do_get_news(self, **kwargs) -> Any:
        """Fetches and returns a list of market news headlines or summaries."""
        pass

    @staticmethod
    @abstractmethod
    def _format_response(response: Any) -> List[Dict[str, str]]:
        """Formats the response."""
        return response
