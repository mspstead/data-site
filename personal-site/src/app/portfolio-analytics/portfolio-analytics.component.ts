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
  chart;
  chartData = [];
  rowData: any;

  columnPriceDefs=[];
  portfolioresults: {};
  priceData;
  rowPriceData: any;
  performanceData=[];

  vfem_weight=12;
  vmid_weight=23;
  vwrl_weight=66;


  constructor(private portfolioanalytics: PortfolioAnalyticsService) { }

  getPortfolioData(){
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

    var BasketPerformance = this.portfolioresults['BasketPerformance']
    var perfRows = []

    for(var i=0; i<BasketPerformance.length; i++) {
        
        var epoch_time = BasketPerformance[i]['epoch_time']
        var cum_return = BasketPerformance[i]['Cumulative_Return']
        var chartDataPoint = [epoch_time,cum_return]
        
        var AsAtDate = BasketPerformance[i]['Date']
        var daily_return = BasketPerformance[i]['Daily_Return']

        this.chartData.push(chartDataPoint)
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
        name: 'USD to EUR',
        data: this.chartData
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

    this.getPortfolioData()

  }
}
