import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header/header.component';
import { FooterComponent } from './shared/components/footer/footer.component';

@Component({
  selector: 'app-root',
  imports: [CommonModule,RouterOutlet, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'book_exchange';
  showLogin = false;
  showReg = false;

  onToggleLogin(value: boolean){
    this.showLogin = value;
    this.showReg = false;
  }
  // LoginDisable(value: boolean){
  //   this.showLogin = value;

  // }

  onToggleReg(value: boolean){
    this.showReg = value;
    this.showLogin = false;
  }

  
  scrollTo(id: string, event: Event) {
    event.preventDefault();
    const target = document.getElementById(id);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
