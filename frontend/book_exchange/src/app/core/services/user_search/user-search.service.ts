import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BookUser, Result } from '../../../shared/interface/book-user';
@Injectable({
  providedIn: 'root'
})
export class UserSearchService {
  private apiUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {}
  
  searchUsers(filters: {
    title?: string;
    author?: string;
    genre?: string;
    exchange_type?: string;
  }): Observable<Result> {

    const form = new FormData();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) form.append(key, value);
    });
    return this.http.post<Result>(this.apiUrl+'search/', form);
  }
}
