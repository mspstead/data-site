import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutComponent } from './about/about.component'
import { BlogListComponent } from './blog-list/blog-list.component'
import { AppComponent } from './app.component'


const routes: Routes = [
        { path: 'about', component: AboutComponent},
        { path: '', component: BlogListComponent}
      ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [AboutComponent,BlogListComponent]
