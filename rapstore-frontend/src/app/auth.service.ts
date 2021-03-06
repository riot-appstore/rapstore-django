
import {map} from 'rxjs/operators';
import {Injectable, Output, EventEmitter} from '@angular/core';
import {Http, Response, RequestOptions, Headers} from '@angular/http';
import {Observable, BehaviorSubject} from 'rxjs';
import {UserService} from './user.service';
import {User} from './models';
import {environment} from '../environments/environment';

@Injectable()
export class AuthService {
  private base_url = environment.apiUrl;
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  private token: boolean;
  private is_dev: boolean;

  @Output() userChangeEvent: EventEmitter<boolean> = new EventEmitter(true);

  constructor(private http: Http) {
    const current_user = JSON.parse(localStorage.getItem('user'));
    this.token = current_user && current_user.token;
    this.is_dev = current_user && current_user.is_dev;
  }

  login(username: string, password: string): Observable<boolean> {
    const url = `${this.base_url}/auth/`;
    return this.http.post(url, JSON.stringify({username: username, password: password}), {headers: this.headers}).pipe(
      map((response: Response) => {
        const data = response.json();
        const token = data && data.token;
        if (token) {
          this.perform_login(username, token);
          return true;
        }
        else {
          this.refresh(false);
          return false;
        }
      }));
  }

  perform_login(username: string, token: boolean) {
    this.refresh(true);
    this.token = token;
    localStorage.setItem('user', JSON.stringify({username: username, token: token}));

  }
  logout() {
    this.token = null;
    this.is_dev = null;
    this.refresh(false);
    localStorage.removeItem('user');
  }

  get_token() {
    return this.token;
  }

  refresh(logging: boolean) {
    this.userChangeEvent.emit(logging);
  }

  get_github_url() {
    const url = `${this.base_url}/social/url/github/`;
    return this.http.get(url, {headers: this.headers, withCredentials: true}).pipe(map(res => res.json()));
  }
  get_social_token(code: string, state: string) {
    const url = `${this.base_url}/social/login/github/`;
    return this.http.post(url, JSON.stringify({code: code, state: state}), {headers: this.headers, withCredentials: true}).pipe(map((response: Response) => {
      let res = response.json();
      this.perform_login(res.username, res.token);
      return true;
    }));
  }
}
