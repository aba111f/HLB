import { Component } from '@angular/core';
import { UserSearchService,BookUser } from '../../../core/services/user_search/user-search.service';

@Component({
  selector: 'app-user-search',
  templateUrl: './user-search.component.html',
  styleUrls: ['./user-search.component.css']
})
export class UserSearchComponent {
  users: BookUser[] = [];
  title = '';
  city = '';
  genre = '';
  exchange_type = '';

  exchangeOptions = ['Exchange', 'Lend', 'Giveaway'];

  constructor(private userSearchService: UserSearchService) {}

  search() {
    const filters = {
      title: this.title,
      city: this.city,
      genre: this.genre,
      exchange_type: this.exchange_type
    };

    this.userSearchService.searchUsers(filters).subscribe({
      next: data => this.users = data,
      error: err => console.error(err)
    });
  }
}
