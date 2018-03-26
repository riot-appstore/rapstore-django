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
  error: string = "";
  constructor(private AuthService: AuthService, private router: Router) { }

  ngOnInit() {
  }
  login() {
    this.AuthService.login(this.model.username, this.model.password)
      .subscribe(result => {
        if(result) {
          this.router.navigate(['/']);
        }
        else {
          console.log("Invalid");
          this.error = "Invalid username or password";
        }
      }); 
  }

}
