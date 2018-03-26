import { Component, OnInit } from '@angular/core';
import { AuthService } from './auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  logged: boolean;
  constructor(private AuthService: AuthService, private router: Router) {}
  ngOnInit() {
    this.logged = this.AuthService.logged();
  }
  logout() {
    this.AuthService.logout();
    this.router.navigate(['/']);
  }
}
