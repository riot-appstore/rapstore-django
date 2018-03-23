import { Component, OnInit } from '@angular/core';
import { Application, APPS } from '../models';

@Component({
  selector: 'app-app-browser',
  templateUrl: './app-browser.component.html',
  styleUrls: ['./app-browser.component.css']
})

export class AppBrowserComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }
  apps = APPS;
  id_prefix="examplesTab_";
  column_width=4;

}
