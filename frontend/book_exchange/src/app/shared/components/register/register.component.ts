import { Component, ElementRef, ViewChild, Output, EventEmitter} from '@angular/core';

@Component({
  selector: 'app-register',
  imports: [],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
@ViewChild('registerSection') registerSection!: ElementRef;
@ViewChild('loginSection') loginSection!: ElementRef;

showLoginBool = false;
@Output() toggleLogin = new EventEmitter<boolean>();


  

  showLogin() {
    // this.loginSection.nativeElement.style.display = 'block';
    // this.registerSection.nativeElement.style.display = 'none';
    // this.loginSection.nativeElement.scrollIntoView({behavior: 'smooth'});

    this.showLoginBool = true;
    this.toggleLogin.emit(this.showLoginBool);
    
            
        }
}
