import {Injectable} from '@angular/core';
import {Application} from './models';
import {Observable} from 'rxjs/Observable';
import {AuthService} from './auth.service';
import {Http, RequestOptions, Headers, ResponseContentType} from '@angular/http';
import 'rxjs/add/operator/map';
import {environment} from '../environments/environment';

@Injectable()
export class AppService {

  private baseUrl = environment.apiUrl;
  private loading: boolean = false;

  constructor(private http: Http, private authService: AuthService) {
  }

  getAll(): Observable<Application[]> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    return this.http.get(`${this.baseUrl}/api/app/`).map(res => res.json());
  }

  get(id: number): Observable<Application> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    return this.http.get(`${this.baseUrl}/api/app/${id}/`).map(res => res.json());
  }

  getAuthOptions(): RequestOptions {
    const authHeaders = new Headers();
    authHeaders.append('Authorization', 'Token ' + this.authService.get_token());
    authHeaders.append('Content-Type', 'application/x-www-form-urlencoded');
    return new RequestOptions({headers: authHeaders, responseType: ResponseContentType.Blob});
  }

  download(id: number, board: number, name: string) {
    return this.http.get(this.baseUrl + '/api/app/' + id + '/build/?board=' + board, this.getAuthOptions());
  }

}
