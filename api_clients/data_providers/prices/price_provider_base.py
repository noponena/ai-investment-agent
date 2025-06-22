from abc import ABC
from typing import Any

from api_clients.data_providers.data_provider_base import DataProviderBase, ProviderType


class PriceProviderBase(DataProviderBase, ABC):
    _filter_keywords = []

    def _init(self) -> None:
        pass

    def _filter_response(self, response: Any) -> Any:
        """
        No filtering for price data.
        """
        return response

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.PRICES
