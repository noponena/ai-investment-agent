from typing import Any, Dict, List

import feedparser

from api_clients.data_providers.news.news_provider_base import NewsProviderBase


class YahooFinanceNewsAPI(NewsProviderBase):
    _name = "YahooFinanceNews"
    _requires_api_key = False

    def _fetch(self, **kwargs) -> Any:
        """
        Fetches business news headlines from Yahoo Finance via RSS.
        Optional kwargs: 'count' (int): number of headlines to return.
        """
        count = kwargs.get("count", 10)
        url = "https://finance.yahoo.com/news/rssindex"

        feed = feedparser.parse(url)
        entries = feed.entries[:count]
        return entries

    def _fetch_mock_data(self, **kwargs) -> Any:
        raise NotImplementedError

    def _format_response(self, response: Any) -> List[Dict[str, str]]:
        result = []
        for entry in response:
            title = entry.get("title", "")
            # Try several fields for summary/description/content
            summary = (
                entry.get("summary")
                or entry.get("description")
                or (entry.get("content")[0].value if entry.get("content") else "")
                or ""
            )
            # If summary is still empty, just use title or a placeholder
            if not summary:
                summary = ""
            result.append({"title": title, "summary": summary})
        return result

    def _is_valid_response(self, response: Any) -> bool:
        """
        No response validation as of now.
        """
        return True


def main():
    data_provider = YahooFinanceNewsAPI()
    print(f"name = {data_provider.name}")

    res = data_provider.get(count=50)
    for title in res:
        print(title)


if __name__ == "__main__":
    main()
