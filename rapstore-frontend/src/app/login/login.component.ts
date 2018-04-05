import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  model: any = {};
  error = '';
  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
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
