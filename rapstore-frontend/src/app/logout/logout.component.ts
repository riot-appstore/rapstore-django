import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import {AuthService} from '../auth.service';
import {Subscription} from 'rxjs/Subscription';
import {AppService} from '../appservice.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {
  // returnURL is only used when logout cant be accomplished successfully
  returnURL: string;

  private $subscriptionRoute: Subscription;

  constructor(protected authService: AuthService,
              private router: Router,
              private activatedRoute: ActivatedRoute,
              private appService: AppService) { }

  ngOnInit() {

    this.$subscriptionRoute = this.activatedRoute
      .queryParams
      .subscribe(params => {
        this.returnURL = params.returnURL || '/';
      });

    if (!this.authService.get_token()) {
      // dont show logout page if user is not logged in
      this.router.navigateByUrl('/');
    }

    if (this.appService.isBuilding()) {
      alert("There is a build process in the queue running, you can't log out now!");
      this.router.navigateByUrl(this.returnURL);
    }
    else {
      this.authService.logout();
      // dont use returnURL! we dont want to show pages which require authentification after the user logged out
      this.router.navigateByUrl('/');
    }
  }
}
