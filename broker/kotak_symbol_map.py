import pandas as pd
import kotak_config as cg
# from nsepython import nse_index_constituents

KOTAK_MASTER_FILE = "nse_cm-v1.csv"

class KotakSymbolMapper:
    def __init__(self, master_file=KOTAK_MASTER_FILE):
        self.df = pd.read_csv(master_file)
        self.symbol_map = self._build_symbol_map()

    def _build_symbol_map(self):
        mapping = {}
        eq_df = self.df[self.df["series"] == "EQ"]

        for _, row in eq_df.iterrows():
            symbol = row["symbol"].strip()
            token = str(row["token"])
            trading_symbol = row["trading_symbol"]

            mapping[symbol] = {
                "trading_symbol": trading_symbol,
                "token": token
            }
        return mapping

    def get_nifty200_kotak_symbols(self):
        nifty200 = cg.NIFTY200
        symbols = [s["symbol"] for s in nifty200]

        mapped = {}
        for s in symbols:
            if s in self.symbol_map:
                mapped[s] = self.symbol_map[s]

        return mapped
