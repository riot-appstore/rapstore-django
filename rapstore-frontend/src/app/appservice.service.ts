import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

const APPS: Application[] = [
  { id: 1, name: 'GNRC Networking', description: "Standard network for RIOT" },
  { id: 2, name: 'My App', description: "This is my own app" },
];

@Injectable()
export class AppserviceService {

  constructor() { }
  getAll() : Observable<Application[]> {
    return of(APPS);
  }
  get(id: number) : Observable<Application> {
   return of(APPS.find(app => app.id === id));
 }

}
