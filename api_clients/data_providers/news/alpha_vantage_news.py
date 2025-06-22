import copy
from typing import Any, Dict, List, Optional

from api_clients.data_providers.news.news_provider_base import NewsProviderBase
from api_clients.data_providers.utils import is_alpha_vantage_valid_response
from io_utils.io_manager import IOManager


class AlphaVantageNewsAPI(NewsProviderBase):
    _name = "AlphaVantageNews"
    _demo_url: str = (
        "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers="
        "COIN,CRYPTO:BTC,FOREX:USD&time_from=20220410T0130&limit=1000&apikey=demo"
    )

    def _fetch(self, **kwargs) -> Any:
        topics: Optional[List[str]] = kwargs.get("topics", None)
        if topics:
            if isinstance(topics, str):
                topics = [topics]
        else:
            topics = []

        limit_per_topic: int = int(kwargs.get("limit", 10))
        total_limit: int = int(kwargs.get("total_limit", 10))

        other_kwargs = copy.deepcopy(kwargs)
        other_kwargs.pop("topics", None)

        raw_news = self._gather_news_for_topics(topics, limit_per_topic, other_kwargs)
        return raw_news[:total_limit]

    def _fetch_mock_data(self, **kwargs) -> Any:
        return self._send_request(self._demo_url)

    def _format_response(self, response: Any) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        for item in response:
            result.append(
                {
                    "title": item.get("title", ""),
                    "summary": item.get("summary", "")[:200],
                }
            )
        return result

    def _gather_news_for_topics(
        self,
        topics: List[Optional[str]],
        limit_per_topic: int,
        other_kwargs: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        seen_titles: set = set()
        all_news: List[Dict[str, Any]] = []
        for topic in topics:
            news_items = self._fetch_for_topic(topic, other_kwargs)
            for item in news_items[:limit_per_topic]:
                title = item.get("title", "")
                if title and title not in seen_titles:
                    all_news.append(item)
                    seen_titles.add(title)
        return all_news

    def _fetch_for_topic(
        self, topic: Optional[str], other_kwargs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        url = self._build_news_url(topic, other_kwargs)
        return self._send_request(url)

    def _build_news_url(self, topic: Optional[str], params: Dict[str, Any]) -> str:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={self._api_key}"
        if "tickers" in params and params["tickers"]:
            url += f"&tickers={','.join(params['tickers'])}"
        if topic:
            url += f"&topics={topic}"
        if "limit" in params and params["limit"]:
            url += f"&limit={int(params['limit'])}"
        if "sort" in params and params["sort"]:
            url += f"&sort={params['sort']}"
        if "time_from" in params and params["time_from"]:
            url += f"&time_from={params['time_from']}"
        if "time_to" in params and params["time_to"]:
            url += f"&time_to={params['time_to']}"
        return url

    def _send_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        data = super()._send_request(url, method, headers, params, **kwargs)
        if isinstance(data, dict):
            return data.get("feed", [])
        else:
            return []

    def _is_valid_response(self, response: Any) -> bool:
        return is_alpha_vantage_valid_response(response)


def main():
    io = IOManager()
    api_key = io.read_api_key("ALPHA_VANTAGE_API_KEY")
    data_provider = AlphaVantageNewsAPI(api_key=api_key, demo_mode=False)

    res = data_provider.get(
        topics=["financial_markets", "economy_macro", "economy_monetary", "technology"],
        limit=10,
        total_limit=50,
        sort="LATEST",
    )

    for title in res:
        print(title)


if __name__ == "__main__":
    main()
