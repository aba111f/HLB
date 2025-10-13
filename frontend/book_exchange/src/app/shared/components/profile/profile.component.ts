import { Component, OnInit } from '@angular/core';
import { UserPost } from '../../interface/interface';
import { ProfileService } from '../../../core/services/profile/profile.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile', 
  imports: [FormsModule, CommonModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user: UserPost = {
    email: '',
    username: '',
    city: '',
    password: '',
    user_image: null
  };

  imagePreview: string | ArrayBuffer | null = null;

  constructor(private profileService: ProfileService) {}

  ngOnInit(): void {
    this.loadUser();
  }

  loadUser() {
    this.profileService.getCurrentUser().subscribe({
      next: (data) => {
        this.user = data;
        if (data.user_image) {
          this.imagePreview = 'http://localhost:8000' + data.user_image;
        }
      },
      error: (err) => console.error('Error loading user:', err)
    });
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
}
