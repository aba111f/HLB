import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BookUser } from '../../../shared/interface/book-user';
@Injectable({
  providedIn: 'root'
})
export class UserSearchService {
  private apiUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {}

  searchUsers(filters: {
    title?: string;
    city?: string;
    genre?: string;
    exchange_type?: string;
  }): Observable<BookUser[]> {
    let params = new HttpParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params = params.set(key, value);
    });
    return this.http.post<BookUser[]>(this.apiUrl+'users/search_and_filter/', { params });
  }
}
