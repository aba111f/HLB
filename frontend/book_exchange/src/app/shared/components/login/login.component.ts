import { Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('login-section') loginSection!: ElementRef;

  showRegister() {
            this.registerSection.nativeElement.style.display = 'block';
            this.loginSection.nativeElement.style.display = 'none';
            this.registerSection.nativeElement.scrollIntoView({behavior: 'smooth'});
        }
}
