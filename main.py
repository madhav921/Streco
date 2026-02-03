# main.py
import config as cg
import data.market_data as mkt_data
import indicators.metadata as md
from strategies.recommender import get_top_stocks
import json
import os
from datetime import datetime
import pytz
import pandas as pd

IST = pytz.timezone("Asia/Kolkata")
os.makedirs("metadata", exist_ok=True)

def main():
    data_dict = {}
    cnt = 0
    for i in cg.NIFTY200:
        symbol = i
        # print(symbol)
        # yf_symbol = i + ".NS"
        yf_symbol = i
        df = mkt_data.MarketData().historical(yf_symbol)
        df = pd.read_csv(f"metadata/{symbol}.csv")
        df = md.compute_metadata(df)
        data_dict[symbol] = df
        file_path = f"metadata/{symbol}.parquet"
        df.to_parquet(file_path)
        df.to_csv(file_path.replace(".parquet", ".csv"))
        # print(f"Saved metadata: {file_path}")
        

    top10 = get_top_stocks(data_dict)

    # Save results
    timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "timestamp": timestamp,
        "stocks": [{"symbol": s, "name": name, "score": float(score), "Decision": dec} for s, name, score, dec in top10]
    }

    with open("latest_recommendations.json", "w") as f:
        json.dump(result, f, indent=4)
    
    with open("metadata/last_updated.txt", "w") as f:
        f.write(timestamp)

    # print("🔥 TOP STOCKS TO INVEST:")
    # for s, name, score, dec in top10:
    #     print(s, name, round(score, 3), dec)

if __name__ == "__main__":
    main()
