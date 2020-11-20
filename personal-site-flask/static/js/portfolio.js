function get_performance(composition){
    console.log(JSON.stringify(composition))

    var api = "https://c1h9ea61fi.execute-api.eu-west-1.amazonaws.com/deployment"
    var details = {
        method: 'POST',
        mode:'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(composition)
    }

    fetch(api, details)
    .then((response) => response.json())
    .then(data => basket_performance(data)
    );

    var chart1 = Highcharts.chart('chart1', {
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

      var chart2 = Highcharts.chart('chart2', {
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

      chart1.showLoading()
      chart2.showLoading()
};

function basket_performance(basket_data){

    var performance = basket_data["BasketPerformance"]
    var equity_history = basket_data["EquityDetails"]
    var current_weightings = basket_data["Current_Weightings"]

    for (var i=0; i<current_weightings.length; i=i+1){
        id = current_weightings[i]["Identifier"]
        console.log(id)
        weighting = current_weightings[i]["Weightings"]
        document.getElementById(id).innerHTML = weighting
    }

    var perfRows = []
    var chartData = []
    var daily_return_chart_data = []
    for(var i=0; i<performance.length; i++) {

        var epoch_time = performance[i]['epoch_time']
        var cum_return = performance[i]['Cumulative_Return']
        var chartDataPoint = [epoch_time,cum_return]

        var AsAtDate = performance[i]['Date']
        var daily_return = performance[i]['Daily_Return']
        var dailyChartDataPoint = [epoch_time,daily_return]

        chartData.push(chartDataPoint)
        daily_return_chart_data.push(dailyChartDataPoint)
        perfRows.push({Date: AsAtDate, Daily_Return:daily_return, Cumulative_Return:cum_return})
    }

    Highcharts.chart('chart1', {
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
        name: 'ETF Portfolio',
        data: chartData
        }]
      });

      Highcharts.chart('chart2', {
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
          name: 'ETF Portfolio',
          data: daily_return_chart_data
          }]
        });
};