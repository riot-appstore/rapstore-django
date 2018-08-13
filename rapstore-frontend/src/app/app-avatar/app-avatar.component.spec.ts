import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppAvatarComponent } from './app-avatar.component';

describe('AppAvatarComponent', () => {
  let component: AppAvatarComponent;
  let fixture: ComponentFixture<AppAvatarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppAvatarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppAvatarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
