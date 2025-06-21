import copy
from typing import Any, Dict, List, Optional

import requests
from market_data_api import MarketDataAPI

from io_manager import IOManager


class AlphaVantageAPI(MarketDataAPI):

    demo_url: str = (
        "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers="
        "COIN,CRYPTO:BTC,FOREX:USD&time_from=20220410T0130&limit=1000&apikey=demo"
    )

    def _do_get_news(self, **kwargs) -> Any:
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

        if self.demo_mode:
            raw_news: List[Dict[str, Any]] = self._fetch_demo_response()
        else:
            raw_news = self._gather_news_for_topics(topics, limit_per_topic, other_kwargs)
        return raw_news[:total_limit]

    @staticmethod
    def _format_response(response: Any) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        for item in response:
            result.append({
                "title": item.get("title", ""),
                "summary": item.get("summary", "")[:200]
            })
        return result

    def _gather_news_for_topics(
        self, topics: List[Optional[str]], limit_per_topic: int, other_kwargs: Dict[str, Any]
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

    def _fetch_for_topic(self, topic: Optional[str], other_kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        url = self._build_news_url(topic, other_kwargs)
        return self._send_request(url)

    def _build_news_url(self, topic: Optional[str], params: Dict[str, Any]) -> str:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={self.api_key}"
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

    def _fetch_demo_response(self) -> List[Dict[str, Any]]:
        return self._send_request(self.demo_url)

    @staticmethod
    def _send_request(url: str) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("feed", [])
        except Exception as e:
            print(f"Error fetching data from AlphaVantage: {e}")
            return []


def main():
    io = IOManager("C:/Aaro/Projects/Personal/AI Investment Agent/settings.yaml")
    api_key = io.read_api_key("ALPHA_VANTAGE_API_KEY")
    av = AlphaVantageAPI(api_key, demo_mode=True)

    res = av.get_news(
    topics=["financial_markets", "economy_macro", "economy_monetary", "technology"],
    limit=10,
    total_limit=50,
    sort="LATEST"
)

    for title in res:
        print(title)

if __name__ == "__main__":
    main()