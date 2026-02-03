# strategies/recommender.py
import pandas as pd
from datetime import datetime
import pytz
from strategies.quant_score import compute_stock_score
from stock_names import STOCK_NAMES

IST = pytz.timezone("Asia/Kolkata")

def decision_from_score(score):
    """Convert score to Buy/Sell/Hold"""
    if score > 1.0:
        return "STRONG BUY"
    elif score > 0.3:
        return "BUY"
    elif score < -1.0:
        return "STRONG SELL"
    elif score < -0.3:
        return "SELL"
    else:
        return "HOLD"

def get_top_stocks(stock_data_dict, save_path="latest_recommendations.csv"):
    scores = []

    for symbol, df in stock_data_dict.items():
        score = compute_stock_score(df)
        if score is None:
            continue

        score = score * 100  # scale for UI
        decision = decision_from_score(score / 100)

        full_name = STOCK_NAMES.get(symbol, symbol)
        scores.append((symbol, full_name, score, decision))

    # Sort by score descending
    scores.sort(key=lambda x: x[2], reverse=True)

    # Convert to DataFrame
    rec_df = pd.DataFrame(scores, columns=["Symbol", "Company", "Score", "Decision"])

    # Add timestamp
    rec_df["Timestamp"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

    # Save CSV
    rec_df.to_csv(save_path, index=False)

    print(f"✅ Recommendations saved to {save_path}")

    return scores
