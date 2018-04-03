import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import {NguUtilityModule} from 'ngu-utility/dist';


import { AppComponent } from './app.component';
import { AppBrowserComponent } from './app-browser/app-browser.component';
import { AppRoutingModule } from './app-routing.module';
import { AppDetailComponent } from './app-detail/app-detail.component';
import { AppService } from './appservice.service';
import { AppBuildComponent } from './app-build/app-build.component';
import { BoardService } from './board.service';
import { AuthService } from './auth.service';
import { AuthGuard } from './auth-guard';
import { LoginComponent } from './login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { BoardSelectorComponent } from './board-selector/board-selector.component';
import { MissingComponentsLabelSectionComponent } from './missing-components-label-section/missing-components-label-section.component';
import {BrowserIntegrationService} from './browser-integration.service';
import { PageInstallInstructionBrowserIntegrationComponent } from './page-install-instruction-browser-integration/page-install-instruction-browser-integration.component';
import { AppUploaderComponent } from './app-uploader/app-uploader.component';
import { UserService } from './user.service';


@NgModule({
  declarations: [
    AppComponent,
    AppBrowserComponent,
    AppDetailComponent,
    AppBuildComponent,
    LoginComponent,
    NavbarComponent,
    BoardSelectorComponent,
    MissingComponentsLabelSectionComponent,
    PageInstallInstructionBrowserIntegrationComponent,
    AppUploaderComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    FormsModule,
    NguUtilityModule,
    AppRoutingModule,
    HttpModule
  ],
  providers: [AppService, BoardService, AuthService, AuthGuard, BrowserIntegrationService, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
