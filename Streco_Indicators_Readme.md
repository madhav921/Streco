# 📈 Streco Feature & Indicator Documentation

## 🔥 Smart Money Concept Indicators

### **Fair Value Gap (FVG)**

**What it indicates:**
Price imbalance where institutions moved price aggressively, leaving
untraded zones.

**Signal use:** ->>>
- Buy when price returns to bullish FVG and holds
- Sell when price returns to bearish FVG

------------------------------------------------------------------------

### **Order Blocks (OB)**

**What it indicates:**
Last opposite candle before a strong impulsive move, representing
institutional accumulation/distribution.

**Signal use:**
- Buy near bullish order blocks
- Sell near bearish order blocks

------------------------------------------------------------------------

### **Liquidity Sweep**

**What it indicates:**
Price spikes above highs or below lows to trigger stop-loss orders,
followed by reversal.

**Signal use:**
- After sweep → contrarian reversal trades

------------------------------------------------------------------------

### **Break of Structure (BOS)**

**What it indicates:**\
Change in market structure confirming trend reversal or continuation.

**Signal use:**\
- Only buy after bullish BOS\
- Only short after bearish BOS

------------------------------------------------------------------------

## 📊 Quantitative Indicators

### **Z-score Returns**

**What it indicates:**\
How extreme the current return is compared to recent history.

**Signal use:**\
- High positive → momentum continuation\
- High negative → mean reversion opportunity

------------------------------------------------------------------------

### **Mean Reversion Score (Bollinger)**

**What it indicates:**\
Deviation of price from its moving average.

**Signal use:**\
- Buy when far below mean\
- Sell when far above mean

------------------------------------------------------------------------

### **Trend Strength Index**

**What it indicates:**\
Strength of the current trend using MA slope and ATR.

**Signal use:**\
- Trade only when trend strength is high\
- Avoid sideways markets

------------------------------------------------------------------------

### **Rolling Sharpe Ratio**

**What it indicates:**\
Risk-adjusted return over a rolling window.

**Signal use:**\
- Rank stocks for portfolio allocation\
- Prefer stable high-Sharpe stocks

------------------------------------------------------------------------

## 🤖 Machine Learning Features

### **Lagged Returns (ret_1, ret_5, ret_10, ret_20)**

**What it indicates:**\
Momentum and autocorrelation patterns in returns.

**Use:**\
- Core ML predictors for price direction models

------------------------------------------------------------------------

### **Rolling Volatility**

**What it indicates:**\
Market risk regime (calm vs turbulent).

**Use:**\
- Position sizing\
- Regime filtering\
- Risk control

------------------------------------------------------------------------

### **Skew & Kurtosis**

**What it indicates:**\
Return distribution asymmetry and tail risk.

**Use:**\
- Crash risk detection\
- Tail-event modeling

------------------------------------------------------------------------

### **Volume Delta**

**What it indicates:**\
Buy vs sell pressure proxy.

**Use:**\
- Breakout confirmation\
- Smart money accumulation detection

------------------------------------------------------------------------

## 🧠 Practical Usage Notes

-   **Smart Money indicators** → discretionary + systematic trading
    signals\
-   **Quant indicators** → ranking, alpha models, portfolio
    construction\
-   **ML features** → predictive models (XGBoost, LSTM, Transformers)

------------------------------------------------------------------------
