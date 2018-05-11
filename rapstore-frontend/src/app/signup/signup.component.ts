import {Component, OnInit} from '@angular/core';
import {UserService} from '../user.service';
import {AuthService} from '../auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  model: any = {};
  message: string = '';
  errors: string[] = [];
  github_url = '';

  constructor(private userService: UserService, private authService: AuthService) {
  }

  ngOnInit() {
    this.authService.get_github_url().subscribe(val => this.github_url = val.url);
  }

  signup() {
    this.refresh();
    this.userService.register(this.model)
      .subscribe(result => {
        this.message = 'Successful registration!';
      }, err => {
        let errors = JSON.parse(err.text());
        for (let k in errors) {
          this.errors.push(`${k}: ${errors[k]}`);
        }
      });
  }

  refresh() {
    this.message = '';
    this.errors = [];
  }


}
