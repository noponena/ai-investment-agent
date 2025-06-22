from typing import Any

from data_fetchers.data_fetcher_base import DataFetcherBase


class PriceDataFetcher(DataFetcherBase):
    def _format_for_prompt(self, data: Any):
        return data
