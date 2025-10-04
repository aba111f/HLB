import { Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-register',
  imports: [],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('login-section') loginSection!: ElementRef;


  

  showLogin() {
    this.loginSection.nativeElement.style.display = 'block';
    this.registerSection.nativeElement.style.display = 'none';
    this.loginSection.nativeElement.scrollIntoView({behavior: 'smooth'});
            
        }
}
