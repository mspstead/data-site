import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutComponent } from './about/about.component'
import { BlogListComponent } from './blog-list/blog-list.component'
import { FitbitDataComponent } from './fitbit-data/fitbit-data.component'
import { PortfolioAnalyticsComponent } from './portfolio-analytics/portfolio-analytics.component'
import { YfinanceComponent } from './yfinance/yfinance.component'
import { PortfolioOptimisationComponent } from './portfolio-optimisation/portfolio-optimisation.component'
import { AppComponent } from './app.component'
import { VisitedmapComponent } from './visitedmap/visitedmap.component'


const routes: Routes = [
        { path: 'about', component: AboutComponent},
        { path: '', component: BlogListComponent},
        { path: 'blog', component: BlogListComponent},
        { path: 'blog/fitbit', component: FitbitDataComponent},
        { path: 'blog/yfinance', component: YfinanceComponent},
        { path: 'portfolioanalytics', component: PortfolioAnalyticsComponent },
        { path: 'visitedcountries', component:VisitedmapComponent },
        { path: 'blog/portfoliopt', component: PortfolioOptimisationComponent},
      ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [AboutComponent,BlogListComponent,
  FitbitDataComponent,YfinanceComponent,
  PortfolioAnalyticsComponent,VisitedmapComponent,PortfolioOptimisationComponent]
