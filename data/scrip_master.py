import requests
import pandas as pd

class KotakScripMaster:
    # URL= client.scrip_master('nse_cm')
    URL = "https://lapi.kotaksecurities.com/wso2-scripmaster/v1/prod/2026-01-26/transformed-v1/nse_cm-v1.csv"

    def fetch_all(self):
        df = pd.read_csv(self.URL)
        return df

    def get_nse_equities(self):
        df = self.fetch_all()
        return df[df["pExchSeg"] == "nse_cm"]

    def get_nifty_like_stocks(self):
        df = self.get_nse_equities()
        return df["tradingsymbol"].unique().tolist()
