import {Component, OnInit} from '@angular/core';
import {UserService} from '../user.service';
import {User} from '../models';
import {FormElementBase, TextboxElement} from '../models';
import { FormGroup } from '@angular/forms';
import {DynFormService} from '../dyn-form.service';

@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.css']
})
export class UserprofileComponent implements OnInit {
  private edit: boolean = false;
  private user: User;
  form: FormGroup;
  elements: FormElementBase<any>[];

  constructor(private userService: UserService, private df: DynFormService) {
    this.elements = [
      new TextboxElement({key: "first_name", label: "First name"}),
      new TextboxElement({key: "last_name", label: "Last name"}),
      new TextboxElement({key: "location", label: "Location"}),
      new TextboxElement({key: "company", label: "Company"}),
      new TextboxElement({key: "gender", label: "Gender"}),
      new TextboxElement({key: "phone_number", label: "Phone number"}),
    ];
    this.form = df.toFormGroup(this.elements);
  }

  ngOnInit() {
    this.userService.get().subscribe(user => {this.user = user; this.form.patchValue(user)});
  }

  update() {
    this.userService.update(this.form.value).subscribe(res => this.set_edit(false));
  }

  set_edit(enable: boolean) {
    this.user = this.form.value;
    if (enable) {
      this.form.patchValue(this.user);
    }
    this.edit = enable;
  }
}
