import { Component, ElementRef, ViewChild, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('login-section') loginSection!: ElementRef;

showReg = false;
@Output() toggleReg = new EventEmitter<boolean>();

  showRegister() {
            // this.registerSection.nativeElement.style.display = 'block';
            // this.loginSection.nativeElement.style.display = 'none';
            // this.registerSection.nativeElement.scrollIntoView({behavior: 'smooth'});
          this.showReg = true;
          this.toggleReg.emit(this.showReg);
        }
}
