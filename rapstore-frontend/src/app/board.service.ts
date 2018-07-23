
import {map} from 'rxjs/operators';
import {Injectable} from '@angular/core';
import {Http, Response, RequestOptions, Headers} from '@angular/http';
import {Board} from './models';
import {Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {AuthService} from './auth.service';

@Injectable()
export class BoardService {

  private baseUrl = environment.apiUrl;

  constructor(private http: Http, private authService: AuthService) {
  }

  getAll(): Observable<Board[]> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    return this.http.get(`${this.baseUrl}/api/board/`).pipe(map(res => res.json()));
  }

  getAuthOptions(): RequestOptions {
    const authHeaders = new Headers();
    authHeaders.append('Authorization', 'Token ' + this.authService.get_token());
    authHeaders.append('Content-Type', 'application/json');
    return new RequestOptions({headers: authHeaders});
  }
  getSupported(app_id: number): Observable<Board[]> {
    let options = this.getAuthOptions();
    return this.http.get(`${this.baseUrl}/api/app/${app_id}/supported_boards/`, options).pipe(map(res => res.json()));
  }

}
