from ai_clients.openai_agent import OpenAIAgent
from api_clients.data_providers import *
from data_fetchers import *
from io_utils.io_manager import IOManager


def test():
    io = IOManager()
    alpha_vantage_api_key = io.read_api_key("ALPHA_VANTAGE_API_KEY")
    news_api_key = io.read_api_key("NEWS_API_KEY")

    price_data_fetcher = PriceDataFetcher()
    news_data_fetcher = NewsDataFetcher()

    yahoo_price_provider = YahooFinancePriceAPI()
    alpha_vantage_price_provider = AlphaVantagePricesAPI(
        api_key=alpha_vantage_api_key, demo_mode=False
    )

    news_api_provider = NewsAPI(api_key=news_api_key)
    yahoo_news_provider = YahooFinanceNewsAPI()

    price_data_fetcher.add_apis([yahoo_price_provider, alpha_vantage_price_provider])
    news_data_fetcher.add_apis([news_api_provider, yahoo_news_provider])

    price_data = price_data_fetcher.get(
        api_kwargs={
            "YahooFinancePrice": {"tickers": ["AAPL", "MSFT"]},
            "AlphaVantagePrice": {"tickers": ["TSLA"], "interval": "5min"},
        }
    )

    news_data = news_data_fetcher.get(
        api_kwargs={
            "NewsAPI": {"count": 7},
            "YahooFinanceNews": {"count": 5},
        }
    )

    print("Data from price data fetcher:\n")
    for entry in price_data:
        print(entry)

    print("\n\n--------------\n\n")
    print("Data from news data fetcher:\n")
    for entry in news_data:
        print(entry)


def main():
    io = IOManager()
    api_key = io.read_api_key("OPENAI_API_KEY")
    base_prompt = io.base_prompt
    buckets = io.buckets
    model = io.model
    print(f"Using model: {model}")

    prompt = base_prompt + "\n\nBuckets and descriptions:\n"
    for b in buckets:
        prompt += f"{b['name']} ({b['allocation']}%): {b['description']}\n"

    print(f"Prompt sent to AI:\n\n{prompt}")

    agent = OpenAIAgent(api_key)
    recommendations = agent.get_recommendations(prompt, model=model)

    print("AI's response:\n")
    for rec in recommendations:
        print(f"{rec['bucket']}: {rec['ticker']} – {rec['name']}")


if __name__ == "__main__":
    test()
