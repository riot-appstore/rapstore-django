import {Component, OnInit} from '@angular/core';
import {UserService} from '../user.service';
import {User} from '../models';

@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.css']
})
export class UserprofileComponent implements OnInit {
  private model: any = {};
  private edit: boolean = false;
  private user: User;

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    this.userService.get().subscribe(user => this.user = user);
  }

  update() {
    this.userService.update(this.model).subscribe(res => this.set_edit(false));
  }

  set_edit(enable: boolean) {
    if (enable) {
      this.model = this.user;
    }
    this.edit = enable;
  }
}
