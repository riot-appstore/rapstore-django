import {Component, OnDestroy, OnInit, HostListener} from '@angular/core';
import {BrowserIntegrationService} from './browser-integration.service';
import {Subscription} from 'rxjs';
import {AuthService} from './auth.service';
import {UserService} from './user.service';
import {FeedbackService} from './feedback.service';
import {Router} from '@angular/router';
import {User} from './models';
import {AppService} from './appservice.service';
import {environment} from '../environments/environment';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit, OnDestroy {

  private user: User;
  protected currentURL: string;

  private $subscriptionExtension: Subscription;
  private $subscriptionHost: Subscription;
  private $subscriptionRouter: Subscription;

  protected extensionAvailable = true;
  protected nativeMessagingHostAvailable = true;
  protected appVersion: string = environment.VERSION;

  constructor(protected authService: AuthService,
              private router: Router,
              private browserIntegrationService: BrowserIntegrationService,
              private userService: UserService,
              private feedbackService: FeedbackService,
              private appService: AppService) {
  }


  ngOnInit(): void {

    this.$subscriptionRouter = this.router.events.subscribe(event => {
      this.currentURL = this.router.url;
    });

    this.$subscriptionExtension = this.browserIntegrationService.isExtensionAvailable()
      .subscribe(updatedBool => {
        this.extensionAvailable = updatedBool;
      });

    this.$subscriptionHost = this.browserIntegrationService.isNativeMessagingHostAvailable()
      .subscribe(updatedBool => {
        this.nativeMessagingHostAvailable = updatedBool;
      });

    this.fetch_user();

    this.authService.userChangeEvent.subscribe(value => {
      this.fetch_user();
    });
  }

  fetch_user() {
    if (this.authService.get_token()) {
      this.userService.get()
        .subscribe(user => this.user = user);
    }
    else {
      this.user = null;
    }
  }

  get_username() {
    return this.user.username;
  }

  is_developer() {
    return this.user.is_dev;
  }

  ngOnDestroy(): void {
    this.$subscriptionExtension.unsubscribe();
    this.$subscriptionHost.unsubscribe();
  }

  @HostListener('window:beforeunload', ['$event'])
  doSomething($event) {
    if(this.appService.isBuilding()) $event.returnValue='There is a pending build in the queue. Do you really want to leave?';
  }
}
