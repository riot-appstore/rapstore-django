import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { Http, RequestOptions, Headers, ResponseContentType } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class AppService {

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
  download(id: number, board: number, name: string) {
        this.http.get("http://localhost:8000/api/app/"+id+"/build?board="+board, {
        responseType: ResponseContentType.Blob,
        headers: new Headers({'Content-Type': 'application/x-www-form-urlencoded'})
    }).subscribe(
        (response) => { // download file
            let filename = response.headers.get("content-disposition").split("=")[1];
            let blob = new Blob([response.blob()], {type: 'application/octet_stream'});
            let downloadUrl= window.URL.createObjectURL(blob);
            let element = document.createElement('a');
            element.setAttribute('href', downloadUrl);
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
    });
  }

}
