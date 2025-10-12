import { CommonModule } from '@angular/common';
import { Component, ElementRef, ViewChild, Output, EventEmitter} from '@angular/core';
import { UserPost } from '../../interface/interface';
import { FormsModule} from '@angular/forms';
import { AuthService } from '../../../core/services/auth/auth.service';

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
@Output() toggleLogin = new EventEmitter<boolean>();


  constructor(private auth_service: AuthService){
    console.log(this.auth_service);
  }

  showLogin() {
    // this.loginSection.nativeElement.style.display = 'block';
    // this.registerSection.nativeElement.style.display = 'none';
    // this.loginSection.nativeElement.scrollIntoView({behavior: 'smooth'});

    this.showLoginBool = true;
    this.toggleLogin.emit(this.showLoginBool);
    
            
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
          console.log('user registered: ', res);
        },
        error: (err) => {
          console.log('error: ', err);
        }
      }); 
      console.log('registered');
    }
    else{
      window.alert('something went wrong, the some data is empty');
    } 
  }
  
  

}
