import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { RegisterComponent } from '../register/register.component';
import { LoginComponent } from '../login/login.component';
import { CommonModule } from '@angular/common';
import { SharingService } from '../../../core/services/sharing/sharing.service';

import { ProfileService } from '../../../core/services/profile/profile.service';
import { UserGet } from '../../interface/interface';
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
  image_preview: string = '';

  @Output() toggleLogin = new EventEmitter<boolean>();
  @Output() toggleReg = new EventEmitter<boolean>();

  user_source: UserGet = {
    id: '',
    date_joined: null,
    // is_active: null,
    // last_login: null,
    user: {
      email: '',
      username: '',
      city: '',
      password: '',
      user_image: null
    }
  };

  constructor(private shared_service: SharingService,
              private profile_service: ProfileService
  )
  {
    
  }
  ngOnInit(): void {

      this.shared_service.isAuthenticated$.subscribe(value => {
        this.show_login_btn = value;
        this.show_reg_btn = value;
      });
      this.shared_service.image.subscribe(value => {
        this.image_preview = value;
      });
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
