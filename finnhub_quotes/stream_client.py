import json
import logging
import threading
import time
from typing import Callable, Iterable, List, Optional

import websocket

logger = logging.getLogger(__name__)

FINNHUB_WS_URL = "wss://ws.finnhub.io"


class FinnhubStreamClient:
    """Streams real-time trade ticks for a set of symbols over Finnhub's websocket."""

    def __init__(
        self,
        api_key: str,
        symbols: Iterable[str],
        on_trade: Callable[[dict], None],
        reconnect_delay: float = 5.0,
    ):
        self.api_key = api_key
        self.symbols: List[str] = list(symbols)
        self.on_trade = on_trade
        self.reconnect_delay = reconnect_delay
        self._stop = threading.Event()
        self._ws: Optional[websocket.WebSocketApp] = None

    def _on_open(self, ws):
        logger.info("Connected to Finnhub, subscribing to %d symbols", len(self.symbols))
        for symbol in self.symbols:
            ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    def _on_message(self, ws, message):
        data = json.loads(message)
        if data.get("type") != "trade":
            return
        for trade in data.get("data", []):
            self.on_trade(trade)

    def _on_error(self, ws, error):
        logger.error("Finnhub websocket error: %s", error)

    def _on_close(self, ws, status_code, msg):
        logger.info("Finnhub websocket closed: %s %s", status_code, msg)

    def run(self):
        """Blocks, reconnecting automatically until stop() is called."""
        while not self._stop.is_set():
            self._ws = websocket.WebSocketApp(
                f"{FINNHUB_WS_URL}?token={self.api_key}",
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
            )
            self._ws.run_forever()
            if not self._stop.is_set():
                logger.info("Reconnecting in %.0fs...", self.reconnect_delay)
                time.sleep(self.reconnect_delay)

    def stop(self):
        self._stop.set()
        if self._ws:
            self._ws.close()
