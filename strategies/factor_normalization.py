# strategies/factor_normalization.py
import pandas as pd

def zscore(series: pd.Series):
    """Z-score normalization"""
    return (series - series.mean()) / (series.std() + 1e-9)

def rank_normalize(series: pd.Series):
    """Percentile rank normalization (0-1)"""
    return series.rank(pct=True)

def normalize_features(df, cols, method="zscore"):
    df_norm = df.copy()
    for c in cols:
        if c not in df.columns:
            continue
        if method == "zscore":
            df_norm[c] = zscore(df[c])
        elif method == "rank":
            df_norm[c] = rank_normalize(df[c])
    return df_norm
