from abc import ABC, abstractmethod
from typing import Any, Dict, List

from api_clients.data_providers.data_provider_base import DataProviderBase


class DataFetcherBase(ABC):
    def __init__(self):
        self._apis: List[DataProviderBase] = []

    def get(self, api_kwargs: dict = None, **kwargs) -> List[Dict[str, str]]:
        """
        api_kwargs: Optional[Dict[DataProviderBase, Dict]] or {str: Dict}
        kwargs: Default args for all APIs if not in api_kwargs.
        """
        if not self._apis:
            raise ValueError("No APIs provided.")

        api_kwargs = api_kwargs or {}
        all_data = []
        for api in self._apis:
            # Use per-API kwargs if available, else fallback to common kwargs
            per_api_kwargs = api_kwargs.get(api.name, kwargs)
            data = api.get(**per_api_kwargs)
            formatted = self._format_for_prompt(data)
            all_data.extend(formatted)
        return all_data

    def add_apis(self, apis: List[DataProviderBase]) -> None:
        self._apis.extend(apis)

    def clear_apis(self) -> None:
        self._apis.clear()

    @abstractmethod
    def _format_for_prompt(self, data: Any):
        """Format fetched data as a string for prompt injection."""
        pass
