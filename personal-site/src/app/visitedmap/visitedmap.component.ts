import { Component, OnInit } from '@angular/core';
import { MapChart } from 'angular-highcharts';
import worldMap from 'src/assets/worldMap';

@Component({
  selector: 'app-visitedmap',
  templateUrl: './visitedmap.component.html',
  styleUrls: ['./visitedmap.component.css']
})
export class VisitedmapComponent implements OnInit {
  mapChart: MapChart
  constructor() { }
  
  ngOnInit(): void {
    let chartData = [{ code3: "ABW", z: 105 }, { code3: "AFG", z: 35530 }];
    this.mapChart = new MapChart({
      plotOptions: {map:{nullColor:'#ededed'}},
      mapNavigation: {
        enabled: true
      },
      chart: {
                borderWidth: 1,
                map: worldMap,
                backgroundColor:'#7DD2FF',
                borderColor:'#FFFFF'
            },
            title: {
              text: 'Countries Travelled'
          },
          legend: {
              enabled: false
          },
      
          series: [{
              type:'map',
              name: 'Country',
              data: [
                  ['co', 1],
                  ['gb', 1],
                  ['us', 1],
                  ['no', 1],
                  ['in', 1],
                  ['jp', 1],
                  ['fr', 1],
                  ['it', 1],
                  ['bg', 1],
                  ['hk', 1],
                  ['au', 1],
                  ['at', 1],
                  ['be', 1],
                  ['de', 1],
                  ['gr', 1],
                  ['ie', 1],
                  ['li', 1],
                  ['lu', 1],
                  ['pt', 1],
                  ['es', 1],
                  ['ch', 1],
                  ['nl', 1],
                  ['va', 1],
                  ['th', 1],
                  ['vn', 1],
                  ['cr', 1],
                  ['ni', 1],
                  ['bo', 1],
                  ['cl', 1],
                  ['ec', 1],
                  ['pe', 1],
                  ['id', 1]
              ],
              color:'#FF9700',
              dataLabels: {
                  enabled: false,
                  color: '#FFFFF',
                  formatter: function () {
                      if (this.point.value) {
                          return this.point.name;
                      }
                  }
              },
              tooltip: {
                headerFormat: '',
                  pointFormat: '{point.name}'
              }
          }]
      });
  }
}
