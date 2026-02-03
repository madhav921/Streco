# strategies/alpha_factors.py
import pandas as pd

def compute_alpha_factors(df):
    """
    Returns last-row alpha factor scores
    """

    row = df.iloc[-1]

    # =============================
    # MOMENTUM FACTOR
    # =============================
    momentum = (
        0.4 * row.get("z_return", 0) +
        0.3 * row.get("ret_5", 0) +
        0.3 * row.get("trend_strength", 0)
    )

    # =============================
    # MEAN REVERSION FACTOR
    # =============================
    mean_reversion = -row.get("mean_rev_score", 0)

    # =============================
    # RISK / STABILITY FACTOR
    # =============================
    risk = (
        row.get("sharpe_20", 0) -
        row.get("vol_20", 0) -
        row.get("kurt_20", 0)
    )

    # =============================
    # SMART MONEY FACTOR
    # Binary institutional signals
    # =============================
    smc = 0
    if row.get("order_block_bull", False) and row.get("bos_up", False):
        smc = 1
    elif row.get("order_block_bear", False) and row.get("bos_down", False):
        smc = -1

    return {
        "momentum": momentum,
        "mean_reversion": mean_reversion,
        "risk": risk,
        "smart_money": smc
    }
