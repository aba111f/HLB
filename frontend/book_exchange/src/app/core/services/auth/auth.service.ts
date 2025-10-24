import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserData, UserPost } from '../../../shared/interface/interface';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Token } from '../../../shared/interface/auth_model';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  readonly apiUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient,
              private router: Router
  ) { this.check_auth_state(); }


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
    return this.http.post(this.apiUrl + 'users/', formData);
  }
  username: string = '';
  
  // LOGIN SECTION
  login_user_token_data(user: UserPost): Observable<Token>{
    const formData = new FormData();
    formData.append('email', user.email);
    formData.append('password', user.password);


    return this.http.post<Token>(this.apiUrl + 'common/login/', formData)
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
  

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticatedSubject.asObservable();
  
  private check_auth_state(){
      if (typeof window !== 'undefined' && window.localStorage) {
      const token = localStorage.getItem('access');
      this.isAuthenticatedSubject.next(!!token);
    } else {
      this.isAuthenticatedSubject.next(false);
    }
    } 

  logout(){
    localStorage.removeItem('refresh');
    localStorage.removeItem('access');
    localStorage.removeItem('id');
    localStorage.removeItem('image');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    localStorage.removeItem('city');
    localStorage.removeItem('password');
    this.router.navigate(['/']);
    this.isAuthenticatedSubject.next(false);
  }
  logged(){
    this.isAuthenticatedSubject.next(true);
  }
  is_logged_in(){
    return this.isAuthenticatedSubject.value;
  }

  delete(id: string, user_data: {
    email: string,
    password: string
  }): Observable<string>{
    return this.http.delete<string>(this.apiUrl + `users/${id}/`, { body: user_data });
  }
}
