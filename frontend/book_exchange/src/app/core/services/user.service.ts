import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  readonly baseUrl = 'http://127.0.0.1:8000/api/users/';

  constructor(private http: HttpClient) { }

  get_user(){
    
  }
}
