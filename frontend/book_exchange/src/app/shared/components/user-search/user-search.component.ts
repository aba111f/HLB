import { Component } from '@angular/core';
import { UserSearchService } from '../../../core/services/user_search/user-search.service';
import { BookUser, Result } from '../../interface/book-user';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  imports: [FormsModule, CommonModule],
  selector: 'app-user-search',
  templateUrl: './user-search.component.html',
  styleUrls: ['./user-search.component.css']
})
export class UserSearchComponent {
  users: BookUser[] = [];
  title = '';
  author = '';
  genre = '';
  exchange_type = '';
  book_image_preview: string = '';
  exchangeOptions = ['Exchange', 'Lend', 'Giveaway'];

  constructor(private userSearchService: UserSearchService) {}

  search() {
    const filters = {
      title: this.title,
      author: this.author,
      genre: this.genre
    };

    this.userSearchService.searchUsers(filters).subscribe({
      next: data => {
        this.users = data.results;
        if(data){
          console.log(data);
        }
        if(this.users[0].book_image){
          console.log(this.users[0].book_image);
          this.book_image_preview = 'http://localhost:8000' + this.users[0].book_image;
        }

      },
      error: err => console.error(err)
    });
  }
}
