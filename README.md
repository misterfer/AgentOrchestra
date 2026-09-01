# AgentOrchestra

## Real-time stock quotes (Finnhub)

Connects to [Finnhub](https://finnhub.io) to fetch real-time quotes for a
configurable set of companies: a snapshot via the REST `/quote` endpoint on
startup, then live trade ticks over Finnhub's websocket.

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # add your Finnhub API key
```

### Run

```bash
python main.py
```

The symbol list defaults to `finnhub_quotes/symbols.py`. Override it by
setting `FINNHUB_SYMBOLS` (comma-separated tickers) in `.env` or the
environment.