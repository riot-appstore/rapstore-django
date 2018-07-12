import { TestBed, inject } from '@angular/core/testing';

import { DynFormService } from './dyn-form.service';

describe('DynFormService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DynFormService]
    });
  });

  it('should be created', inject([DynFormService], (service: DynFormService) => {
    expect(service).toBeTruthy();
  }));
});
