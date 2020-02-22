import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AlertModule } from 'ngx-bootstrap';

import { AppRoutingModule, routingComponents} from './app-routing.module';
import { AppComponent } from './app.component';
import { BlogListComponent } from './blog-list/blog-list.component';
import { FitbitDataComponent } from './fitbit-data/fitbit-data.component';
import { AgGridModule } from 'ag-grid-angular';
import { YfinanceComponent } from './yfinance/yfinance.component';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
    BlogListComponent,
    FitbitDataComponent,
    YfinanceComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AlertModule.forRoot(),
    AgGridModule.withComponents([])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
