import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharingService {
  private show_login_btn = new BehaviorSubject<boolean>(true);
  current_state = this.show_login_btn.asObservable();

  constructor() { }

  set_bool(value: boolean){
    this.show_login_btn.next(value);
  }
}
