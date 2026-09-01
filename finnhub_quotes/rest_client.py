from typing import Dict, Iterable, List

import requests

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


class FinnhubRestClient:
    """Thin wrapper around Finnhub's REST quote endpoint."""

    def __init__(self, api_key: str, timeout: float = 10.0):
        self.api_key = api_key
        self.timeout = timeout

    def get_quote(self, symbol: str) -> Dict:
        response = requests.get(
            f"{FINNHUB_BASE_URL}/quote",
            params={"symbol": symbol, "token": self.api_key},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_quotes(self, symbols: Iterable[str]) -> Dict[str, Dict]:
        return {symbol: self.get_quote(symbol) for symbol in symbols}
