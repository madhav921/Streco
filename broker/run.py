# run.py

import os
from xmlrpc import client
import pandas as pd
import json
from datetime import datetime
from auth import KotakSession
# from broker.kotak_api import KotakBroker   # If using alternate broker wrapper

RECO_FILE = "../latest_recommendations.csv"
POSITIONS_FILE = "positions.json"

MAX_POSITIONS = 3
ORDER_QTY = 1   # CHANGE THIS


# ================================
# Load active positions
# ================================
def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return {}


# ================================
# Save active positions
# ================================
def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=4)


# ================================
# Execute BUY Order (Placeholder)
# ================================
def execute_buy(client, symbol, qty):
    print(f"🚀 BUY ORDER -> {symbol}, Qty={qty}")



    res= client.place_order(
        exchange_segment="nse_cm",
        product="CNC",
        price="0",
        order_type="MKT",
        quantity="1",
        validity="DAY",
        trading_symbol=symbol,
        transaction_type="B",
        amo="NO",
        disclosed_quantity="0",
        market_protection="0",
        pf="N",
        trigger_price="0",
        tag=None,
        scrip_token=None,
        square_off_type=None,
        stop_loss_type=None,
        stop_loss_value=None,
        square_off_value=None,
        last_traded_price=None,
        trailing_stop_loss=None,
        trailing_sl_value=None,
    )
    print(res)
    return True  # Assume success


# ================================
# Execute SELL Order (Placeholder)
# ================================
def execute_sell(client, symbol, qty):
    print(f"🔥 SELL ORDER -> {symbol}, Qty={qty}")

    res = client.place_order(
        exchange_segment="nse_cm",
        product="CNC",
        price="0",
        order_type="MKT",
        quantity="1",
        validity="DAY",
        trading_symbol=symbol,
        transaction_type="S",
        amo="NO",
        disclosed_quantity="0",
        market_protection="0",
        pf="N",
        trigger_price="0",
        tag=None,
        scrip_token=None,
        square_off_type=None,
        stop_loss_type=None,
        stop_loss_value=None,
        square_off_value=None,
        last_traded_price=None,
        trailing_stop_loss=None,
        trailing_sl_value=None,
    )
    print(res)
    # TODO: Replace with real API call
    return True


# ================================
# MAIN TRADING LOOP
# ================================
def main():
    if not os.path.exists(RECO_FILE):
        print("❌ No recommendation file found")
        return

    df = pd.read_csv(RECO_FILE)

    # Filter BUY signals
    buy_df = df[df["Decision"].isin(["BUY", "STRONG BUY"])]
    buy_df = buy_df.sort_values("Score", ascending=False).head(MAX_POSITIONS)
    buy_df["Symbol"] = buy_df["Symbol"].str.replace(".NS", "-EQ", regex=False)

    # Load stored positions
    positions = load_positions()

    # Login Kotak
    session = KotakSession()
    client = session.get_client()
    # client = "LOL"

    # =============================
    # BUY LOGIC
    # =============================
    for _, row in buy_df.iterrows():
        symbol = row["Symbol"]

        symbol = symbol.replace(".NS", "-EQ")

        # Skip if already holding
        if symbol in positions:
            continue

        success = execute_buy(client, symbol, ORDER_QTY)

        if success:
            positions[symbol] = {
                "qty": ORDER_QTY,
                "buy_time": datetime.now().isoformat(),
                "score": row["Score"]
            }

    # =============================
    # SELL LOGIC (Placeholder)
    # =============================
    # Example: Sell if score < 0 or no longer BUY
    current_buy_symbols = set(buy_df["Symbol"].tolist())
    print("current_buy_symbols")
    print(current_buy_symbols)
    

    for symbol in list(positions.keys()):
        symbol = symbol.replace(".NS", "-EQ")
        if symbol not in current_buy_symbols:
            qty = positions[symbol]["qty"]
            success = execute_sell(client, symbol, qty)

            if success:
                del positions[symbol]

    # Save updated positions
    save_positions(positions)
    print("✅ Trading cycle complete")


if __name__ == "__main__":

    main()