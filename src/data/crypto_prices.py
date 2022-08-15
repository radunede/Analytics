import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.fundamentaldata import FundamentalData
import matplotlib.pyplot as plt
import requests
import datetime

class CryptoPricesCC:
    def __init__(self,):
        pass

    def get_price(self, symbol, from_date=None):
        fsym = symbol
        tsym = 'USD'
        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit=2000'
        response = requests.get(url)
        data = response.json()['Data']['Data']

        import pandas as pd
        data = pd.DataFrame(data)
        data['timestamp'] = data.apply(lambda x: datetime.datetime.fromtimestamp(x.time).strftime('%Y-%m-%d'), axis=1 )
        data.set_index('timestamp',inplace=True)
        if from_date is not None:
            data = data['2021-01-01':]
        columns = ['high','low','open','close','volumefrom','volumeto']
        df = data[columns]
        df.columns = ['high','low','open','close',fsym.lower(),tsym.lower()]

        return df[['high','low','open','close']]

    def get_prices(self, symbols, from_date=None):
        '''
        Get prices for multiple currencies.
        '''
        result = pd.DataFrame()
        for s in symbols:
            df = self.get_price(s, from_date)[['close']]
            df.columns = [s]
            if result.empty:
                result = df
            else:
                result = pd.merge(result, df, how='inner', on = 'timestamp')
        return result


class CryptoPricesAV:
    def __init__(self,api_key = '4V3Z3QEE9NHU5V0D'):
        self.api_key = api_key
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        self.fx = ForeignExchange(key=api_key, output_format='pandas')
        self.fd = FundamentalData(key=api_key, output_format='pandas')

    def get_company_data(self, ticker):
        return self.fd.get_company_overview(ticker)
        
        
    def get_calendar(self, tickers=None):
        url=f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={self.api_key}'
        df = pd.read_csv(url)
        df.set_index('reportDate', inplace=True)
        df.sort_index(inplace=True)
        if tickers is not None:
            df = df.loc[df.symbol.isin(tickers)]
        
        return df

    def get_historical(self, tickers, columns=['5. adjusted close']):
        '''
        Returns a DataFrame pf closing prices going back 
        '''
        data = pd.DataFrame()
        for ticker in tickers:
            
            ticker_data, meta_data = self.ts.get_monthly_adjusted(symbol=ticker)
            ticker_data = ticker_data[columns]
            if ticker_data.dropna().empty == False:
                data = pd.concat([data, ticker_data], axis=1)
            else:
                print(f"{ticker} has no data!")
        data.columns = tickers
        return data


    def get_price(self, ticker,columns=['05. price','07. latest trading day']):
        '''
        Returns a DataFrame of prices for ticker on Alpha Vantage API 
        '''
        data, meta_data= self.ts.get_quote_endpoint(ticker)
        data.reset_index(inplace=True)
        data = data[columns]
        data.columns = ['price', 'date']
        data.set_index('date', inplace=True)
        return data

    def get_prices(self, tickers,columns=['05. price','07. latest trading day']):
        '''
        Returns a DataFrame of prices for a list of tickers on Alpha Vantage API  
        '''
        prices = pd.DataFrame()
        for ticker in tickers:
            ticker_prices = self.get_price(ticker, columns)
            ticker_prices.columns = [ticker]
            if ticker_prices.dropna().empty == False:
                prices = pd.concat([prices, ticker_prices], axis=1)
            else:
                print(f"{ticker} has no data!")
        return prices

    def get_rate(self, from_curr, to_curr='GBP', columns=['5. Exchange Rate', '6. Last Refreshed']):
        '''
        Returns the spot rate from Alpha Vantage API
        '''
        rate, metadata = self.fx.get_currency_exchange_rate(from_currency=from_curr, to_currency=to_curr)
        rate.reset_index(inplace=True)
        rate = rate[columns]
        rate.columns = ['rate', 'date']
        rate.set_index('date', inplace=True)
        rate.index = pd.to_datetime(rate.index).strftime('%Y-%m-%d')
        return rate

    def get_rates(self, from_currencies, to_curr='GBP', columns=['5. Exchange Rate', '6. Last Refreshed']):
        '''
        Returns a DataFrame of rates for a list of currencies on Alpha Vantage API  
        '''
        rates = pd.DataFrame()
        for curr in from_currencies:
            rate = self.get_rate(from_curr=curr, to_curr=to_curr, columns=columns)
            rate.columns = [curr]
            if rate.dropna().empty == False:
                rates = pd.concat([rates, rate], axis=1)
            else:
                print(f"{curr} has no data!")
        return rates