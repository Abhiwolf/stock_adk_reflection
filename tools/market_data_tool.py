import os
import ssl
import time
import requests

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import yfinance as yf

# ---------------------------------------------------------------------------
# Market suffixes for Indian exchanges
# ---------------------------------------------------------------------------
MARKET_SUFFIX = {
    "NSE": ".NS",   # National Stock Exchange of India
    "BSE": ".BO",   # Bombay Stock Exchange
}


def _make_session():
    """Create a requests session with browser-like headers and no SSL verify."""
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
    })
    return s


def _resolve_ticker(ticker: str, market: str = "US") -> str:
    """
    Return a yfinance-compatible ticker symbol.

    Examples
    -------
    _resolve_ticker("AAPL")                  -> "AAPL"
    _resolve_ticker("RELIANCE", "NSE")       -> "RELIANCE.NS"
    _resolve_ticker("TCS", "BSE")            -> "TCS.BO"
    _resolve_ticker("INFY.NS")               -> "INFY.NS"   (already qualified)
    """
    market = market.upper()
    if market == "US" or ticker.endswith((".NS", ".BO")):
        return ticker
    suffix = MARKET_SUFFIX.get(market)
    if suffix is None:
        raise ValueError(f"Unsupported market '{market}'. Use 'US', 'NSE', or 'BSE'.")
    return f"{ticker}{suffix}"


def _download(ticker: str, period: str, retries: int):
    """Core download logic with retry using yf.download() for reliability."""
    for attempt in range(retries):
        try:
            df = yf.download(ticker, period=period, threads=False, progress=False)
        except Exception as e:
            print(f"[market_data] Download error for {ticker}: {e}")
            df = None
        if df is not None and not df.empty:
            # Flatten multi-level columns if present (e.g. Price / Ticker levels)
            if hasattr(df.columns, 'nlevels') and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)
            return df
        wait = 5 * (attempt + 1)
        print(f"[market_data] Empty result for {ticker}, retrying in {wait}s...")
        time.sleep(wait)
    raise RuntimeError(f"Failed to download data for {ticker} after {retries} attempts")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_stock_data(ticker: str, period: str = "1y", market: str = "US", retries: int = 3):
    """
    Fetch historical stock data for any market.

    Parameters
    ----------
    ticker  : symbol, e.g. "AAPL", "RELIANCE", "TCS"
    period  : yfinance period string – "5d", "1mo", "6mo", "1y", "5y", etc.
    market  : "US" (default) | "NSE" | "BSE"
    retries : number of retry attempts on failure

    Returns
    -------
    pandas.DataFrame with OHLCV columns.
    """
    resolved = _resolve_ticker(ticker, market)
    print(f"[market_data] Fetching {resolved} (market={market}, period={period})")
    return _download(resolved, period, retries)


def fetch_us_stock(ticker: str, period: str = "1y", retries: int = 3):
    """Convenience: fetch a US stock."""
    return fetch_stock_data(ticker, period=period, market="US", retries=retries)


def fetch_india_stock(ticker: str, exchange: str = "NSE", period: str = "1y", retries: int = 3):
    """
    Convenience: fetch an Indian stock.

    Parameters
    ----------
    ticker   : NSE/BSE symbol, e.g. "RELIANCE", "TCS", "INFY"
    exchange : "NSE" (default) or "BSE"
    """
    return fetch_stock_data(ticker, period=period, market=exchange, retries=retries)
