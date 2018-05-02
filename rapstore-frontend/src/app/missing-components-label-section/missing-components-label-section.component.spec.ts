import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {MissingComponentsLabelSectionComponent} from './missing-components-label-section.component';

describe('MissingComponentsLabelSectionComponent', () => {
  let component: MissingComponentsLabelSectionComponent;
  let fixture: ComponentFixture<MissingComponentsLabelSectionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MissingComponentsLabelSectionComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MissingComponentsLabelSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
