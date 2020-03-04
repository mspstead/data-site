import PortfolioPerformance as pp
import os

def lambda_handler(event, context):

    BasketComposition = event.get('BasketComposition')
    Currency = event.get('Currency')
    api_key = os.environ['API_KEY']
    start_date = event.get('StartDate')
    end_date = event.get('EndDate')

    ia = pp.Investment_Analysis(BasketComposition,Currency,api_key,start_date,end_date)
    results = ia.getPerformanceMetrics()

    return results

example_event = {
    "BasketComposition": [
        {"Identifier": "VFEM.L","Shares":10},
        {"Identifier": "VWRL.L","Shares":40},
        {"Identifier": "VMID.L","Shares":30}
        ],
    "Currency": "GBP",
    "StartDate": "2019-10-01",
    "EndDate": "2020-02-22"

}