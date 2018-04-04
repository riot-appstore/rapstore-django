import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service'

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  model: any = {};

  constructor(private userService: UserService) { }

  ngOnInit() {
  }

  signup() {
    this.userService.register(this.model)
      .subscribe(result => {
        console.log("Registered!");
      });
  }


}
