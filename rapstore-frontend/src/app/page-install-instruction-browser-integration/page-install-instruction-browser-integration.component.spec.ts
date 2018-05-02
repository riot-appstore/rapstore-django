import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {PageInstallInstructionBrowserIntegrationComponent} from './page-install-instruction-browser-integration.component';

describe('PageInstallInstructionBrowserIntegrationComponent', () => {
  let component: PageInstallInstructionBrowserIntegrationComponent;
  let fixture: ComponentFixture<PageInstallInstructionBrowserIntegrationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PageInstallInstructionBrowserIntegrationComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PageInstallInstructionBrowserIntegrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
