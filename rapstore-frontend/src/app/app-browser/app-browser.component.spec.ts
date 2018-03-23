import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppBrowserComponent } from './app-browser.component';

describe('AppBrowserComponent', () => {
  let component: AppBrowserComponent;
  let fixture: ComponentFixture<AppBrowserComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppBrowserComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppBrowserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
