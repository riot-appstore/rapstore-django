import {TestBed, inject} from '@angular/core/testing';

import {BrowserIntegrationService} from './browser-integration.service';

describe('BrowserIntegrationService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BrowserIntegrationService]
    });
  });

  it('should be created', inject([BrowserIntegrationService], (service: BrowserIntegrationService) => {
    expect(service).toBeTruthy();
  }));
});
