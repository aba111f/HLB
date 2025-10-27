import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRequestService {
  private apiUrl = 'http://localhost:8000/exchange-requests/';

  constructor(private http: HttpClient) {}

  createExchangeRequest(requestData: any): Observable<any> {
    const token = localStorage.getItem('access');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl, requestData, { headers });
  }

  getExchangeRequests(): Observable<any> {
    const token = localStorage.getItem('access');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get(this.apiUrl, { headers });
  }
}
