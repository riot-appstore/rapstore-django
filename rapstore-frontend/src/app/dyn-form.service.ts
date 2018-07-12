import { Injectable } from '@angular/core';
import { FormElementBase } from './models';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Injectable()
export class DynFormService {

  constructor() { }

  toFormGroup(elements: FormElementBase<any>[] ) {
    let group: any = {};

    elements.forEach(el => {
      group[el.key] = el.required ? new FormControl(el.value || '', Validators.required)
                                              : new FormControl(el.value || '');
    });
    return new FormGroup(group);
  }
}
