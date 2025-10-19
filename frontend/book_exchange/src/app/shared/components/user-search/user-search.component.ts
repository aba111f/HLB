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
        

      },
      error: err => console.error(err)
    });
  }
}
