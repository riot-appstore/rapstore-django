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
  constructor(private appService: AppService, private route: ActivatedRoute) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.appService.get(id)
    .subscribe(app => {this.application = app; this.show_avatar = true;});
  }

}
