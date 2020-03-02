import { Component, OnInit } from '@angular/core';
import { Chart } from 'angular-highcharts';
import { PortfolioAnalyticsService } from './portfolio-analytics.service'
import { AgGridModule } from 'ag-grid-angular';

@Component({
  selector: 'app-portfolio-analytics',
  templateUrl: './portfolio-analytics.component.html',
  styleUrls: ['./portfolio-analytics.component.css'],
  providers: [PortfolioAnalyticsService]
})
export class PortfolioAnalyticsComponent implements OnInit {
  
  columnDefs=[];
  chart: Chart;
  dailychart: Chart;
  chartData = [];
  daily_return_chart_data=[];
  rowData: any;

  columnPriceDefs=[];
  portfolioresults: {};
  priceData;
  rowPriceData: any;
  performanceData=[];

  vfem_weight;
  vmid_weight;
  vwrl_weight;


  constructor(private portfolioanalytics: PortfolioAnalyticsService) { }

  getPortfolioData(){

    this.chart.ref$.subscribe((res:any)=>{ res.showLoading(); })
    this.dailychart.ref$.subscribe((res:any)=>{ res.showLoading(); })

    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    var today = [year, month, day].join('-');

    console.log(today)
    var Basket = {
      "BasketComposition": [
          {"Identifier": "VFEM.L","Shares":7},
          {"Identifier": "VWRL.L","Shares":24},
          {"Identifier": "VMID.L","Shares":28}
          ],
      "Currency": "GBP",
      "StartDate": "2019-10-01",
      "EndDate": today
    }
    this.portfolioanalytics.getPortfolioData(Basket)
      .subscribe(result => {this.portfolioresults = result, 
                            this.addReturnData(),
                            this.addPriceTableData()                   
      },
              error => console.log(error))
  }

  addReturnData(){
    var currentWeightings = this.portfolioresults['Current_Weightings']

    for (var item=0; item<currentWeightings.length; item++){
        if (currentWeightings[item]['Identifier']=='VFEM.L'){
            this.vfem_weight=currentWeightings[item]['Weightings'].toFixed(2)
        }
        if (currentWeightings[item]['Identifier']=='VWRL.L'){
          this.vwrl_weight=currentWeightings[item]['Weightings'].toFixed(2)
        }
        if (currentWeightings[item]['Identifier']=='VMID.L'){
          this.vmid_weight=currentWeightings[item]['Weightings'].toFixed(2)
        }
    }

    var BasketPerformance = this.portfolioresults['BasketPerformance']
    var perfRows = []

    for(var i=0; i<BasketPerformance.length; i++) {
        
        var epoch_time = BasketPerformance[i]['epoch_time']
        var cum_return = BasketPerformance[i]['Cumulative_Return']
        var chartDataPoint = [epoch_time,cum_return]
        
        var AsAtDate = BasketPerformance[i]['Date']
        var daily_return = BasketPerformance[i]['Daily_Return']
        var dailyChartDataPoint = [epoch_time,daily_return]

        this.chartData.push(chartDataPoint)
        this.daily_return_chart_data.push(dailyChartDataPoint)
        perfRows.push({Date: AsAtDate, Daily_Return:daily_return, Cumulative_Return:cum_return})

    }

    this.rowData = perfRows;
    
    this.chart = new Chart({
      chart: {
        zoomType: 'x'
      },
      title: {
        text: 'ETF Portfolio Cumulative Performance to Date'
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        title: {
          text: '% Change'
        }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          marker: {
            radius: 2
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
          threshold: null
        }
      },
      series: [{
        type: 'area',
        name: 'portfolio',
        data: this.chartData
        }]
      });

      this.dailychart = new Chart({
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'ETF Portfolio Daily Return'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: '% Change'
          }
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          area: {
            marker: {
              radius: 2
            },
            lineWidth: 1,
            states: {
              hover: {
                lineWidth: 1
              }
            },
            threshold: null
          }
        },
        series: [{
          type: 'line',
          name: 'portfolio',
          data: this.daily_return_chart_data
          }]
        });
  }

  addPriceTableData() {

    var priceData = this.portfolioresults['EquityDetails']
    var prices = []
    for(var i=0; i<priceData.length; i++) {

      var AsAtDate = priceData[i]['Date'];
      var Ric = priceData[i]['Identifier']
      var openPrice = priceData[i]['open']
      var closePrice = priceData[i]['Close']

      prices.push({Date: AsAtDate, Identifier: Ric, open:openPrice, Close: closePrice})
    }
    this.rowPriceData = prices;
  }

  ngOnInit(): void {

    this.vfem_weight = 0.0
    this.vmid_weight = 0.0
    this.vwrl_weight = 0.0

    this.columnDefs = [
      {headerName: 'Date', field: 'Date', filter: "agTextColumnFilter", resizable: true },
      {headerName: 'Daily Return %', field: 'Daily_Return', filter: "agNumberColumnFilter", resizable: true },
      {headerName: 'Cumulative Return %', field: 'Cumulative_Return', filter: "agNumberColumnFilter", resizable: true}
    ];

    this.columnPriceDefs = [
      {headerName: 'Date', field: 'Date', filter:"agTextColumnFilter",resizable: true },
      {headerName:'Ric', field: 'Identifier', filter: "agTextColumnFilter",resizable: true},
      {headerName:'Open Price', field:'open', filter: "agNumberColumnFilter",resizable: true},
      {headerName: 'Close Price', field: 'Close', filter: "agNumberColumnFilter",resizable: true}
    ];

    this.chart = new Chart({
      chart: {
        zoomType: 'x'
      },
      title: {
        text: 'ETF Portfolio Cumulative Performance to Date'
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        title: {
          text: '% Change'
        }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          marker: {
            radius: 2
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
          threshold: null
        }
      },
      series: [{
        type: 'area',
        name: 'portfolio',
        data: []
        }]
      });

      this.dailychart = new Chart({
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'ETF Portfolio Daily Return'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: '% Change'
          }
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          area: {
            marker: {
              radius: 2
            },
            lineWidth: 1,
            states: {
              hover: {
                lineWidth: 1
              }
            },
            threshold: null
          }
        },
        series: [{
          type: 'line',
          name: 'portfolio',
          data: []
          }]
        });

    this.getPortfolioData()

  }
}
