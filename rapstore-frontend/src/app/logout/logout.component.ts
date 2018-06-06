import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {User} from '../models';
import {UserService} from '../user.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {
  private user: User;

  constructor(protected authService: AuthService,
              private router: Router,
              private userService: UserService) { }

  ngOnInit() {

    if (!this.authService.get_token()) {
      // dont show logout page if user is not logged in
      this.router.navigateByUrl('/');
    }

    this.authService.logout();
    this.router.navigateByUrl('/');
  }
}
