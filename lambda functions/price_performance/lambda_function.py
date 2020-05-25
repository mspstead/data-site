import PortfolioPerformance as pp
import os

def lambda_handler(event, context):

    BasketComposition = event.get('BasketComposition')
    Currency = event.get('Currency')
    #api_key = os.environ['API_KEY']
    api_key = '351047277amsh5508dafa91eec03p1f25c5jsndbe69efc68c2'
    start_date = event.get('StartDate')
    end_date = event.get('EndDate')

    ia = pp.Investment_Analysis(BasketComposition,Currency,api_key,start_date,end_date)
    results = ia.getPerformanceMetrics()

    return results

example_event = {
    "BasketComposition": [
        {"Identifier": "VWRL.L","Shares":40},
        {"Identifier": "VMID.L", "Shares": 30}
    ],
    "Currency": "GBP",
    "StartDate": "2019-10-01",
    "EndDate": "2020-05-17"

}

lambda_handler(example_event,'')