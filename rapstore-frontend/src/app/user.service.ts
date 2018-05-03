import {Injectable, Output, EventEmitter} from '@angular/core';
import {Http, Response, RequestOptions, Headers} from '@angular/http';
import {AuthService} from './auth.service';
import {Signup, User} from './models';
import {environment} from '../environments/environment';

@Injectable()
export class UserService {
  private url = `${environment.apiUrl}/api/user/`;
  private contentType = {'Content-Type': 'application/json'};

  constructor(private authService: AuthService, private http: Http) {
  }

  get() {
    return this.http.get(this.url, this.getAuthOptions()).map(res => res.json());
  }

  update(user: User) {
    return this.http.put(`${this.url}update/`, user, this.getAuthOptions()).map(res => res.json());
  }

  getAuthOptions(): RequestOptions {
    const authHeaders = new Headers(this.contentType);
    authHeaders.append('Authorization', 'Token ' + this.authService.get_token());
    return new RequestOptions({headers: authHeaders});
  }

  register(signup: Signup) {
    const authHeaders = new Headers(this.contentType);
    return this.http.post(`${this.url}register/`, signup, new RequestOptions({headers: authHeaders})).map(res => res.json());
  }

}
