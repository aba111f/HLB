import { CommonModule } from '@angular/common';
import { Component, ElementRef, ViewChild, Output, EventEmitter} from '@angular/core';
import { UserPost } from '../../interface/interface';
import { FormsModule} from '@angular/forms';
import { AuthService } from '../../../core/services/auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [CommonModule, FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('loginSection') loginSection!: ElementRef;

showLoginBool = false;



  constructor(private auth_service: AuthService,
              private router: Router
  ){

  }

  showLogin() {

    this.router.navigate(['/login']);
            
  }

  user: UserPost = {
    username: '',
    email: '',
    password: '',
    city: '',
    user_image: null
  };

  confirmPassword: string = "";
  previewUrl: string | ArrayBuffer | null = null;

  onFileSelected(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    this.user.user_image = file;

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result;
    };
    reader.readAsDataURL(file);
  }

  onsubmit(){
    if (this.user.username && this.user.email && this.user.city && this.user.password && this.user.user_image){
      this.auth_service.register_user(this.user).subscribe({
        next: (res) => {
          window.alert('user registered successfully: ' + res);
          this.router.navigate(['/login']);
        },
        error: (err) => {
          console.log('error: ', err);
        }
      }); 
      
      this.user.username = "";
      this.user.email = "";
      this.user.city = "";
      this.user.password= "";
      this.user.user_image = null;
      this.confirmPassword = "";
      this.previewUrl = null;
    }
    else{
      window.alert('something went wrong, the some data is empty');
    } 
  }
  
  

}
