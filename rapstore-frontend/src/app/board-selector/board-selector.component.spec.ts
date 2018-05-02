import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BoardSelectorComponent} from './board-selector.component';

describe('BoardSelectorComponent', () => {
  let component: BoardSelectorComponent;
  let fixture: ComponentFixture<BoardSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [BoardSelectorComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
