import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {NguUtilityModule} from "ngu-utility/dist";


import { AppComponent } from './app.component';
import { AppBrowserComponent } from './app-browser/app-browser.component';
import { AppRoutingModule } from './/app-routing.module';
import { AppDetailComponent } from './app-detail/app-detail.component';
import { AppserviceService } from './appservice.service';


@NgModule({
  declarations: [
    AppComponent,
    AppBrowserComponent,
    AppDetailComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    NguUtilityModule,
    AppRoutingModule
  ],
  providers: [AppserviceService],
  bootstrap: [AppComponent]
})
export class AppModule { }
