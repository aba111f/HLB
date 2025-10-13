import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserData, UserPost } from '../../../shared/interface/interface';
import { Observable, tap } from 'rxjs';
import { Token } from '../../../shared/interface/auth_model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  readonly apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }


  // REGISTER SECTION
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
  username: string = '';
  
  // LOGIN SECTION
  login_user_token_data(user: UserPost): Observable<Token>{
    const formData = new FormData();
    formData.append('email', user.email);
    formData.append('password', user.password);


    return this.http.post<Token>(this.apiUrl + '/login/', formData)
      .pipe(tap((token: Token) =>{
          localStorage.setItem("access", token.access);
          localStorage.setItem("refresh", token.refresh);
          localStorage.setItem('id', token.id);
        })
      );
  }

  // login_user_user_data(user: UserPost): Observable<UserData>{

  //   return this.http.post<UserData>(this.apiUrl + '/.../', user);
  // } 
  
}
