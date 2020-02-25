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