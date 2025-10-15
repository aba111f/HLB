import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth/auth.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-hero',
  imports: [CommonModule],
  templateUrl: './hero.component.html',
  styleUrl: './hero.component.css'
})
export class HeroComponent implements OnInit{
  show_btn: boolean = true;
  constructor(private router: Router,
              private auth_service: AuthService
  ){

  }

  ngOnInit(): void {
    this.show_btn = !this.auth_service.is_logged_in();
    // this.auth_service.isAuthenticated$.subscribe(val => {
    //   this.show_btn = val;
    // }
    // );
  }
  showRegister(){
    this.router.navigate(['/register']);
  }
}
