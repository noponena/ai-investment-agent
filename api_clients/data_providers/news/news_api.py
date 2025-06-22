from typing import Any, Dict, List, Optional

from ai_clients import OpenAIAgent
from api_clients.data_providers.news.news_provider_base import NewsProviderBase
from io_utils.io_manager import IOManager


class NewsAPI(NewsProviderBase):
    _name = "NewsAPI"

    def _fetch(self, **kwargs) -> Any:
        count = kwargs.get("count", 10)
        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?category=business&language=en&pageSize={count}&apiKey={self._api_key}"
        )
        return self._send_request(url)

    def _fetch_mock_data(self, **kwargs) -> Any:
        raise NotImplementedError

    def _format_response(self, response: Any) -> List[Dict[str, str]]:
        result = []
        for a in response:
            summary = a.get("description") or ""
            if not summary and a.get("content"):
                summary = a["content"][:200]
            result.append({"title": a.get("title", ""), "summary": summary})
        return result

    def _send_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Override the base _send_request to extract 'articles' from the NewsAPI response.
        """
        data = super()._send_request(url, method, headers, params, **kwargs)
        if isinstance(data, dict):
            return data.get("articles", [])
        else:
            return []

    def _is_valid_response(self, response: Any) -> bool:
        """
        No response validation as of now.
        """
        return True


def main():
    io = IOManager()
    news_api_key = io.read_api_key("NEWS_API_KEY")
    openai_api_key = io.read_api_key("OPENAI_API_KEY")
    data_provider = NewsAPI(news_api_key)
    res = data_provider.get()
    for item in res:
        print(item)
    # agent = OpenAIAgent(openai_api_key)
    # summary = agent.summarize_market_headlines(res)
    # print(summary)


if __name__ == "__main__":
    main()
