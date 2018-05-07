import {Component, OnInit} from '@angular/core';
import {AuthService} from '../auth.service';
import {Router, ActivatedRoute, Params} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  model: any = {};
  error = '';
  github_url = '';
  social_loading: boolean = false;

  constructor(private authService: AuthService, private router: Router, private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.authService.get_github_url().subscribe(val => this.github_url = val.url);
    this.activatedRoute.queryParams.subscribe((params: Params) => {
        let code = params['code'];
        if(code) {
          this.social_loading = true;
          this.authService.get_social_token(code).subscribe(val => this.router.navigate(['/']));
        }
      });
  }

  login() {
    this.authService.login(this.model.username, this.model.password)
      .subscribe(result => {
        this.router.navigate(['/']);
      }, err => {
        this.error = 'Invalid username or password';
      });
  }

}
