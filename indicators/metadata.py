import pandas as pd
import numpy as np

def compute_metadata(df):
    # ================================
    # BASIC PRICE FEATURES
    # ================================
    df["body"] = (df["Close"] - df["Open"]).abs()
    df["upper_wick"] = df["High"] - df[["Close","Open"]].max(axis=1)
    df["lower_wick"] = df[["Close","Open"]].min(axis=1) - df["Low"]
    df["range"] = df["High"] - df["Low"]
    df["return"] = df["Close"].pct_change()

    # ================================
    # MOVING AVERAGES
    # ================================
    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()
    df["ma200"] = df["Close"].rolling(200).mean()
    df["ma20_slope"] = df["ma20"].diff()

    # ================================
    # RSI
    # ================================
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # ================================
    # ATR (Volatility)
    # ================================
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(14).mean()

    # ================================
    # VOLUME FEATURES
    # ================================
    df["vol_ma20"] = df["Volume"].rolling(20).mean()
    df["rel_volume"] = df["Volume"] / df["vol_ma20"]
    df["vol_delta"] = np.where(df["Close"] > df["Open"], df["Volume"], -df["Volume"])

    # ================================
    # SMART MONEY CONCEPTS
    # ================================
    # Fair Value Gap (FVG)
    df["fvg_bull"] = df["Low"] > df["High"].shift(-2)
    df["fvg_bear"] = df["High"] < df["Low"].shift(-2)

    # Break of Structure (BOS)
    df["hh"] = df["High"] > df["High"].shift(1)
    df["ll"] = df["Low"] < df["Low"].shift(1)
    df["bos_up"] = df["hh"] & (~df["ll"])
    df["bos_down"] = df["ll"] & (~df["hh"])

    # Liquidity Sweep
    df["liq_sweep_high"] = (df["High"] > df["High"].shift(1)) & (df["Close"] < df["High"].shift(1))
    df["liq_sweep_low"] = (df["Low"] < df["Low"].shift(1)) & (df["Close"] > df["Low"].shift(1))

    # Order Block (simplified impulsive move detection)
    impulse = df["range"] > (df["atr"] * 1.5)
    df["order_block_bull"] = impulse & (df["Close"].shift(1) < df["Open"].shift(1))
    df["order_block_bear"] = impulse & (df["Close"].shift(1) > df["Open"].shift(1))

    # ================================
    # QUANT SIGNALSd
    # ================================
    # Z-score of returns
    df["ret_mean20"] = df["return"].rolling(20).mean()
    df["ret_std20"] = df["return"].rolling(20).std()
    df["z_return"] = (df["return"] - df["ret_mean20"]) / df["ret_std20"]

    # Mean Reversion (Bollinger style)
    df["bb_upper"] = df["ma20"] + 2 * df["Close"].rolling(20).std()
    df["bb_lower"] = df["ma20"] - 2 * df["Close"].rolling(20).std()
    df["mean_rev_score"] = (df["Close"] - df["ma20"]) / df["Close"].rolling(20).std()

    # Trend Strength (ADX-like proxy)
    df["trend_strength"] = df["ma20_slope"] / df["atr"]

    # Rolling Sharpe Ratio
    df["sharpe_20"] = df["return"].rolling(20).mean() / df["return"].rolling(20).std()
    df["sharpe_60"] = df["return"].rolling(60).mean() / df["return"].rolling(60).std()

    # ================================
    # ML FEATURES
    # ================================
    # Lagged Returns
    for lag in [1,5,10,20]:
        df[f"ret_{lag}"] = df["return"].shift(lag)

    # Rolling Volatility
    df["vol_5"] = df["return"].rolling(5).std()
    df["vol_20"] = df["return"].rolling(20).std()
    df["vol_60"] = df["return"].rolling(60).std()

    # Skew & Kurtosis
    df["skew_20"] = df["return"].rolling(20).skew()
    df["kurt_20"] = df["return"].rolling(20).kurt()
    df.to_csv("metadata.csv")
    return df
        