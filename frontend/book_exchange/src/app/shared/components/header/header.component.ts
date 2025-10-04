import { Component, Output, EventEmitter } from '@angular/core';
import { RegisterComponent } from '../register/register.component';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  isPressedLogin: boolean = false;
  isPressedReg: boolean = false;

  @Output() toggleLogin = new EventEmitter<boolean>();
  @Output() toggleReg = new EventEmitter<boolean>();
  showLogin(){
    this.isPressedLogin = true;
    this.isPressedReg = false;
    this.toggleLogin.emit(this.isPressedLogin);
    
  }
  showReg(){
    this.isPressedReg = true;
    this.isPressedLogin = false;
    this.toggleReg.emit(this.isPressedReg);
  }
  


}
