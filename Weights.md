# 📊 Streco Multi-Factor Scoring Strategy

Streco is a quantitative alpha-modeling framework that converts engineered financial indicators into normalized factor scores. By combining statistical momentum with institutional price action (Smart Money), Streco generates a weighted signal designed to navigate various market regimes.

## 🏗 Strategy Architecture

The engine follows a three-step process: **Feature Engineering → Normalization → Weighted Aggregation.**

### 1. Signal Normalization
To ensure comparability across diverse metrics (e.g., comparing a percentage RSI to a price-based EMA), all indicators undergo:
* **Z-Score Normalization:** Scaling features to have a mean of 0 and a standard deviation of 1.
* **Percentile Ranking:** Mapping values to a 0–1 range to mitigate the impact of outliers.

### 2. Factor Groups
The model categorizes indicators into four distinct alpha drivers:

| Factor | Components |
| :--- | :--- |
| **Momentum** | Z-score returns, lagged returns, trend strength, EMA slope |
| **Mean Reversion** | Bollinger Band deviation, Relative Strength Index (RSI) |
| **Risk** | Rolling volatility, Sharpe ratio, Skewness, Kurtosis |
| **Smart Money** | Fair Value Gaps (FVG), Order Blocks, Liquidity Sweeps, Break of Structure (BOS) |

---

## 🔢 The Alpha Model

### Final Score Formula
The strategy uses a weighted linear combination to produce the final signal:

$$FinalScore = 0.40(Mom) + 0.25(Risk) + 0.20(Rev) + 0.15(SMC)$$

### Decision Thresholds
The output score determines the directional bias and conviction level:

* **> 1.0** 🟢 Strong Buy
* **0.3 to 1.0** 📈 Buy
* **-0.3 to 0.3** ⚖️ Hold / Neutral
* **-1.0 to -0.3** 📉 Sell
* **< -1.0** 🔴 Strong Sell

---

## 💼 Portfolio Construction & Rationale

### Execution
* **Ranking:** All assets in the universe are ranked by their `Final Score`.
* **Long Positions:** Selection of the **top decile (10%)** of stocks.
* **Hedging/Shorts:** Selection of the **bottom decile (10%)** to offset beta or capture downside.

### Why it Works
1.  **Empirical Alpha:** Momentum and risk-adjusted metrics historically explain the majority of equity returns.
2.  **Timing:** Mean reversion and Smart Money concepts refine entry/exit points, specifically targeting "liquidity traps" to reduce drawdowns.
3.  **Adaptability:** The multi-factor approach prevents the model from failing when a single style (e.g., Value or Growth) goes out of favor.

---