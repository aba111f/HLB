import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExchangeRequestComponent } from './exchange-request.component';

describe('ExchangeRequestComponent', () => {
  let component: ExchangeRequestComponent;
  let fixture: ComponentFixture<ExchangeRequestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExchangeRequestComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExchangeRequestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
