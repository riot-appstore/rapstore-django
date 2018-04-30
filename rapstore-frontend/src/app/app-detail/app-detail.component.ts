import { Component, OnInit, Input } from '@angular/core';
import { Application } from '../models';
import { AppService } from '../appservice.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-app-detail',
  templateUrl: './app-detail.component.html',
  styleUrls: ['./app-detail.component.css']
})

export class AppDetailComponent implements OnInit {

  @Input() application: Application;
  show_avatar = false;
  app_author = null;
  private one_line_description=""
  constructor(private appService: AppService, private route: ActivatedRoute) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.appService.get(id)
      .subscribe(
        app => {
          this.application = app;
          this.app_author = app.author;
          this.show_avatar = true;
          this.one_line_description = app.description.split(".")[0];
        }
      );
  }

}
