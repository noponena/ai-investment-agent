from datetime import datetime
from typing import Any, Dict, List

from api_clients.data_providers.prices.price_provider_base import PriceProviderBase
from api_clients.data_providers.utils import is_alpha_vantage_valid_response
from io_utils.io_manager import IOManager


class AlphaVantagePricesAPI(PriceProviderBase):
    _name = "AlphaVantagePrice"
    _demo_url: str = (
        "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
    )

    def _fetch(self, **kwargs) -> Any:
        """
        Fetch raw daily prices for each ticker and return as a list of dicts: [{ "ticker": ..., "raw": ... }, ...]
        """
        tickers = kwargs.get("tickers")
        if not tickers:
            raise ValueError("No ticker(s) provided.")
        if isinstance(tickers, str):
            tickers = [tickers]
        results = []
        for ticker in tickers:
            url = (
                f"https://www.alphavantage.co/query"
                f"?function=TIME_SERIES_DAILY_ADJUSTED"
                f"&symbol={ticker}&outputsize=full"
                f"&apikey={self._api_key}"
            )
            data = self._send_request(url)
            results.append({"ticker": ticker, "raw": data})
        return results

    def _fetch_mock_data(self, **kwargs) -> Any:
        """
        Fetches demo/mock data from Alpha Vantage's public demo endpoint.
        """
        data = self._send_request(self._demo_url)
        return [{"ticker": "IBM", "raw": data}]

    def _format_response(self, response: Any) -> List[Dict[str, str]]:
        formatted = []
        current_year = str(datetime.now().year)
        for entry in response:
            ticker = entry.get("ticker", "")
            raw = entry.get("raw", {})
            series_key = next((k for k in raw.keys() if "Time Series" in k), None)
            if not series_key:
                formatted.append(
                    {
                        "ticker": ticker,
                        "price": "",
                        "timestamp": "",
                        "ytd_return": "",
                        "error": raw.get("Note")
                        or raw.get("Error Message")
                        or "No time series data.",
                    }
                )
                continue
            timeseries = raw[series_key]
            if not timeseries:
                formatted.append(
                    {
                        "ticker": ticker,
                        "price": "",
                        "timestamp": "",
                        "ytd_return": "",
                        "error": "No time series entries.",
                    }
                )
                continue
            # Dates are in "YYYY-MM-DD" format
            all_dates = sorted(timeseries.keys())
            # Find the first trading day of the current year
            first_date_this_year = next((d for d in all_dates if d.startswith(current_year)), None)
            latest_date = all_dates[-1]
            latest_close = timeseries[latest_date].get("4. close", None)
            ytd_return_str = ""
            if first_date_this_year:
                first_close = timeseries[first_date_this_year].get("4. close", None)
                if latest_close is not None and first_close is not None:
                    try:
                        ytd_return = (float(latest_close) - float(first_close)) / float(first_close)
                        ytd_return_str = f"{ytd_return:.4f}"
                    except (TypeError, ValueError, ZeroDivisionError):
                        ytd_return_str = ""
            formatted.append(
                {
                    "ticker": ticker,
                    "price": str(latest_close) if latest_close is not None else "",
                    "timestamp": latest_date,
                    "ytd_return": ytd_return_str,
                }
            )
        return formatted

    def _is_valid_response(self, response: Any) -> bool:
        return is_alpha_vantage_valid_response(response)


def main():
    io = IOManager()
    api_key = io.read_api_key("ALPHA_VANTAGE_API_KEY")
    data_provider = AlphaVantagePricesAPI(api_key=api_key, demo_mode=False)

    res = data_provider.get(tickers=["AAPL"])

    for title in res:
        print(title)


if __name__ == "__main__":
    main()
