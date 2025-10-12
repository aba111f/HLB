import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserPost } from '../../../shared/interface/interface';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  readonly apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

  register_user(user: UserPost){
    const formData = new FormData();
    formData.append('username', user.username);
    formData.append('email', user.email);
    formData.append('password', user.password);
    formData.append('city', user.city);
    if (user.user_image) {
      formData.append('user_image', user.user_image);
      console.log('image sent');
    }
    else{
      console.log('image not sent');
    }
    return this.http.post(this.apiUrl + '/users/', formData);
  }
}
