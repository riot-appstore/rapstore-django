import {Component, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Router, ActivatedRoute} from '@angular/router';
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
  returnURL: string;

  private $subscriptionRoute: Subscription;

  constructor(private userService: UserService,
              private authService: AuthService,
              private router: Router,
              private activatedRoute: ActivatedRoute) {}

  ngOnInit() {

    this.$subscriptionRoute = this.activatedRoute
      .queryParams
      .subscribe(params => {
        this.returnURL = params.returnURL || '/';
      });

    this.authService.get_github_url().subscribe(val => this.github_url = val.url);
  }

  signup() {
    this.refresh();
    this.userService.register(this.model)
      .subscribe(result => {
        this.message = 'Successful registration!';
        setTimeout( () => {
          this.router.navigateByUrl(this.returnURL);
        }, 1000 );

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
