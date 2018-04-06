import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppUploaderComponent } from './app-uploader.component';

describe('AppUploaderComponent', () => {
  let component: AppUploaderComponent;
  let fixture: ComponentFixture<AppUploaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppUploaderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppUploaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
