import {Component, OnInit, Input} from '@angular/core';
import {Application} from '../models';
import {AppService} from '../appservice.service';
import {ActivatedRoute} from '@angular/router';
import 'rxjs/Rx' ;
import Timer = NodeJS.Timer;

@Component({
  selector: 'app-app-build',
  templateUrl: './app-build.component.html',
  styleUrls: ['./app-build.component.css']
})
export class AppBuildComponent implements OnInit {
  private selected_board: number;
  private loading: boolean = false;
  private dots: string = '';
  private timer_id: Timer;
  private error = '';
  @Input() application: Application;

  constructor(private appService: AppService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.appService.get(id)
      .subscribe(app => this.application = app);
  }

  onBoardChange(id) {
    this.selected_board = id;
  }

  downloadElf(id) {
    this.loading = true;
    this.error = '';
    this.timer_id = setInterval(val => {
      this.dots += '.';
      if (this.dots.length == 4) {
        this.dots = '';
      }
    }, 700);
    this.appService.download(id, this.selected_board, this.application.name).subscribe(
      (response) => { // download file
        clearInterval(this.timer_id);

        let filename = response.headers.get('content-disposition').split('=')[1];
        let blob = new Blob([response.blob()], {type: 'application/octet_stream'});
        let downloadUrl = window.URL.createObjectURL(blob);
        let element = document.createElement('a');
        element.setAttribute('href', downloadUrl);
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
      }, (err) => {
        this.loading = false;
        this.error = 'Something went wrong';
      },
      () => this.loading = false);
  }

}
