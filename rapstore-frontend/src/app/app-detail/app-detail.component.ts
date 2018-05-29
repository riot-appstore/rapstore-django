import {Component, OnInit, Input} from '@angular/core';
import {Application} from '../models';
import {AppService} from '../appservice.service';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {UserService} from '../user.service';
import {User} from '../models';

@Component({
  selector: 'app-app-detail',
  templateUrl: './app-detail.component.html',
  styleUrls: ['./app-detail.component.css']
})

export class AppDetailComponent implements OnInit {

  @Input() application: Application;
  private user: User;
  show_avatar = false;
  app_author = null;
  private one_line_description = '';

  constructor(private appService: AppService,
              private router: Router,
              private route: ActivatedRoute,
              private authService: AuthService,
              private userService: UserService) {
  }

  ngOnInit() {
    this.fetch_user();
    const id = +this.route.snapshot.paramMap.get('id');
    this.appService.get(id)
      .subscribe(
        app => {
          this.application = app;
          this.app_author = app.author;
          this.show_avatar = true;
          this.one_line_description = app.description.split('.')[0];
        }
      );
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

  request_login_page() {
    this.router.navigate(['/login'], { queryParams: { returnURL: this.router.url } });
  }

}
