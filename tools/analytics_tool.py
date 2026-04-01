import numpy as np
import ta


def compute_technical(df):

    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()

    latest = df.iloc[-1]

    return {
        "MA50": float(latest["MA50"]),
        "MA200": float(latest["MA200"]),
        "RSI": float(latest["RSI"]),
        "MACD": float(latest["MACD"]),
    }


def compute_risk(df):

    returns = df["Close"].pct_change().dropna()

    volatility = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    return {
        "volatility": float(volatility),
        "sharpe": float(sharpe),
    }