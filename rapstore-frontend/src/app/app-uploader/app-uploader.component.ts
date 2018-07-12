import {Component, OnInit} from '@angular/core';
import {Http, RequestOptions, Headers} from '@angular/http';
import {AuthService} from '../auth.service';
import {DynFormService} from '../dyn-form.service';
import {environment} from '../../environments/environment';
import {Application} from '../models';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { FormElementBase, TextboxElement, TextareaElement } from '../models';

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
  elements: FormElementBase<any>[];
  file_element: FormElementBase<any>;

  constructor(private http: Http, private AuthService: AuthService, private fb: FormBuilder, private df: DynFormService) {
    this.file_element = new FormElementBase({key: "file", label: "File", controlType: "file"});
    this.elements = [
      new TextboxElement({key: "name", label: "App name", required: true}),
      new TextareaElement({key: "description", label: "Description"}),
      new TextboxElement({key: "licenses", label: "Licenses"}),
      new TextboxElement({key: "project_page", label: "Project page"}),
    ];

    this.form = df.toFormGroup(this.elements.concat([this.file_element]));
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

  fileChanged(file: File) {
    this.file = file;
  }

}
