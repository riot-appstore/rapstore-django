import { Component, OnInit } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/take';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  username="";
  is_logged_in$: Observable<boolean>;
  constructor(private AuthService: AuthService, private router: Router) {}
  ngOnInit() {
   this.is_logged_in$ = this.AuthService.is_logged; 
   this.username = this.AuthService.username();
  }
  logout() {
    this.AuthService.logout();
    this.router.navigate(['/']);
  }
}
