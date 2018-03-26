import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Http, RequestOptions, Headers } from '@angular/http';
import {Board} from './models';

@Injectable()
export class BoardService {

  private baseUrl = 'http://localhost:8000';

  constructor(private http: Http) {}

  getAll(): Observable<Board[]> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({ headers: headers });
    return this.http.get(`${this.baseUrl}/api/board/`).map(res => res.json());
  }

}
