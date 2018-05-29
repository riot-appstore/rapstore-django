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
  returnURL: string;

  constructor(private authService: AuthService, private router: Router, private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.authService.get_github_url().subscribe(val => this.github_url = val.url);
    this.activatedRoute.queryParams.subscribe((params: Params) => {
        let code = params['code'];
        let state = params['state'];
        if(code && state) {
          this.social_loading = true;
          this.authService.get_social_token(code, state).subscribe(val => this.router.navigate(['/']), error => {
            alert("Invalid github login");
            this.router.navigate(['/']);
          });
        }
      });

    this.returnURL = this.activatedRoute.snapshot.queryParams['returnURL'] || '/';
  }

  login() {
    this.authService.login(this.model.username, this.model.password)
      .subscribe(result => {
        this.router.navigateByUrl(this.returnURL);
      }, err => {
        this.error = 'Invalid username or password';
      });
  }

}
