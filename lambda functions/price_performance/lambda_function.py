import PortfolioPerformance as pp
import datetime as dt

def lambda_handler(event, context):

    BasketComposition = event.get('BasketComposition')
    Currency = event.get('Currency')

    start_date = dt.datetime.strptime(event.get('StartDate'),'%Y-%m-%d')
    end_date = dt.datetime.strptime(event.get('EndDate'),'%Y-%m-%d')

    ia = pp.Investment_Analysis(BasketComposition,Currency,start_date,end_date)
    results = ia.getPerformanceMetrics()

    return results


event = {
    "BasketComposition": [
        {"Identifier": "MSFT","Shares":10},
        {"Identifier": "AAPL","Shares":20}],
    "Currency": "GBP",
    "StartDate": "2018-01-01",
    "EndDate": "2020-02-14"

}
res = lambda_handler(event,'')
print(res)