import src.data.crypto_prices as cc
import src.core.helper.dash_boostrap_utils as helper

class CryptoStats:

    def __init__(self):
        self.crypto_data = cc.CryptoPricesCC()

        pass


    def get_summary_table(self, symbols):
        df = self.crypto_data.get_prices(symbols=symbols)
        df.index.name = 'date'
        df.reset_index(inplace=True)
        return helper.generate_bootstrao_table(df.tail())
