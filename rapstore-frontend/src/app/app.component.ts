import {Component, OnDestroy, OnInit} from '@angular/core';
import {BrowserIntegrationService} from './browser-integration.service';
import {Subscription} from 'rxjs/Subscription';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/take';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit, OnDestroy {

  username = '';
  is_logged_in$: Observable<boolean>;

  private $subscriptionExtension: Subscription;
  private $subscriptionHost: Subscription;

  protected extensionAvailable = true;
  protected nativeMessagingHostAvailable = true;

  constructor(protected authService: AuthService, private router: Router, private browserIntegrationService: BrowserIntegrationService) {}

  ngOnInit(): void {

    this.is_logged_in$ = this.authService.is_logged;
    this.username = this.authService.username();

    this.$subscriptionExtension = this.browserIntegrationService.isExtensionAvailable()
      .subscribe(updatedBool => { this.extensionAvailable = updatedBool; });

    this.$subscriptionHost = this.browserIntegrationService.isNativeMessagingHostAvailable()
      .subscribe(updatedBool => { this.nativeMessagingHostAvailable = updatedBool; });
  }

  ngOnDestroy(): void {
    this.$subscriptionExtension.unsubscribe();
    this.$subscriptionHost.unsubscribe();
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/']);
  }

}
