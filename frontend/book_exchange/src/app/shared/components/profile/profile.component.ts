import { Component, OnInit } from '@angular/core';
import { UserData, UserGet, UserPost } from '../../interface/interface';
import { ProfileService } from '../../../core/services/profile/profile.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SharingService } from '../../../core/services/sharing/sharing.service';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth/auth.service';

@Component({
  selector: 'app-profile', 
  imports: [FormsModule, CommonModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  // user: UserPost = {
    // email: '',
    // username: '',
    // city: '',
    // password: '',
    // user_image: null
  // };
  // user_source: UserGet = {
    // id: '',
    // date_joined: null,
  //   // is_active: null,
  //   // last_login: null,
  //   user: this.user
  // };
  user: UserData = {
    id: '',
    date_joined: null,
    email: '',
    username: '',
    city: '',
    password: '',
    user_image: null
  };
  

  imagePreview: string | ArrayBuffer | null = null;

  constructor(private profileService: ProfileService, 
              private shared_service: SharingService,
              private auth_service: AuthService,
              private router: Router
  ) {
    // window.location.reload();
  }

  ngOnInit(): void {
    
    this.loadUser();
    
  }

  loadUser() {
    let username = localStorage.getItem('username');
    let email = localStorage.getItem('email');
    let city = localStorage.getItem('city');
    let image  = localStorage.getItem('image');
    if(!username && !email && !city && !image){

      this.profileService.getCurrentUser().subscribe({
        next: (data) => {
          console.log(data);
          this.user = data;

          if (data.user_image) {
            this.imagePreview = '' + data.user_image;
            this.shared_service.set_image(this.imagePreview);
          }
          localStorage.setItem('username', data.username);
          localStorage.setItem('email', data.email);
          localStorage.setItem('city', data.city);
          localStorage.setItem('image', this.imagePreview + '');
        },
        error: (err) => console.error('Error loading user:', err)
      });
    }
    else{
      this.user.username = username + '';
      this.user.email = email + '';
      this.user.city = city + '';
      this.imagePreview = image;
      
    }
  }

  onImageSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.user.user_image = file;
      const reader = new FileReader();
      reader.onload = () => this.imagePreview = reader.result;
      reader.readAsDataURL(file);
    }
  }

  saveProfile() {
    this.profileService.updateUser(this.user).subscribe({
      next: () => alert('Profile updated successfully!'),
      error: (err) => console.error('Update failed:', err)
    });
  }

  quit(){
    let is = confirm('are you sure');
    if(is){
      this.auth_service.logout();
    }
  }
}
