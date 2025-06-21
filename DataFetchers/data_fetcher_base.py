from abc import ABC, abstractmethod


class DataFetcher(ABC):
    @abstractmethod
    def fetch(self):
        """Fetch and return data (as a dict, list, or string)."""
        pass

    @abstractmethod
    def format_for_prompt(self, data):
        """Format fetched data as a string for prompt injection."""
        pass
