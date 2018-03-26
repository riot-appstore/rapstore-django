import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { Http, RequestOptions, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class AppserviceService {

  private baseUrl = 'http://localhost:8000';

  constructor(private http: Http) { }

  getAll(): Observable<Application[]> {
     let headers = new Headers({'Content-Type': 'application/json'});
     let options = new RequestOptions({ headers: headers });
     return this.http.get(`${this.baseUrl}/api/app/`).map(res => res.json());
  }

  get(id: number): Observable<Application> {
   let headers = new Headers({'Content-Type': 'application/json'});
   let options = new RequestOptions({ headers: headers });
   return this.http.get(`${this.baseUrl}/api/app/${id}/`).map(res => res.json());
  }

}
