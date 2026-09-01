import logging
import signal
import sys

from finnhub_quotes.config import load_config
from finnhub_quotes.rest_client import FinnhubRestClient
from finnhub_quotes.stream_client import FinnhubStreamClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    config = load_config()

    rest_client = FinnhubRestClient(config.api_key)
    logger.info("Fetching initial quotes for %s", ", ".join(config.symbols))
    for symbol in config.symbols:
        try:
            quote = rest_client.get_quote(symbol)
            logger.info("%s: price=%s change=%s%%", symbol, quote.get("c"), quote.get("dp"))
        except Exception as exc:
            logger.warning("Failed to fetch initial quote for %s: %s", symbol, exc)

    def on_trade(trade: dict):
        logger.info(
            "TRADE %s price=%s volume=%s ts=%s",
            trade.get("s"),
            trade.get("p"),
            trade.get("v"),
            trade.get("t"),
        )

    stream_client = FinnhubStreamClient(config.api_key, config.symbols, on_trade)

    def handle_sigint(signum, frame):
        logger.info("Shutting down...")
        stream_client.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    stream_client.run()


if __name__ == "__main__":
    main()
