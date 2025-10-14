import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharingService {




  constructor() {

   }

    // Not neccessary info
  private show_login_btn = new BehaviorSubject<boolean>(true);
  current_state = this.show_login_btn.asObservable();

  set_bool(value: boolean){
    this.show_login_btn.next(value);
  }





    // Auth Check
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  check_auth_state(value: boolean){
    
    this.isAuthenticatedSubject.next(value);
  } 


  private imageSubject = new BehaviorSubject<string>('');
  image = this.imageSubject.asObservable();

  set_image(value: string){
    this.imageSubject.next(value);
  }
}
