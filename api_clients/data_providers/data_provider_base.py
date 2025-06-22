from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List

from api_clients.api_client_base import ApiClientBase


class ProviderType(Enum):
    NEWS = auto()
    PRICES = auto()


class DataProviderBase(ApiClientBase, ABC):

    def get(self, **kwargs) -> List[Dict[str, str]]:
        valid_response = True
        if self._demo_mode:
            raw = self._fetch_mock_data(**kwargs)
        else:
            raw = self._fetch(**kwargs)
            valid_response = self._is_valid_response(raw)

        if not valid_response:
            print(
                f"Data provider '{self.name}' did not give valid response. The response was: {raw}"
            )
            return []

        filtered = self._filter_response(raw)
        return self._format_response(filtered)

    @abstractmethod
    def _fetch(self, **kwargs) -> Any:
        """
        Unified fetch method for all data providers.
        Could fetch prices, news, or other types depending on the provider.
        """
        pass

    @abstractmethod
    def _fetch_mock_data(self, **kwargs) -> Any:
        """
        Fetch mock data for testing and demo purposes.
        """
        pass

    @abstractmethod
    def _is_valid_response(self, response: Any) -> bool:
        """
        Checks whether the received response is valid.
        """
        pass

    @abstractmethod
    def _filter_response(self, response: Any) -> Any:
        """
        Filter result to contain only relevant data.
        """
        pass

    @abstractmethod
    def _format_response(self, response: Any) -> List[Dict[str, str]]:
        """
        Format the fetched response into a standardized list of dicts.
        """
        pass

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        pass
