import { TestBed } from '@angular/core/testing';

import { ExchangeRequestService } from './exchange-request.service';

describe('ExchangeRequestService', () => {
  let service: ExchangeRequestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExchangeRequestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
