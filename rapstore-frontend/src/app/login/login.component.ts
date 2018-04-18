import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  model: any = {};
  error = '';
  constructor(private authService: AuthService, private router: Router, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
      this.activatedRoute.queryParams.subscribe((params: Params) => {
        let code = params['code'];
        console.log(code);
      });
  }
  login() {
    this.authService.login(this.model.username, this.model.password)
      .subscribe(result => {
        this.router.navigate(['/']);
        }, err =>{
          this.error = "Invalid username or password";
        });
  }

}
