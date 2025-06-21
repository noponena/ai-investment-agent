from typing import Any, Dict, List

import requests
from market_data_api import MarketDataAPI

from ai_agent import OpenAIAgent
from io_manager import IOManager


class NewsAPI(MarketDataAPI):
    def _do_get_news(self, **kwargs) -> Any:
        count = kwargs["count"] if "count" in kwargs else 10
        url = (
            f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize={count}&apiKey={self.api_key}"
        )
        resp = requests.get(url)
        data = resp.json()
        return data.get("articles", [])

    @staticmethod
    def _format_response(response: Any) -> List[Dict[str, str]]:
        result = []
        for a in response:
            summary = a.get("description") or ""
            if not summary and a.get("content"):
                summary = a["content"][:200]
            result.append({
                "title": a["title"],
                "summary": summary
            })
        return result


def main():
    io = IOManager("C:/Aaro/Projects/Personal/AI Investment Agent/settings.yaml")
    news_api_key = io.read_api_key("NEWS_API_KEY")
    openai_api_key = io.read_api_key("OPENAI_API_KEY")
    newsapi = NewsAPI(news_api_key)
    res = newsapi.get_news()
    for item in res:
        print(item)
    #agent = OpenAIAgent(openai_api_key)
    #summary = agent.summarize_market_headlines(res)
    #print(summary)

if __name__ == "__main__":
    main()