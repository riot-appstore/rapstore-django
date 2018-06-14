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

  getAuthHeaders(): Headers {
    const authHeaders = new Headers();
    authHeaders.append('Authorization', 'Token ' + this.authService.get_token());
    return authHeaders;
  }

  request_build(id: number, board: number, name: string, type: string) {
  let headers = this.getAuthHeaders();
  headers.append('Content-Type', 'application/json');
  return this.http.get(`${this.baseUrl}/api/app/${id}/build/?board=${board}&type=${type}`, new RequestOptions({headers: headers})).map(res => res.json());
  }

  check_build(task_id: string) {
  let headers = this.getAuthHeaders();
  headers.append('Content-Type', 'application/json');
  return this.http.get(`${this.baseUrl}/api/buildmanager/${task_id}/status/`, new RequestOptions({headers: headers})).map(res => res.json());
  }

  fetch_file(task_id) {
  let headers = this.getAuthHeaders();
  headers.append('Content-Type', 'application/x-www-form-urlencoded');
  return this.http.get(`${this.baseUrl}/api/buildmanager/${task_id}/fetch/`, new RequestOptions({headers: headers, responseType: ResponseContentType.Blob}));
  }

  perform_download(filename, blob) {
    let downloadUrl = window.URL.createObjectURL(blob);
    let element = document.createElement('a');
    element.setAttribute('href', downloadUrl);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }
}
