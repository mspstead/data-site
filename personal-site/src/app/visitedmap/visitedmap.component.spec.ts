import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VisitedmapComponent } from './visitedmap.component';

describe('VisitedmapComponent', () => {
  let component: VisitedmapComponent;
  let fixture: ComponentFixture<VisitedmapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VisitedmapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VisitedmapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
