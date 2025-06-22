from typing import Any, List

from data_fetchers.data_fetcher_base import DataFetcherBase


class NewsDataFetcher(DataFetcherBase):

    def _format_for_prompt(self, data: Any):
        return data
