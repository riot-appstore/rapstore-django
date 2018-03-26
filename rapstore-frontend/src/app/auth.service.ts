import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class AuthService {
  private base_url: string = 'http://localhost:8000';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  public token: string;

  constructor(private http: Http) { }
  login(username: string, password: string): Observable<boolean> {
      const url=`${this.base_url}/api/auth`;
      return this.http.post(url, JSON.stringify({username: username, password: password}), {headers: this.headers})
        .map((response: Response) => {
          const token = response.json() && response.json().token;
          if(token) {
            this.token = token;
            localStorage.setItem("user", JSON.stringify({username: username, token: token}));
            return true;
          }
          else {
            return false;
          }
        });
  }
  logout() {
    this.token = null;
    localStorage.removeItem("user");  
  }
}
