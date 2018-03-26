import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class AuthService {
  private base_url = 'http://localhost:8000';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  private token: boolean;
  private logged_in = new BehaviorSubject<boolean>(false);

  constructor(private http: Http) {
      const current_user = JSON.parse(localStorage.getItem('user'));
      this.token = current_user && current_user.token;
      this.logged_in.next(this.token);
  }
  login(username: string, password: string): Observable<boolean> {
      const url=`${this.base_url}/auth/`;
      return this.http.post(url, JSON.stringify({username: username, password: password}), {headers: this.headers})
        .map((response: Response) => {
          const token = response.json() && response.json().token;
          if(token) {
            this.token = token;
            localStorage.setItem("user", JSON.stringify({username: username, token: token}));
            this.logged_in.next(true);
            return true;
          }
          else {
            this.logged_in.next(false);
            return false;
          }
        });
  }
  logout() {
    this.token = null;
    localStorage.removeItem("user");
    this.logged_in.next(false);
  }
  get is_logged() {
    return this.logged_in.asObservable();
  }
  username() {
    if (localStorage.getItem('user')){
      return JSON.parse(localStorage.getItem('user')).username;
     } else return "";
  }
  is_developer() {
    return false;
  }
}
