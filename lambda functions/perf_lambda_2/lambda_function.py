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

# example_event = {
#     "BasketComposition": [
#         {"Identifier": "VWRL.L","Shares":40},
#         {"Identifier": "VMID.L", "Shares": 30},
#         {"Identifier": "VFEM.L", "Shares": 30}
#     ],
#     "Currency": "GBP",
#     "StartDate": "2020-09-01",
#     "EndDate": "2020-11-16"
# }
#
# lambda_handler(example_event,'')