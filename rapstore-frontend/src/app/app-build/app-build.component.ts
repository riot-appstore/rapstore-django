import { Component, OnInit, Input } from '@angular/core';
import { Application } from '../models';
import { AppService } from '../appservice.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-app-build',
  templateUrl: './app-build.component.html',
  styleUrls: ['./app-build.component.css']
})
export class AppBuildComponent implements OnInit {

  @Input() application: Application;
  constructor(private appService: AppService, private route: ActivatedRoute) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.appService.get(id)
      .subscribe(app => this.application = app);
  }

}
