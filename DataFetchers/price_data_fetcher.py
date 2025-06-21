import os

os.environ["YFINANCE_USE_CURL_CFFI"] = "0"
import yfinance as yf
from data_fetcher_base import DataFetcher


class PriceDataFetcher(DataFetcher):
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch(self):
        data = []
        for t in self.tickers:
            ticker = yf.Ticker(t)
            info = ticker.info
            data.append({
                "ticker": t,
                "name": info.get("longName", t),
                "price": info.get("regularMarketPrice"),
                "ytd_return": info.get("ytdReturn")
            })
        return data

    def format_for_prompt(self, data):
        lines = ["Current market data:"]
        for item in data:
            ytd = f", YTD: {item['ytd_return']*100:.1f}%" if item['ytd_return'] else ""
            lines.append(f"- {item['ticker']}: €{item['price']}{ytd}")
        return "\n".join(lines)

def main():
    data_fetcher = PriceDataFetcher(['VWRL.AS', 'NVDA', 'SGLN.L', 'SWDA.L'])
    data = data_fetcher.fetch()
    formatted = data_fetcher.format_for_prompt(data)
    print(data)
    print(formatted)

if __name__ == "__main__":
    main()
