import { Component, OnInit } from '@angular/core';
import { Chart, HIGHCHARTS_MODULES} from 'angular-highcharts';
import { PortfolioAnalyticsService } from './portfolio-analytics.service'

@Component({
  selector: 'app-portfolio-analytics',
  templateUrl: './portfolio-analytics.component.html',
  styleUrls: ['./portfolio-analytics.component.css'],
  providers: [PortfolioAnalyticsService]
})
export class PortfolioAnalyticsComponent implements OnInit {
  
  columnDefs=[];
  rowData=[];
  chart;

  columnPriceDefs=[];
  rowPriceData=[];
  portfolioresults;
  priceData=[];
  performanceData=[];


  constructor(private portfolioanalytics: PortfolioAnalyticsService) { }

  getPortfolioData(){
    var Basket = {
      "BasketComposition": [
          {"Identifier": "VFEM.L","Shares":10},
          {"Identifier": "VWRL.L","Shares":40},
          {"Identifier": "VMID.L","Shares":30}
          ],
      "Currency": "GBP",
      "StartDate": "2019-10-01",
      "EndDate": "2020-02-22"
  
    }
    this.portfolioanalytics.getPortfolioData(Basket)
      .subscribe(result => {this.portfolioresults = result},
              error => console.log(error))
    console.log(this.portfolioresults)
  }

  plotCumulativeReturnChart(){

    var chartData = [[
      1569888000000,
      0.7537
    ],
    [
      1569974400000,
      0.7559
    ]]

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
        data: chartData
        }]
      });

  }

  ngOnInit(): void {
    this.getPortfolioData()
    this.plotCumulativeReturnChart()

    this.columnDefs = [
      {headerName: 'Date', field: 'Date' },
      {headerName: 'Daily Return %', field: 'Daily_Return' },
      {headerName: 'Cumulative Return %', field: 'Cumulative_Return'}
    ];

    this.rowData = [
      { Date: '2019-10-01', Daily_Return: 0, Cumulative_Return: 35000 },
      { Date: '2019-10-02', Daily_Return: 0.123, Cumulative_Return: 0.123 },
      { Date: '2019-10-03', Daily_Return: 0.153, Cumulative_Return: 0.276 }
    ];

    this.columnPriceDefs = [
      {headerName: 'Date', field: 'Date' },
      {headerName:'Ric', field: 'Identifier'},
      {headerName:'Open Price', field:'open'},
      {headerName: 'Close Price', field: 'Close'}
    ];

    this.rowPriceData = [
      { Date: '2019-10-01', Identifier: 'VFEM.L', open: 45.43, Close: 46.24 },
      { Date: '2019-10-01', Identifier: 'VFEM.L', open: 45.43, Close: 46.24 },
      { Date: '2019-10-01', Identifier: 'VFEM.L', open: 45.43, Close: 46.24 }
    ];
  }
}
