import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { AppBrowserComponent } from './app-browser/app-browser.component';
import { AppDetailComponent } from './app-detail/app-detail.component';
import { AppBuildComponent } from './app-build/app-build.component';


const routes: Routes = [
  { path: '', component: AppBrowserComponent },
  { path: 'detail/:id', component: AppDetailComponent },
  { path: 'build/:id', component: AppBuildComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  declarations: [],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
