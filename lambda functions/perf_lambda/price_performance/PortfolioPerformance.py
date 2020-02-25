import yfinance as yf
import requests as req
import datetime as dt
import pandas as pd


class Investment_Analysis:

    def __init__(self,BasketCompostion,BaseCurrency,start_date='',end_date=dt.datetime.today()):
        """
            :Parameters:
                BasketComposition : Dict
                    Object array containing stock/ETF ticker and shares in the following format,
                    [{'Identifier':'MSFT', 'Shares':10},{'Identifier':'AAPL', 'Shares':20}]

                BaseCurrency : str
                    Base Currency code, eg. USD, basket constituents with differing currency codes will be FX'd

                start_date : date
                    Start of time range for performance metrics as python datetime object
                end_date : date
                    End date, default is the current date as python datetime object.
        """
        self.BaseCurrency = BaseCurrency
        self.BasketComposition = BasketCompostion
        self.end_date = end_date

        #if no start date given, go back one week
        if start_date=='':
            self.start_date = dt.datetime.today() - dt.timedelta(days=7)
        else:
            self.start_date = start_date


    def _getHistoricalFXRates(self):
        """
        Uses the exchange rates API to get historical FX rates for the base currency
        Returns a pandas dataframe of currency rates based on the base currency and start/end dates provided at class creation.
        """

        start_date = self.start_date.strftime('%Y-%m-%d')
        end_date = self.end_date.strftime('%Y-%m-%d')

        rates_url = 'https://api.exchangeratesapi.io/history?start_at='+start_date+'&end_at='+end_date+'&base='+self.BaseCurrency
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
        """Uses the yFinanace module to get pricing data for each equity returns a dataframe of prices"""
        price_dfs = []
        for id in self.BasketComposition:
            identifier = id.get('Identifier')
            shares = id.get('Shares')

            equity = yf.Ticker(identifier)
            currency_code = equity.info.get('currency')

            prices_df = equity.history(start=self.start_date, end=self.end_date)
            prices_df['Identifier'] = identifier
            prices_df['Shares'] = shares
            prices_df['CurrencyCode'] = currency_code

            prices_df.reset_index(inplace=True)
            price_dfs.append(prices_df)

        final_prices_df = pd.concat(price_dfs)
        return final_prices_df


    def getPerformanceMetrics(self):
        """calculates and returns a portfolio performance measure"""

        fx_rates = self._getHistoricalFXRates()
        prices = self._getEquitiesHistory()

        constituents = pd.merge(prices,fx_rates,'inner',left_on=['Date','CurrencyCode'],right_on=['CloseDate','CurrencyCode'])
        constituents = constituents.drop(['CloseDate','Open', 'High', 'Low','Volume','Dividends','Stock Splits'],axis=1)

        constituents['constituent_mcap'] = constituents['Close'] * constituents['FXRate'] * constituents['Shares']

        daily_market_caps = constituents.groupby('Date')['constituent_mcap'].sum().reset_index()
        daily_market_caps = daily_market_caps.rename(columns={'constituent_mcap':'Total_Market_Cap'})

        daily_market_caps['Daily_Return'] = daily_market_caps['Total_Market_Cap'].pct_change() * 100
        daily_market_caps['Cumulative_Return'] = daily_market_caps['Daily_Return'].cumsum()

        performance = {'BasketPerformance':daily_market_caps.to_dict(orient='records'),
                       'EquityDetails':prices.to_dict(orient='records')}

        return performance
