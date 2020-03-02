import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AlertModule } from 'ngx-bootstrap';
import { HttpClientModule } from '@angular/common/http'
 
import { AppRoutingModule, routingComponents} from './app-routing.module';
import { AppComponent } from './app.component';
import { AgGridModule } from 'ag-grid-angular';
import { ChartModule, HIGHCHARTS_MODULES } from 'angular-highcharts';
import { VisitedmapComponent } from './visitedmap/visitedmap.component';
import * as highmaps from 'highcharts/modules/map.src';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
    VisitedmapComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AlertModule.forRoot(),
    AgGridModule.withComponents([]),
    ChartModule,
    HttpClientModule
  ],
  providers: [{provide: HIGHCHARTS_MODULES, useFactory: () => [highmaps]}],
  bootstrap: [AppComponent]
})
export class AppModule { }
