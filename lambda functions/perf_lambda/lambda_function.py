import PortfolioPerformance as pp
import os

def lambda_handler(event, context):

    BasketComposition = event.get('BasketComposition')
    Currency = event.get('Currency')
    api_key = "QGXhjiTiS0bcZSkW935sXu0B69xYutrqvUe5Bd2mfFJoII9qyOSrOB1V1XGM"
    start_date = event.get('StartDate')
    end_date = event.get('EndDate')

    ia = pp.Investment_Analysis(BasketComposition,Currency,api_key,start_date,end_date)
    results = ia.getPerformanceMetrics()

    return results