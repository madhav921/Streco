# strategies/rules.py
class Rules:
    @staticmethod
    def rule_based_signal(df):
        df["signal"] = 0

        # Trend filter (avoid sideways)
        trend_filter = (df["close"] > df["ma50"]) & (df["ma50"] > df["ma200"])

        # Momentum confirmation
        momentum = df["ret_5"] > 0

        # Volume confirmation
        volume_confirm = df["rel_volume"] > 1.2

        # Trend strength filter
        strong_trend = df["trend_strength"] > 0

        # Buy signal
        df.loc[trend_filter & momentum & volume_confirm & strong_trend, "signal"] = 1

        return df

