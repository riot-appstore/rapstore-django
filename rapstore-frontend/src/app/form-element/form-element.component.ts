import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormElementBase } from '../models';
import { FormGroup} from '@angular/forms';

@Component({
  selector: 'app-form-element',
  templateUrl: './form-element.component.html',
  styleUrls: ['./form-element.component.css']
})

export class FormElementComponent {
  @Input() element: FormElementBase<any>;
  @Input() form: FormGroup;
  @Output() notify_file: EventEmitter<File> = new EventEmitter<File>();
  // get isValid() { return this.form.controls[this.element.key].valid; }
  onChange(event) {
    let file: File = event.target.files.length > 0 && event.target.files[0];
    this.notify_file.emit(file);
  }

}
