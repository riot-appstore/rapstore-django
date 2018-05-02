import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {AppBrowserComponent} from './app-browser/app-browser.component';
import {AppDetailComponent} from './app-detail/app-detail.component';
import {AppBuildComponent} from './app-build/app-build.component';
import {AppUploaderComponent} from './app-uploader/app-uploader.component';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {DeveloperComponent} from './developer/developer.component';
import {UserprofileComponent} from './userprofile/userprofile.component';
import {PageInstallInstructionBrowserIntegrationComponent} from './page-install-instruction-browser-integration/page-install-instruction-browser-integration.component';
import {PageInstallInstructionDragAndDropComponent} from './page-install-instruction-drag-and-drop/page-install-instruction-drag-and-drop.component';
import {AuthGuard} from './auth-guard';


const routes: Routes = [
  {path: '', component: AppBrowserComponent},
  {path: 'login', component: LoginComponent},
  {path: 'install-instruction-browser-integration', component: PageInstallInstructionBrowserIntegrationComponent},
  {path: 'install-instruction-drag-and-drop', component: PageInstallInstructionDragAndDropComponent},
  {path: 'app/:id', component: AppDetailComponent},
  {path: 'app/:id/build', component: AppBuildComponent},
  {path: 'upload', component: AppUploaderComponent},
  {path: 'signup', component: SignupComponent},
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
