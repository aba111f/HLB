import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharingService } from '../../../core/services/sharing/sharing.service';
import { Router } from '@angular/router';
import { ProfileService } from '../../../core/services/profile/profile.service';
import { UserGet } from '../../interface/interface';
import { AuthService } from '../../../core/services/auth/auth.service';
@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit{
  show_login_btn: boolean = true;
  show_reg_btn: boolean = true;
  image_preview: string = '';



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
              private profile_service: ProfileService,
              private auth_service: AuthService,
              private router: Router
  )
  {
    this.show_login_btn = this.auth_service.is_logged_in();
    this.show_reg_btn = this.show_login_btn;
  }
  
  ngOnInit(): void {

      this.auth_service.isAuthenticated$.subscribe(value => {
        this.show_login_btn = value;
        this.show_reg_btn = value;
      });
      

      // this.shared_service.image.subscribe(value => {
      //   this.image_preview = value;
      // });
      if (typeof window !== 'undefined' && window.localStorage) {
      // localStorage.setItem('image', value);
      this.image_preview = localStorage.getItem('image') + '';
    }
  }

  goLogin(){
    this.router.navigate(['/login']);
    
  }
  goReg(){
    this.router.navigate(['/register']);
  }
  
  go_profile(){
    this.router.navigate(['/profile']);
  } 

  go_search(){
    this.router.navigate(['/user-search']);
  }

}
