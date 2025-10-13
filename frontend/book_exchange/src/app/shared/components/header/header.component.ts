import { Component, Output, EventEmitter } from '@angular/core';
import { RegisterComponent } from '../register/register.component';
import { LoginComponent } from '../login/login.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  isPressedLogin: boolean = false;
  isPressedReg: boolean = false;
  show_login_btn: boolean = true;
  show_reg_btn: boolean = true;

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
  
  hide_login_reg_btn(value: boolean){
    this.isPressedLogin = false;
    this.isPressedReg = false;
  }


}
