import { Injectable } from '@angular/core';
import { Application } from './models';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

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

  constructor() { }
  getAll() : Observable<Application[]> {
    return of(APPS);
  }
  get(id: number) : Observable<Application> {
   return of(APPS.find(app => app.id === id));
 }

}
