import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { Http, RequestOptions, Headers, ResponseContentType } from '@angular/http';
import 'rxjs/add/operator/map';
import { environment } from '../environments/environment';

@Injectable()
export class AppService {

  private baseUrl = environment.apiUrl;
  private loading: boolean = false;

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
  download(id: number, board: number, name: string) {
        return this.http.get(this.baseUrl+"/api/app/"+id+"/build?board="+board, {
        responseType: ResponseContentType.Blob,
        headers: new Headers({'Content-Type': 'application/x-www-form-urlencoded'})
    });
  }

}
