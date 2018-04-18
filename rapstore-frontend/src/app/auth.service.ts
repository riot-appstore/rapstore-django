import { Injectable, Output, EventEmitter } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { UserService } from './user.service';
import { User } from './models'

@Injectable()
export class AuthService {
  private base_url = `http://${window.location.hostname}:8080`;
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
      const url=`${this.base_url}/auth/`;
      return this.http.post(url, JSON.stringify({username: username, password: password}), {headers: this.headers})
        .map((response: Response) => {
          const data = response.json();
          const token = data && data.token;
          const is_dev = data && data.is_dev;
          if(token) {
            this.refresh(true);
            this.token = token;
            this.is_dev = is_dev;
            localStorage.setItem("user", JSON.stringify({username: username, token: token, is_dev: is_dev}));
            return true;
          }
          else {
            this.refresh(false);
            return false;
          }
        });
  }
  logout() {
    this.token = null;
    this.is_dev = null;
    this.refresh(false);
    localStorage.removeItem("user");
  }
  get_token() {
    return this.token;
  }
  refresh(logging: boolean)
  {
    this.userChangeEvent.emit(logging);
  }
}
