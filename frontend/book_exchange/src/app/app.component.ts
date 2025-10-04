import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header/header.component';
import { FooterComponent } from './shared/components/footer/footer.component';
import { HeroComponent } from './shared/components/hero/hero.component';
import { LoginComponent } from './shared/components/login/login.component';
import { RegisterComponent } from './shared/components/register/register.component';
import { FeaturesComponent } from './shared/components/features/features.component';
import { BooksComponent } from './shared/components/books/books.component';
@Component({
  selector: 'app-root',
  imports: [HeaderComponent, FooterComponent, HeroComponent, LoginComponent, RegisterComponent, FeaturesComponent, BooksComponent, CommonModule],
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
