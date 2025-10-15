import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BookUser {
  username: string;
  city: string;
  book_title: string;
  genre: string;
  exchange_type: string;
  user_image?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserSearchService {
  private apiUrl = 'http://localhost:8000/api/user-search/';

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
    return this.http.get<BookUser[]>(this.apiUrl, { params });
  }
}
