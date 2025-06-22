import datetime
from typing import Any, Dict, List

import yfinance as yf

from api_clients.data_providers.prices.price_provider_base import PriceProviderBase
from io_utils import IOManager


class YahooFinancePriceAPI(PriceProviderBase):
    """
    Data provider for price information using Yahoo Finance (batch mode).
    """

    _name = "YahooFinancePrice"
    _requires_api_key = False

    def _fetch(self, **kwargs) -> List[Dict[str, Any]]:
        tickers = kwargs.get("tickers", [])
        if not tickers:
            raise ValueError("No tickers provided for price fetch.")

        this_year = datetime.datetime.now().year
        df = yf.download(
            tickers=tickers,
            start=f"{this_year}-01-01",
            end=None,
            group_by="ticker",
            auto_adjust=False,  # So we can always access 'Adj Close'
            threads=True,
            progress=False,
        )

        results = []
        for t in tickers:
            try:
                prices = df if len(tickers) == 1 else df[t]
                start_price = prices["Adj Close"].dropna().iloc[0]
                latest_price = prices["Adj Close"].dropna().iloc[-1]
                latest_date = prices.index[-1].strftime("%Y-%m-%d")
                ytd_return = (latest_price - start_price) / start_price
            except (KeyError, IndexError) as e:
                print(f"Error fetching prices for {t}: {e}")
                latest_price = None
                latest_date = None
                ytd_return = None

            results.append(
                {
                    "ticker": t,
                    "price": latest_price,
                    "timestamp": latest_date,
                    "ytd_return": "" if ytd_return is None else f"{ytd_return:.4f}",
                }
            )
        return results

    def _fetch_mock_data(self, **kwargs) -> Any:
        raise NotImplementedError

    def _format_response(self, response: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Converts price data into a list of dicts with stringified values.
        Example output: [{"ticker": "AAPL", "name": "AAPL", "price": "194.83", "ytd_return": ""}, ...]
        """
        formatted = []
        for item in response:
            formatted.append(
                {
                    "ticker": str(item.get("ticker", "")),
                    "price": "" if item.get("price") is None else str(item.get("price")),
                    "timestamp": str(item.get("timestamp", "")),
                    "ytd_return": (
                        "" if item.get("ytd_return") is None else str(item.get("ytd_return"))
                    ),
                }
            )
        return formatted

    def _is_valid_response(self, response: Any) -> bool:
        """
        No response validation as of now.
        """
        return True


def main():
    io = IOManager()
    data_provider = YahooFinancePriceAPI()
    print(f"name = {data_provider.name}")

    res = data_provider.get(tickers=["AAPL", "MSFT", "TSLA"])
    for title in res:
        print(title)


if __name__ == "__main__":
    main()
