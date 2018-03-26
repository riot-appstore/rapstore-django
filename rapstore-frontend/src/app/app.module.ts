import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import {NguUtilityModule} from "ngu-utility/dist";


import { AppComponent } from './app.component';
import { AppBrowserComponent } from './app-browser/app-browser.component';
import { AppRoutingModule } from './/app-routing.module';
import { AppDetailComponent } from './app-detail/app-detail.component';
import { AppserviceService } from './appservice.service';
import { AppBuildComponent } from './app-build/app-build.component';
import { BoardService } from './board.service';
import { AuthService } from './auth.service';
import { AuthGuard } from './auth-guard';


@NgModule({
  declarations: [
    AppComponent,
    AppBrowserComponent,
    AppDetailComponent,
    AppBuildComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    FormsModule,
    NguUtilityModule,
    AppRoutingModule,
    HttpModule
  ],
  providers: [AppserviceService, BoardService, AuthService, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
