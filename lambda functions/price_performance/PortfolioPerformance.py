import requests as req
import time
import pandas as pd
import numpy as np
import datetime as dt

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
        """Uses the alphavantage api to get pricing data for each equity returns a dataframe of prices"""

        price_api = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"
        currency_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }

        pattern = '%Y-%m-%d'
        epoch_start_time = int(time.mktime(time.strptime(self.start_date, pattern)))
        epoch_end_time = int(time.mktime(time.strptime(self.end_date, pattern)))

        dfs = []
        for id in self.BasketComposition:

            identifier = id.get('Identifier')
            shares = id.get('Shares')

            params = {"frequency": "1d",
                      "filter": "history",
                      "period1": epoch_start_time,
                      "period2": epoch_end_time,
                      "symbol": identifier}

            currency_params = {"region":"US","symbol":identifier}

            equity_history = pd.DataFrame.from_dict(req.get(price_api,headers=headers,params=params).json().get("prices"))
            currency_code = req.get(currency_url,headers=headers,params=currency_params).json().get("price").get("currency")
            prices_df = equity_history
            prices_df['Identifier'] = identifier
            prices_df['Shares'] = shares
            prices_df['CurrencyCode'] = currency_code
            prices_df = prices_df[['date','close','Identifier', 'Shares', 'CurrencyCode','open']]
            prices_df = prices_df.rename(columns={'date':'Date','close':'Close'})
            prices_df['Date'] = pd.to_datetime(prices_df['Date'],unit='s').dt.date.astype('datetime64')
            prices_df['Close'] = prices_df['Close'].astype(float)
            dfs.append(prices_df[1:])

        final_prices_df = pd.concat(dfs)

        return final_prices_df


    def getPerformanceMetrics(self):
        """calculates and returns a portfolio performance measure"""

        fx_rates = self._getHistoricalFXRates()
        prices = self._getEquitiesHistory()
        print(prices[prices['Date']==prices['Date'].max])
        constituents = pd.merge(prices,fx_rates,'inner',left_on=['Date','CurrencyCode'],right_on=['CloseDate','CurrencyCode'])
        constituents = constituents.drop(['CloseDate'],axis=1)
        constituents['constituent_mcap'] = constituents['Close'] * constituents['FXRate'] * constituents['Shares']
        # Remove marketcap dates with missing prices using the constituent count for each of those days
        counts_df = pd.DataFrame(data=constituents.groupby('Date')['Identifier'].count())
        counts_df = counts_df.reset_index()
        counts_df['Date'] = pd.to_datetime(counts_df['Date'])

        daily_market_caps = pd.DataFrame(constituents.groupby('Date')['constituent_mcap'].sum().reset_index())
        daily_market_caps = daily_market_caps.rename(columns={'constituent_mcap': 'Total_Market_Cap'})

        daily_market_caps = pd.merge(left=daily_market_caps, right=counts_df, on='Date', how='inner')
        num_constituents = len(constituents['Identifier'].unique())

        daily_market_caps = daily_market_caps[daily_market_caps['Identifier'] == num_constituents]
        del daily_market_caps['Identifier']

        daily_market_caps['Daily_Return'] = daily_market_caps['Total_Market_Cap'].pct_change() * 100
        daily_market_caps['Cumulative_Return'] = daily_market_caps['Daily_Return'].cumsum()
        daily_market_caps.fillna(value=0,inplace=True)

        daily_market_caps['Date'] = daily_market_caps['Date'].dt.strftime('%Y-%m-%d')
        prices['Date'] = prices['Date'].dt.strftime('%Y-%m-%d')

        daily_market_caps['epoch_time'] = pd.to_datetime(daily_market_caps['Date']).astype(np.int64) // 10**6
        prices['epoch_time'] = pd.to_datetime(prices['Date']).astype(np.int64) // 10**6

        daily_market_caps = daily_market_caps.sort_values(by='epoch_time', ascending=False)
        prices = prices.sort_values(by='epoch_time', ascending=False)
        current_day_mcap = daily_market_caps.iloc[0]['Total_Market_Cap']
        final_weightings = constituents.sort_values(by='Date', ascending=False)
        final_weightings['Weightings'] = (final_weightings.iloc[0:3]['constituent_mcap']/current_day_mcap)*100
        final_weightings = final_weightings.iloc[0:3][['Identifier','Weightings']]
        print(daily_market_caps)
        performance = {'BasketPerformance':daily_market_caps.to_dict(orient='records'),
                       'EquityDetails':prices.to_dict(orient='records'),
                       'Current_Weightings':final_weightings.to_dict(orient='records')}

        return performance
