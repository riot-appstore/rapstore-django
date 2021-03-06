import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {AppBrowserComponent} from './app-browser/app-browser.component';
import {AppDetailComponent} from './app-detail/app-detail.component';
import {AppBuildComponent} from './app-build/app-build.component';
import {AppUploaderComponent} from './app-uploader/app-uploader.component';
import {LoginComponent} from './login/login.component';
import {LogoutComponent} from './logout/logout.component';
import {SignupComponent} from './signup/signup.component';
import {DeveloperComponent} from './developer/developer.component';
import {UserprofileComponent} from './userprofile/userprofile.component';
import {PageInstallInstructionBrowserIntegrationComponent} from './page-install-instruction-browser-integration/page-install-instruction-browser-integration.component';
import {PageInstallInstructionDragAndDropComponent} from './page-install-instruction-drag-and-drop/page-install-instruction-drag-and-drop.component';
import {ImprintComponent} from './imprint/imprint.component';
import {AboutComponent} from './about/about.component';


const routes: Routes = [
  {path: '', component: AppBrowserComponent},
  {path: 'signup', component: SignupComponent},
  {path: 'login', component: LoginComponent},
  {path: 'logout', component: LogoutComponent},

  {path: 'install-instruction-browser-integration', component: PageInstallInstructionBrowserIntegrationComponent},
  {path: 'install-instruction-drag-and-drop', component: PageInstallInstructionDragAndDropComponent},
  {path: 'imprint', component: ImprintComponent},
  {path: 'about', component: AboutComponent},

  {path: 'app', component: AppBrowserComponent},
  {path: 'app/:id', component: AppDetailComponent},
  {path: 'app/:id/build', component: AppBuildComponent},

  {path: 'upload', component: AppUploaderComponent},
  {path: 'user-profile', component: UserprofileComponent},
  {path: 'developer', component: DeveloperComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  declarations: [],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
