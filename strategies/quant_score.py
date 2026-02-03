# strategies/quant_score.py
import pandas as pd
from strategies.factor_normalization import normalize_features
from strategies.alpha_factors import compute_alpha_factors

# # Final factor weights (research-backed)
# WEIGHTS = {
#     "momentum": 0.40,
#     "risk": 0.25,
#     "mean_reversion": 0.2,
#     "smart_money": 0.15
# }

# Final factor weights (research-backed)
WEIGHTS = {
    "momentum": 0.6,
    "risk": 0.15,
    "mean_reversion": 0.1,
    "smart_money": 0.15
}

def compute_stock_score(df, norm_method="zscore"):
    if df is None or df.empty or len(df) < 100:
        return None

    # Required columns for normalization
    cols = [
        "z_return","ret_5","trend_strength",
        "mean_rev_score","sharpe_20","vol_20","kurt_20"
    ]

    # Normalize features
    df_norm = normalize_features(df, cols, method=norm_method)

    # Drop NaNs only for required cols
    df_norm = df_norm.dropna(subset=cols)
    if df_norm.empty:
        return None

    # Compute factor groups
    factors = compute_alpha_factors(df_norm)

    # Weighted final score
    final_score = sum(WEIGHTS[k] * factors[k] for k in WEIGHTS)

    return float(final_score)
