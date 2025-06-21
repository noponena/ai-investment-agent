from data_fetcher_base import DataFetcher


class MarketTrendsFetcher(DataFetcher):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self):
        # Example: in real code, fetch from API
        return {
            "overview": "Tech and AI stocks are strong, inflation cooling, Fed likely to hold rates."
        }

    def format_for_prompt(self, data):
        # Expects data to be a dict with "overview"
        return f"Market Overview: {data['overview']}"
