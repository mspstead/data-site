import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PortfolioOptimisationComponent } from './portfolio-optimisation.component';

describe('PortfolioOptimisationComponent', () => {
  let component: PortfolioOptimisationComponent;
  let fixture: ComponentFixture<PortfolioOptimisationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PortfolioOptimisationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PortfolioOptimisationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
