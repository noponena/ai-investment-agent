from abc import ABC
from typing import Any

from api_clients.data_providers.data_provider_base import DataProviderBase, ProviderType


class NewsProviderBase(DataProviderBase, ABC):
    _filter_keywords = []

    def _init(self) -> None:
        self._filter_keywords = self._io_manager.keywords

    def _filter_response(self, response: Any) -> Any:
        """
        Generic filtering of the fetched response to contain only relevant data.
        Override this method in the child class if more specific filtering is needed.
        """
        if not self._filter_keywords or not isinstance(response, list):
            return response

        def is_relevant(item):
            title = item.get("title", "").lower()
            return any(kw in title for kw in self._filter_keywords)

        filtered = [item for item in response if is_relevant(item)]
        filtered_out = len(response) - len(filtered)
        print(f"Filtered out {filtered_out} of {len(response)} entries (kept {len(filtered)})")
        return filtered

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.NEWS
