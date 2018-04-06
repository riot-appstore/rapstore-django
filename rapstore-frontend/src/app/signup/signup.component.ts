import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service'

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  model: any = {};
  message: string = "";
  errors: string[] = [];

  constructor(private userService: UserService) { }

  ngOnInit() {
  }

  signup() {
    this.refresh();
    this.userService.register(this.model)
      .subscribe(result => {
        this.message = "Successful registration. Please wait until a RAPstore admin activates your account";
        }, err => {
          let errors = JSON.parse(err.text());
          for(let k in errors) {
            this.errors.push(`${k}: ${errors[k]}` );
          }
        });
  }

  refresh() {
    this.message = "";
    this.errors = [];
  }


}
