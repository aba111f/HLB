import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { RegisterComponent } from '../register/register.component';
import { LoginComponent } from '../login/login.component';
import { CommonModule } from '@angular/common';
import { SharingService } from '../../../core/services/sharing/sharing.service';
@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit{
  isPressedLogin: boolean = false;
  isPressedReg: boolean = false;
  show_login_btn: boolean = true;
  show_reg_btn: boolean = true;

  @Output() toggleLogin = new EventEmitter<boolean>();
  @Output() toggleReg = new EventEmitter<boolean>();

  constructor(private shared_service: SharingService){}
  ngOnInit(): void {
      this.shared_service.current_state.subscribe(value => {
        this.show_login_btn = value;
        this.show_reg_btn = value;
      }
      );
  }

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
