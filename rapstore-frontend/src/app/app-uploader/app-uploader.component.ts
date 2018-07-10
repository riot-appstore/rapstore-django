import {Component, OnInit} from '@angular/core';
import {Http, RequestOptions, Headers} from '@angular/http';
import {AuthService} from '../auth.service';
import {environment} from '../../environments/environment';
import {Application} from '../models';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-app-uploader',
  templateUrl: './app-uploader.component.html',
  styleUrls: ['./app-uploader.component.css'],
  providers: [Application]
})
export class AppUploaderComponent implements OnInit {
  private file: File;
  message: string = '';
  errors: string[] = [];
  private baseurl = environment.apiUrl;
  form: FormGroup;

  constructor(private http: Http, private AuthService: AuthService, protected model: Application, private fb: FormBuilder) {
    this.model.initial_instance = {id: 0, version_name: '', version_code: 0};
    this.form = this.fb.group({name: [null, Validators.required], description: '', licenses: '', project_page: '', file: [null, Validators.required]});
  }

  ngOnInit() {
  }

  onSubmit() {
    if(this.form.valid) {
      let values = this.form.value;
      this.errors = [];
      this.message = '';
      let formData: FormData = new FormData();
      console.log(this.form.controls)
      formData.append('name', values.name);
      formData.append('description', values.description);
      formData.append('licenses', values.licenses);

      if(values.project_page) {
        formData.append('project_page', values.project_page);
      }

      formData.append('app_tarball', this.file, this.file.name);
      formData.append('initial_instance.version_name', 'VERSION');
      formData.append('initial_instance.version_code', '0');

      let headers = new Headers();
      headers.append('Authorization', 'Token ' + this.AuthService.get_token());
      headers.append('Accept', 'application/json');
      let options = new RequestOptions({headers: headers});
      this.http.post(`${this.baseurl}/api/app/`, formData, options)
        .map(res => res.json())
        .subscribe(
          data => this.message = `Successfully uploaded your app "${this.form.value.name}" ! The app will be under a review process in order to make it public.`,
          err => {
            let errors = JSON.parse(err.text());
            for (let k in errors) {
              this.errors.push(`${k}: ${errors[k]}`);
            }
          }
        );
    }
  }

  fileChanged(event) {
    this.file = event.target.files.length > 0 && event.target.files[0];
  }

}
