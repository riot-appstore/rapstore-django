import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PageInstallInstructionDragAndDropComponent } from './page-install-instruction-drag-and-drop.component';

describe('PageInstallInstructionDragAndDropComponent', () => {
  let component: PageInstallInstructionDragAndDropComponent;
  let fixture: ComponentFixture<PageInstallInstructionDragAndDropComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PageInstallInstructionDragAndDropComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PageInstallInstructionDragAndDropComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
