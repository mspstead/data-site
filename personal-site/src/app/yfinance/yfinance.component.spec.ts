import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { YfinanceComponent } from './yfinance.component';

describe('YfinanceComponent', () => {
  let component: YfinanceComponent;
  let fixture: ComponentFixture<YfinanceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ YfinanceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(YfinanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
