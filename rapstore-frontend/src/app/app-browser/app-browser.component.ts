import { Component, OnInit, Input } from '@angular/core';
import { Application} from '../models';
import { AppserviceService } from '../appservice.service';

@Component({
  selector: 'app-app-browser',
  templateUrl: './app-browser.component.html',
  styleUrls: ['./app-browser.component.css']
})

export class AppBrowserComponent implements OnInit {

  @Input() apps: Application[];
  constructor(private AppserviceService: AppserviceService) {}

  ngOnInit() {
    this.AppserviceService.getAll()
      .subscribe(app => this.apps = app);
  }
  id_prefix="examplesTab_";
  column_width=4;

}
