import os
from dataclasses import dataclass
from typing import List

from .symbols import DEFAULT_SYMBOLS

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@dataclass
class Config:
    api_key: str
    symbols: List[str]


def load_config() -> Config:
    api_key = os.environ.get("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError(
            "FINNHUB_API_KEY is not set. Copy .env.example to .env and add your Finnhub API key."
        )

    symbols_env = os.environ.get("FINNHUB_SYMBOLS")
    symbols = (
        [s.strip().upper() for s in symbols_env.split(",") if s.strip()]
        if symbols_env
        else DEFAULT_SYMBOLS
    )

    return Config(api_key=api_key, symbols=symbols)
