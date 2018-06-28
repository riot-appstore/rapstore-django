import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {User} from '../models';
import {AppService} from '../appservice.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {
  private user: User;

  constructor(protected authService: AuthService,
              private router: Router,
              private appService: AppService) { }

  ngOnInit() {

    if (!this.authService.get_token()) {
      // dont show logout page if user is not logged in
      this.router.navigateByUrl('/');
    }

    if (this.appService.isBuilding()) {
      alert("There is a build process in the queue running, you can't log out now!");
      this.router.navigateByUrl('/');
    }
    else {
      this.authService.logout();
      this.router.navigateByUrl('/');
    }
  }
}
