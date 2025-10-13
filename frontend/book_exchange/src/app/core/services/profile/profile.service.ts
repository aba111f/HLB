import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserData, UserPost } from '../../../shared/interface/interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private baseUrl = 'http://localhost:8000/api/users';

  constructor(private http: HttpClient) {}

  getCurrentUser(): Observable<UserData> {

    let id=localStorage.getItem('id');

    return this.http.get<UserData>(`${this.baseUrl}/${id}/`);
  }

  updateUser(user: UserPost): Observable<any> {

    let id=localStorage.getItem('id');
    const formData = new FormData();

    formData.append('email', user.email);
    formData.append('username', user.username);
    formData.append('city', user.city);
    formData.append('password', user.password);

    if (user.user_image) {
      formData.append('user_image', user.user_image);
    }

    return this.http.put(`${this.baseUrl}/${id}/`, formData);
  }
}
