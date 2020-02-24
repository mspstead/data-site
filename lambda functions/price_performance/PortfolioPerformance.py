import requests as req
import datetime as dt
import pandas as pd
import numpy as np

class Investment_Analysis:

    def __init__(self,BasketCompostion,BaseCurrency,api_key,start_date=dt.datetime.today() - dt.timedelta(days=7),end_date=dt.datetime.today()):
        """
            :Parameters:
                BasketComposition : Dict
                    Object array containing stock/ETF ticker and shares in the following format,
                    [{'Identifier':'MSFT', 'Shares':10},{'Identifier':'AAPL', 'Shares':20}]

                BaseCurrency : str
                    Base Currency code, eg. USD, basket constituents with differing currency codes will be FX'd

                api_key : str
                    API KEY for https://www.worldtradingdata.com/

                start_date : date
                    Start of time range for performance metrics as python datetime object

                end_date : date
                    End date, default is the current date as python datetime object.

        """
        self.BaseCurrency = BaseCurrency
        self.BasketComposition = BasketCompostion
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date



    def _getHistoricalFXRates(self):
        """
        Uses the exchange rates API to get historical FX rates for the base currency
        Returns a pandas dataframe of currency rates based on the base currency and start/end dates provided at class creation.
        """

        rates_url = 'https://api.exchangeratesapi.io/history?start_at='+self.start_date+'&end_at='+self.end_date+'&base='+self.BaseCurrency
        rates_json = req.get(rates_url).json().get('rates')

        dates=[]
        for date in rates_json:
            date_rates = rates_json.get(date)
            for rate in date_rates:
                dates.append([dt.datetime.strptime(date,'%Y-%m-%d'),rate,date_rates.get(rate)])

        rates_df = pd.DataFrame(data=dates,columns=['CloseDate','CurrencyCode','FXRate'])
        rates_df = rates_df.sort_values(by='CloseDate')

        return rates_df

    def _getEquitiesHistory(self):
        """Uses the worldtradingdata api to get pricing data for each equity returns a dataframe of prices"""

        historical_price_api = "https://api.worldtradingdata.com/api/v1/history"
        latest_info_api = "https://api.worldtradingdata.com/api/v1/stock"

        dfs = []
        for id in self.BasketComposition:

            identifier = id.get('Identifier')
            shares = id.get('Shares')

            params = {
                'symbol': identifier,
                'api_token': self.api_key,
                'date_from':self.start_date,
                'date_to':self.end_date
            }

            equity_history = pd.DataFrame.from_dict(req.get(historical_price_api,params=params).json().get('history'),orient='index')
            currency_code = req.get(latest_info_api,params=params).json().get('data')[0].get('currency')

            prices_df = equity_history
            prices_df['Identifier'] = identifier
            prices_df['Shares'] = shares
            prices_df['CurrencyCode'] = currency_code
            prices_df.reset_index(inplace=True)
            prices_df = prices_df.rename(columns={'index':'Date','close':'Close'})

            prices_df['Date'] = pd.to_datetime(prices_df['Date'])
            prices_df['Close'] = prices_df['Close'].astype(float)

            dfs.append(prices_df)

        final_prices_df = pd.concat(dfs)

        return final_prices_df


    def getPerformanceMetrics(self):
        """calculates and returns a portfolio performance measure"""

        fx_rates = self._getHistoricalFXRates()
        prices = self._getEquitiesHistory()

        constituents = pd.merge(prices,fx_rates,'inner',left_on=['Date','CurrencyCode'],right_on=['CloseDate','CurrencyCode'])
        constituents = constituents.drop(['CloseDate','open', 'high', 'low','volume'],axis=1)

        constituents['constituent_mcap'] = constituents['Close'] * constituents['FXRate'] * constituents['Shares']

        daily_market_caps = constituents.groupby('Date')['constituent_mcap'].sum().reset_index()
        daily_market_caps = daily_market_caps.rename(columns={'constituent_mcap':'Total_Market_Cap'})

        daily_market_caps['Daily_Return'] = daily_market_caps['Total_Market_Cap'].pct_change() * 100
        daily_market_caps['Cumulative_Return'] = daily_market_caps['Daily_Return'].cumsum()
        daily_market_caps.fillna(value=0,inplace=True)

        daily_market_caps['Date'] = daily_market_caps['Date'].dt.strftime('%Y-%m-%d')
        prices['Date'] = prices['Date'].dt.strftime('%Y-%m-%d')

        daily_market_caps['epoch_time'] = pd.to_datetime(daily_market_caps['Date']).astype(np.int64) // 10**6
        prices['epoch_time'] = pd.to_datetime(prices['Date']).astype(np.int64) // 10**6

        performance = {'BasketPerformance':daily_market_caps.to_dict(orient='records'),
                       'EquityDetails':prices.to_dict(orient='records')}

        return performance
