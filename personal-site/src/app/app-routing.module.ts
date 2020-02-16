import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutComponent } from './about/about.component'
import { BlogListComponent } from './blog-list/blog-list.component'
import { FitbitDataComponent } from './fitbit-data/fitbit-data.component'
import { InvestmentsComponent } from './investments/investments.component'
import { AppComponent } from './app.component'


const routes: Routes = [
        { path: 'about', component: AboutComponent},
        { path: '', component: BlogListComponent},
        { path: 'blog', component: BlogListComponent},
        { path: 'blog/fitbit', component: FitbitDataComponent},
        { path: 'blog/investments', component: InvestmentsComponent}
      ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [AboutComponent,BlogListComponent,FitbitDataComponent,InvestmentsComponent]
