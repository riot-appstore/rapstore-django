import { Component, OnInit } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';
import { AuthService } from '../auth.service';
import { environment } from '../../environments/environment';
import { Application } from '../models'

@Component({
  selector: 'app-app-uploader',
  templateUrl: './app-uploader.component.html',
  styleUrls: ['./app-uploader.component.css'],
  providers: [Application]
})
export class AppUploaderComponent implements OnInit {
  private file: File;
  message: string = "";
  errors: string[] = [];
  private baseurl = environment.apiUrl;
  constructor(private http: Http, private AuthService: AuthService, protected model: Application) {
    this.model.initial_instance={id: 0, version_name: "", version_code: ""}; }

  ngOnInit() {
  }

  fileUpload() {
  if(this.file && this.model.name) {
    this.errors = [];
    let formData:FormData = new FormData();
    formData.append('name', this.model.name);
    formData.append('description', this.model.description);
    formData.append('licenses', this.model.licenses);
    formData.append('project_page', this.model.project_page);
    formData.append('app_tarball', this.file, this.file.name);
    formData.append('initial_instance.version_name', this.model.initial_instance.version_name);
    formData.append('initial_instance.version_code', this.model.initial_instance.version_code);
    let headers = new Headers();

    headers.append('Authorization', 'Token '+this.AuthService.get_token());
    headers.append('Accept', 'application/json');
    let options = new RequestOptions({ headers: headers });
    this.http.post(`${this.baseurl}/api/app/`, formData, options)
        .map(res => res.json())
        .subscribe(
        data => this.message = `Successfully uploaded your app "${this.model.name}" ! The app will be under a review process in order to make it public.`,
        err => {
            let errors = JSON.parse(err.text());
            for (let k in errors) {
                this.errors.push(`${k}: ${errors[k]}`);
            }
        }
        )
  }
  }
  fileChanged(event) {
    this.file = event.target.files.length > 0 && event.target.files[0];
  }

}
