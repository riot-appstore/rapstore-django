import {Injectable} from '@angular/core';
import {Http, Response, RequestOptions, Headers} from '@angular/http';
import {Feedback} from './models';
import {environment} from '../environments/environment';

@Injectable()
export class FeedbackService {
  private baseUrl = environment.apiUrl;
  private contentType = {'Content-Type': 'application/json'};

  constructor(private http: Http) {
  }

  sendFeedback(feedback: Feedback) {
    const authHeaders = new Headers(this.contentType);
    return this.http.post(`${this.baseUrl}/api/feedback/`, feedback, new RequestOptions({headers: authHeaders})).map(res => res.json());
  }

}
