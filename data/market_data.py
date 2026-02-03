import yfinance as yf
import pandas as pd

class MarketData:
    def convert_to_ist(self, df):
        df.index = pd.to_datetime(df.index)
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
        df.index = df.index.tz_convert("Asia/Kolkata")
        return df

    def historical(self, symbol):
        df = yf.download(symbol, period="1mo", interval="30m")
        df = df.droplevel(1, axis=1)
        df = self.convert_to_ist(df)
        return df