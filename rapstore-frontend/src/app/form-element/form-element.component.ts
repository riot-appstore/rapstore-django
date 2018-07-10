import { Component, Input } from '@angular/core';
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
  // get isValid() { return this.form.controls[this.element.key].valid; }

}
