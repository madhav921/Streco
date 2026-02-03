# risk/risk_model.py
import numpy as np

class RiskModel:
    def calculate_volatility(self, df):
        return np.std(df["Close"].pct_change()) * 100

    def risk_score(self, df):
        vol = self.calculate_volatility(df)
        if vol < 1:
            return "LOW"
        elif vol < 3:
            return "MEDIUM"
        else:
            return "HIGH"
