import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

const APPS: Application[] = [
  { id: 1, name: 'GNRC Networking', description: "Standard network for RIOT" },
  { id: 2, name: 'My App', description: "This is my own app" },
  { id: 3, name: 'My App', description: "This is my own app" },
  { id: 4, name: 'My App', description: "This is my own app" },
  { id: 5, name: 'My App', description: "This is my own app" },
  { id: 6, name: 'My App', description: "This is my own app" },
  { id: 7, name: 'My App', description: "This is my own app" },
  { id: 8, name: 'My App', description: "This is my own app" },
  { id: 9, name: 'My App', description: "This is my own app" },
  { id: 10, name: 'My App', description: "This is my own app" },
];

@Injectable()
export class AppserviceService {
private baseUrl: string = 'http://localhost:8000';
  constructor(private http: Http) { }
  getAll() : Observable<Application[]> {
     let headers = new Headers({"Content-Type": 'application/json'});
     let options = new RequestOptions({ headers: headers });
     return this.http.get(`${this.baseUrl}/api/app/`).map(res => res.json());
  }
  get(id: number) : Observable<Application> {
   let headers = new Headers({"Content-Type": 'application/json'});
   let options = new RequestOptions({ headers: headers });
   return this.http.get(`${this.baseUrl}/api/app/${id}/`).map(res => res.json());
 }

}
