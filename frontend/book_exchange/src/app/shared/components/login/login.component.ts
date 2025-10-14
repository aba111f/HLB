import { Component, ElementRef, ViewChild, Output, EventEmitter } from '@angular/core';
import { UserPost } from '../../interface/interface';
import { AuthService } from '../../../core/services/auth/auth.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SharingService } from '../../../core/services/sharing/sharing.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('login-section') loginSection!: ElementRef;

  constructor(private auth_service: AuthService, 
              private shared_service: SharingService,
              private router: Router
  ){}

showReg = false;
showLogin = true;
@Output() toggleReg = new EventEmitter<boolean>();
@Output() toggleLogin = new EventEmitter<boolean>();


  showRegister() {
      // this.registerSection.nativeElement.style.display = 'block';
      // this.loginSection.nativeElement.style.display = 'none';
      // this.registerSection.nativeElement.scrollIntoView({behavior: 'smooth'});
    this.showReg = true;
    this.toggleReg.emit(this.showReg);
  }

  user: UserPost = {
    username: '',
    email: '',
    password: '',
    city: '',
    user_image: null
  };

  onsubmit(){
    if(this.user.email && this.user.password){
      this.auth_service.login_user_token_data(this.user).subscribe({
        next: (res) => {
          console.log('successfully logged in: ', res);
        },
        error: (err) => {
          console.log('Error: ', err)
        }
      });
      this.showLogin = false;
      this.toggleLogin.emit(this.showLogin);
      this.shared_service.check_auth_state(this.showLogin);
      this.router.navigate(['/profile']);
    }
    else{
      window.alert('Error occured: not logged in');
    }
  }
  
}
