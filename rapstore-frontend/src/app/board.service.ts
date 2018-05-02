import {Injectable} from '@angular/core';
import {Http, Response, RequestOptions, Headers} from '@angular/http';
import {Board} from './models';
import {Observable} from 'rxjs/Observable';
import {environment} from '../environments/environment';

@Injectable()
export class BoardService {

  private baseUrl = environment.apiUrl;

  constructor(private http: Http) {
  }

  getAll(): Observable<Board[]> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    return this.http.get(`${this.baseUrl}/api/board/`).map(res => res.json());
  }

  getSupported(app_id: number): Observable<Board[]> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    return this.http.get(`${this.baseUrl}/api/app/${app_id}/supported_boards/`).map(res => res.json());
  }

}
